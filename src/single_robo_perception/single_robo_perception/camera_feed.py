#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from ultralytics import YOLO
import numpy as np
import threading
import queue
import time
from collections import deque

class CameraFeed(Node):
    def __init__(self):
        super().__init__('camera_feed_viewer')
        self.bridge = CvBridge()

        # ---------- YOLO settings ----------
        # Use a small model for CPU: yolov8n.pt is the smallest (nano)
        self.model = YOLO('/home/asd/Downloads/best (1).pt')
        # Optional: reduce inference image size (default 640). Smaller = faster but less accurate.
        self.imgsz = 320  # try 320 or 416
        # Process every Nth frame (skip frames to reduce CPU load)
        self.frame_skip = 2  # process every 2nd frame
        self.frame_counter = 0

        self.get_logger().info('YOLO model loaded (CPU mode).')

        # ---------- Queues for threading ----------
        # Queue for raw frames (to be processed by inference thread)
        self.frame_queue = queue.Queue(maxsize=5)  # limit to avoid memory build-up
        # Queue for annotated frames (to be displayed)
        self.result_queue = queue.Queue(maxsize=2)

        # ---------- FPS calculation ----------
        self.raw_fps_history = deque(maxlen=30)   # store last 30 frame times
        self.yolo_fps_history = deque(maxlen=30)

        # ---------- Start inference thread ----------
        self.running = True
        self.inference_thread = threading.Thread(target=self.inference_loop, daemon=True)
        self.inference_thread.start()

        # ---------- Subscription ----------
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',   # adjust to your topic
            self.image_callback,
            10)
        self.subscription

    def image_callback(self, msg):
        """Main callback (runs in ROS spin thread)."""
        try:
            # Convert ROS Image to OpenCV BGR
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f'Error converting image: {e}')
            return

        # ---- Display raw feed with FPS ----
        now = time.time()
        self.raw_fps_history.append(now)
        # Compute FPS over last N frames
        if len(self.raw_fps_history) > 1:
            fps = len(self.raw_fps_history) / (self.raw_fps_history[-1] - self.raw_fps_history[0])
        else:
            fps = 0.0
        # Put FPS text on raw frame
        raw_display = frame.copy()
        cv2.putText(raw_display, f'Raw FPS: {fps:.1f}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Raw Feed', raw_display)
        cv2.waitKey(1)

        # ---- Push frame to inference queue (if not full) ----
        # Use frame skipping to reduce load
        self.frame_counter += 1
        if self.frame_counter % self.frame_skip == 0:
            try:
                # Put frame with timestamp
                self.frame_queue.put_nowait((frame, now))
            except queue.Full:
                # If queue full, skip this frame (old frame not processed yet)
                pass

        # ---- Check for latest YOLO result ----
        # Show the most recent annotated frame (if any)
        annotated_frame = None
        yolo_fps = 0.0
        while not self.result_queue.empty():
            annotated_frame, yolo_fps = self.result_queue.get_nowait()  # keep only latest

        if annotated_frame is not None:
            # Add YOLO FPS text
            cv2.putText(annotated_frame, f'YOLO FPS: {yolo_fps:.1f}', (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('YOLO Feed', annotated_frame)
            cv2.waitKey(1)

    def inference_loop(self):
        """Separate thread: runs YOLO on frames from queue."""
        yolo_fps_history = deque(maxlen=30)
        while self.running:
            try:
                # Wait for a frame (with timeout to allow checking self.running)
                frame, timestamp = self.frame_queue.get(timeout=0.1)
            except queue.Empty:
                continue

            # Run YOLO inference (on CPU, verbose=False)
            results = self.model(frame, imgsz=self.imgsz, verbose=False)

            # Annotate frame
            annotated = frame.copy()
            if results and len(results) > 0:
                boxes = results[0].boxes
                if boxes is not None:
                    for box in boxes:
                        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                        conf = float(box.conf[0])
                        cls_id = int(box.cls[0])
                        label = f'{self.model.names[cls_id]}: {conf:.2f}'
                        cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(annotated, label, (x1, y1-10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Compute YOLO FPS (based on time between frames processed)
            now = time.time()
            yolo_fps_history.append(now)
            if len(yolo_fps_history) > 1:
                yolo_fps = len(yolo_fps_history) / (yolo_fps_history[-1] - yolo_fps_history[0])
            else:
                yolo_fps = 0.0

            # Send result to main thread (overwrite old if any)
            # We'll clear the queue and put only the latest to avoid lag
            while not self.result_queue.empty():
                try:
                    self.result_queue.get_nowait()
                except queue.Empty:
                    break
            self.result_queue.put_nowait((annotated, yolo_fps))

    def destroy_node(self):
        self.running = False
        if self.inference_thread.is_alive():
            self.inference_thread.join(timeout=1.0)
        cv2.destroyAllWindows()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = CameraFeed()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()