#!/usr/bin/env python3
from turtle import width

import rclpy
from rclpy.executors import MultiThreadedExecutor
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
import math

from tf2_ros import Buffer, TransformListener
from tf2_geometry_msgs import do_transform_point
from geometry_msgs.msg import PointStamped
from single_robo_custom_interface.msg import ComWithID, ClusterPoints

class CameraToWorldTransformer(Node):
    def __init__(self, camera_frame, world_frame):
        super().__init__('camera_to_world_transformer')
        self.camera_frame = camera_frame
        self.world_frame = world_frame
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.get_logger().info(f'Transformer initialized: camera_frame={camera_frame}, world_frame={world_frame}')  # LOG

    def transform_point(self, x, y, z, timeout_sec=1.0):
        """
        Transform a point from camera frame to world frame.
        Returns a tuple (x_world, y_world, z_world) or None if transform fails.
        """
        point_camera = PointStamped()
        point_camera.header.frame_id = self.camera_frame
        point_camera.header.stamp = self.get_clock().now().to_msg()
        point_camera.point.x = x
        point_camera.point.y = y
        point_camera.point.z = z

        try:
            # Look up the transform with a timeout
            transform = self.tf_buffer.lookup_transform(
                self.world_frame,
                self.camera_frame,
                rclpy.time.Time(),  # latest available transform
                timeout=rclpy.duration.Duration(seconds=timeout_sec)
            )
            point_world = do_transform_point(point_camera, transform)
            # LOG: successful transform
            self.get_logger().debug(f'Transform success: ({x:.2f},{y:.2f},{z:.2f}) -> ({point_world.point.x:.2f},{point_world.point.y:.2f},{point_world.point.z:.2f})')
            return (point_world.point.x, point_world.point.y, point_world.point.z)
        except Exception as e:
            self.get_logger().warn(f"Transform failed for point ({x:.2f},{y:.2f},{z:.2f}): {e}")
            return None


class GridClusterCOM:
    def __init__(self, com_radius, reduction_threshold=None):
        """
        com_radius: maximum distance from centroid to any point in the cluster.
        reduction_threshold: if set, each cluster stores at most this many
                             raw points (oldest are discarded). Centroid is
                             still computed from all points.
        """
        self.com_radius = com_radius
        self.cell_size = com_radius / np.sqrt(3)
        self.reduction_threshold = reduction_threshold
        self.clusters = []                    # list of {'id': int, 'leader': tuple, 'points': deque, 'count': int}
        self.cell_to_cluster = {}             # maps grid cell key -> index in self.clusters
        # LOG: clustering initialized
        # No logger here because this is not a Node; we'll log from CameraFeed

    def _cell_key(self, point):
        return tuple(np.floor(point / self.cell_size).astype(int))

    def add_point(self, point):
        point = np.asarray(point)
        point_tuple = tuple(float(x) for x in point)

        key = self._cell_key(point)

        if key not in self.cell_to_cluster:
            # Create a new cluster
            new_id = len(self.clusters) + 1
            if self.reduction_threshold is not None:
                points_buffer = deque(maxlen=self.reduction_threshold)
                points_buffer.append(point_tuple)
            else:
                points_buffer = [point_tuple]   # store all points (unbounded)

            cluster = {
                'id': new_id,
                'leader': point_tuple,
                'points': points_buffer,
                'count': 1
            }
            self.cell_to_cluster[key] = len(self.clusters)
            self.clusters.append(cluster)
            # LOG: new cluster created (will be logged by caller)
        else:
            cluster_idx = self.cell_to_cluster[key]
            cluster = self.clusters[cluster_idx]

            # Update centroid using weighted average
            old_count = cluster['count']
            old_leader = np.array(cluster['leader'])
            new_leader = (old_leader * old_count + point) / (old_count + 1)
            cluster['leader'] = tuple(float(x) for x in new_leader)
            cluster['count'] += 1

            # Add point to raw buffer (deque automatically discards oldest if at maxlen)
            if cluster['points'] is not None:
                cluster['points'].append(point_tuple)

        return [cluster['leader'] , cluster['id']]

    def get_all_centroids(self):
        return [cluster['leader'] for cluster in self.clusters]

    def get_cluster_points(self, cluster_id):
        """
        Return the raw points buffer (deque or list) for a given cluster ID,
        or None if the cluster does not exist.
        """
        for cl in self.clusters:
            if cl['id'] == cluster_id:
                return cl['points']
        return None

class CameraFeed(Node):
    def __init__(self, transformer_node):
        super().__init__('camera_feed_viewer')
        self.bridge = CvBridge()
        self.transformer_node = transformer_node
        self.clusterer = GridClusterCOM(com_radius=1.0, reduction_threshold=10) # in meters

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
        self.get_logger().info('Inference thread started')  # LOG

        # ---------- Subscription ----------
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',   # adjust to your topic
            self.image_callback,
            10)
        self.subscription
        self.get_logger().info('Subscribed to /camera/image_raw')  # LOG

        # ---------- Publishers ----------
        # Publisher for raw world points (each detection)
        self.point_publisher = self.create_publisher(
            ClusterPoints,
            '/world_points',
            10
        )
        self.get_logger().info('Publisher created: /world_points')  # LOG
        
        # Publisher for cluster centroids with IDs
        self.com_publisher = self.create_publisher(
            ComWithID,
            '/cluster_centroids',
            10
        )
        self.get_logger().info('Publisher created: /cluster_centroids')  # LOG

    def image_callback(self, msg):
        """Main callback (runs in ROS spin thread)."""
        self.get_logger().info(f'Image received, current frame_counter={self.frame_counter}')  # LOG
        try:
            # Convert ROS Image to OpenCV BGR
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            self.get_logger().info(f'Image converted, shape: {frame.shape}')  # LOG
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
        self.get_logger().info('Raw feed displayed')  # LOG

        # ---- Push frame to inference queue (if not full) ----
        # Use frame skipping to reduce load
        self.frame_counter += 1
        self.get_logger().info(f'After increment, frame_counter={self.frame_counter}')  # LOG
        skip_condition = (self.frame_counter % self.frame_skip == 0)
        self.get_logger().info(f'Frame skip check: {self.frame_counter} % {self.frame_skip} = {self.frame_counter % self.frame_skip} -> {skip_condition}')  # LOG
        if skip_condition:
            try:
                # Put frame with timestamp
                self.get_logger().info(f'Attempting to push frame to inference queue, queue size approx {self.frame_queue.qsize()}')  # LOG
                self.frame_queue.put_nowait((frame, now))
                self.get_logger().info(f'Frame pushed to inference queue (frame #{self.frame_counter}), queue size now {self.frame_queue.qsize()}')  # LOG
            except queue.Full:
                self.get_logger().warn('Frame queue full, skipping frame')  # LOG
                pass
        else:
            self.get_logger().info('Frame skip: not pushing this frame')  # LOG

        # ---- Check for latest YOLO result ----
        # Show the most recent annotated frame (if any)
        annotated_frame = None
        yolo_fps = 0.0
        while not self.result_queue.empty():
            annotated_frame, yolo_fps = self.result_queue.get_nowait()  # keep only latest
            self.get_logger().info('New YOLO result retrieved from queue')  # LOG

        if annotated_frame is not None:
            # Add YOLO FPS text
            cv2.putText(annotated_frame, f'YOLO FPS: {yolo_fps:.1f}', (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('YOLO Feed', annotated_frame)
            cv2.waitKey(1)
            self.get_logger().info('YOLO feed displayed')  # LOG


    def calculate_area(self,frame, x1, y1, x2, y2):
        frame_copy = frame.copy()
        area = abs(x2 - x1) * abs(y2 - y1)
        return area
    
    def get_depth_from_area(self,area):
        caliberation_area_for_1m = 10000  # example area corresponding to 1 meter distance
        distance = 1.0 * (caliberation_area_for_1m / area) ** 0.5  # simple inverse square relationship
        self.get_logger().debug(f'Depth from area {area:.2f}: {distance:.2f}')  # LOG
        return distance

    
    def map(self, value, in_min, in_max, out_min, out_max):
            """Map a value from one range to another."""
            return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    
    def polar_to_cartesian(self, r, theta_1, theta_2):
            """Convert polar coordinates (distance, horizontal angle, vertical angle) to Cartesian."""
            x_w = r * math.cos(theta_2) * math.cos(theta_1)
            y_w = r * math.cos(theta_2) * math.sin(theta_1)
            z_w = r * math.sin(theta_2)
            return x_w, y_w, z_w
    
    def camera_to_world(self, x_c, y_c, z_c):
            """Convert camera coordinates to world coordinates (apply rotation/translation)."""
            world_coords = self.transformer_node.transform_point(x_c, y_c, z_c)
            # LOG: result from transformer
            self.get_logger().debug(f'camera_to_world: ({x_c:.2f},{y_c:.2f},{z_c:.2f}) -> {world_coords}')
            return world_coords[0], world_coords[1], world_coords[2]
    
    def get_world_point(self,frame, cx, cy, area):
        frame_height = frame.shape[0]
        frame_width = frame.shape[1]
        pixel_left = 0
        pixel_right = frame_width
        pixel_top = 0
        pixel_bottom = frame_height

        fov_horizontal = 90  # example horizontal FOV in degrees
        fov_vertical = 60    # example vertical FOV in degrees
        angl_left = -fov_horizontal / 2
        angl_right = fov_horizontal / 2
        angl_top = fov_vertical / 2
        angl_bottom = -fov_vertical / 2

        theta_1 = self.map(cx, pixel_left, pixel_right, angl_left, angl_right)  # 2d points to angle
        theta_2 = self.map(cy, pixel_top, pixel_bottom, angl_top, angl_bottom)
        
        # Convert degrees to radians
        theta_1_rad = math.radians(theta_1)
        theta_2_rad = math.radians(theta_2)

        r = self.get_depth_from_area(area) # area to distance (based on calibration)

        x_c, y_c, z_c = self.polar_to_cartesian(r, theta_1_rad, theta_2_rad) # convert to world coordinates
        x_w, y_w, z_w = self.camera_to_world(x_c, y_c, z_c)

        self.get_logger().info(f'get_world_point: (cx={cx:.1f}, cy={cy:.1f}, area={area:.1f}) -> world ({x_w:.2f},{y_w:.2f},{z_w:.2f})')  # LOG
        return x_w, y_w, z_w


    def publish_point(self, x_w, y_w, z_w):
        """
        Publish a single detected point in world coordinates
        """
        msg = ClusterPoints()
        msg.arr = [float(x_w), float(y_w), float(z_w)]
        self.point_publisher.publish(msg)
        self.get_logger().info(f'Published point: ({x_w:.2f}, {y_w:.2f}, {z_w:.2f})')  # LOG (changed from debug to info for visibility)

    def publish_COM(self, nearest_cluster_centroid_point, id):
        """
        Publish cluster centroid with ID
        nearest_cluster_centroid_point: tuple or list of (x, y, z)
        id: integer cluster ID
        """
        msg = ComWithID()
        msg.arr = [
            float(nearest_cluster_centroid_point[0]),
            float(nearest_cluster_centroid_point[1]),
            float(nearest_cluster_centroid_point[2])
        ]
        msg.id = int(id)
        self.com_publisher.publish(msg)
        self.get_logger().info(f'Published COM: ID={id}, point=({msg.arr[0]:.2f}, {msg.arr[1]:.2f}, {msg.arr[2]:.2f})')  # LOG (changed from debug to info)

    
    def get_id_with_com(self, pt):
        nearest_cluster_centroid_point, id = self.clusterer.add_point(pt)
        self.get_logger().info(f'Clustering: point {pt} -> centroid {nearest_cluster_centroid_point}, ID {id}')  # LOG
        return [nearest_cluster_centroid_point, id]

    # def publish_COM(self, nearest_cluster_centroid_point, id):
    #     pass

    def inference_loop(self):
        """Separate thread: runs YOLO on frames from queue."""
        yolo_fps_history = deque(maxlen=30)
        self.get_logger().info('Inference loop started')  # LOG
        last_heartbeat = time.time()
        while self.running:
            # Heartbeat log every 5 seconds to confirm thread is alive
            if time.time() - last_heartbeat > 5.0:
                self.get_logger().info('Inference thread heartbeat: waiting for frames...')
                last_heartbeat = time.time()

            try:
                # Wait for a frame (with timeout to allow checking self.running)
                frame, timestamp = self.frame_queue.get(timeout=0.1)
                self.get_logger().info(f'Frame popped from queue, queue size now {self.frame_queue.qsize()}')  # LOG
            except queue.Empty:
                continue

            # Run YOLO inference (on CPU, verbose=False)
            self.get_logger().info('Starting YOLO inference...')  # LOG
            results = self.model(frame, imgsz=self.imgsz, verbose=False)
            self.get_logger().info(f'YOLO inference done, found {len(results)} results')  # LOG

        # ... rest of the method ...

            # Annotate frame
            annotated = frame.copy()
            if results and len(results) > 0:
                boxes = results[0].boxes
                if boxes is not None:
                    num_boxes = len(boxes)
                    self.get_logger().info(f'Detected {num_boxes} boxes')  # LOG
                    for i, box in enumerate(boxes):
                        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                        cx , cy = (x1 + x2) / 2, (y1 + y2) / 2
                        area = self.calculate_area(frame, x1, y1, x2, y2)
                        conf = float(box.conf[0])
                        cls_id = int(box.cls[0])
                        label = f'{self.model.names[cls_id]}: {conf:.2f}'
                        self.get_logger().info(f'Box {i}: x1={x1}, y1={y1}, x2={x2}, y2={y2}, conf={conf:.2f}, class={cls_id}')  # LOG

                        x_w,y_w,z_w = self.get_world_point(frame,cx, cy, area)
                        self.publish_point(x_w,y_w,z_w)

                        # After publishing
                        cluster_centroid, cluster_id = self.get_id_with_com((x_w, y_w, z_w))
                        self.publish_COM(cluster_centroid, cluster_id)

                        # Draw on image
                        cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        # Label with class and confidence
                        label_text = f"{self.model.names[cls_id]}: {conf:.2f}"
                        cv2.putText(annotated, label_text, (x1, y1 - 25),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        # ID and centroid text
                        id_text = f"ID:{cluster_id}"
                        centroid_text = f"({cluster_centroid[0]:.2f}, {cluster_centroid[1]:.2f}, {cluster_centroid[2]:.2f})"
                        cv2.putText(annotated, id_text, (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
                        cv2.putText(annotated, centroid_text, (x1, y1 + 15),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0), 1)
                else:
                    self.get_logger().info('No boxes detected')  # LOG
            else:
                self.get_logger().info('No results from YOLO')  # LOG

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
            self.get_logger().info('Annotated frame sent to result queue')  # LOG

    def destroy_node(self):
        self.running = False
        if self.inference_thread.is_alive():
            self.inference_thread.join(timeout=1.0)
        cv2.destroyAllWindows()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)

    # Create both nodes
    transformer_node = CameraToWorldTransformer('camera_link', 'map')
    camera_node = CameraFeed(transformer_node)

    # Create a multi-threaded executor
    executor = MultiThreadedExecutor(num_threads=2)  # you can adjust the number of threads

    # Add nodes to the executor
    executor.add_node(camera_node)
    executor.add_node(transformer_node)

    try:
        # Spin both nodes together
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        # Clean shutdown
        executor.shutdown()
        camera_node.destroy_node()
        transformer_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()