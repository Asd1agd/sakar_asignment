#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Point
from std_msgs.msg import ColorRGBA
from single_robo_custom_interface.msg import ComWithID, ClusterPoints
import numpy as np
from collections import defaultdict

class Rviz3DPointVisualizer(Node):
    def __init__(self):
        super().__init__('rviz_3d_point_visualizer')
        
        # ---------- Parameters ----------
        self.declare_parameter('world_frame', 'map')
        self.world_frame = self.get_parameter('world_frame').value
        
        self.declare_parameter('marker_lifetime', 0.1)  # seconds (0 = forever)
        self.marker_lifetime = self.get_parameter('marker_lifetime').value
        
        self.declare_parameter('point_color_r', 1.0)
        self.declare_parameter('point_color_g', 1.0)
        self.declare_parameter('point_color_b', 0.0)
        self.declare_parameter('point_color_a', 0.8)
        
        self.declare_parameter('centroid_color_r', 0.0)
        self.declare_parameter('centroid_color_g', 1.0)
        self.declare_parameter('centroid_color_b', 0.0)
        self.declare_parameter('centroid_color_a', 1.0)
        
        self.declare_parameter('point_size', 0.1)
        self.declare_parameter('centroid_size', 0.3)
        self.declare_parameter('text_size', 0.2)
        
        # ---------- Data storage ----------
        self.points = []  # Store recent points (for trails)
        self.max_points_to_store = 100
        self.centroids = {}  # Dictionary of centroid_id -> (point, timestamp)
        self.centroid_history = defaultdict(list)  # Store trajectory of centroids
        self.max_centroid_history = 20
        
        # ---------- Publishers ----------
        self.marker_publisher = self.create_publisher(
            MarkerArray,
            '/visualization_markers',
            10
        )
        
        # ---------- Subscribers ----------
        self.point_subscriber = self.create_subscription(
            ClusterPoints,
            '/world_points',
            self.point_callback,
            10
        )
        
        self.centroid_subscriber = self.create_subscription(
            ComWithID,  # Note: Capital D in ComWithID
            '/cluster_centroids',
            self.centroid_callback,
            10
        )
        
        # ---------- Timer for periodic marker publishing ----------
        self.timer = self.create_timer(0.1, self.publish_markers)  # 10 Hz
        
        self.get_logger().info('Rviz 3D Point Visualizer initialized')
        self.get_logger().info(f'Using frame: {self.world_frame}')
        
    def point_callback(self, msg):
        """Store incoming world points"""
        point = (msg.points_arr[0], msg.points_arr[1], msg.points_arr[2])
        self.points.append(point)
        
        # Keep only recent points
        if len(self.points) > self.max_points_to_store:
            self.points.pop(0)
    
    def centroid_callback(self, msg):
        """Store incoming centroids with IDs"""
        point = (msg.com_arr[0], msg.com_arr[1], msg.com_arr[2])
        centroid_id = msg.id
        timestamp = self.get_clock().now()
        
        # Update current centroid
        self.centroids[centroid_id] = (point, timestamp)
        
        # Add to history for trajectory
        self.centroid_history[centroid_id].append((point, timestamp))
        
        # Keep only recent history
        if len(self.centroid_history[centroid_id]) > self.max_centroid_history:
            self.centroid_history[centroid_id].pop(0)
    
    def create_point_marker(self, point, marker_id, color=None, scale=None, namespace="points"):
        """Create a sphere marker for a single point"""
        marker = Marker()
        marker.header.frame_id = self.world_frame
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = namespace
        marker.id = marker_id
        marker.type = Marker.SPHERE
        marker.action = Marker.ADD
        
        marker.pose.position.x = float(point[0])
        marker.pose.position.y = float(point[1])
        marker.pose.position.z = float(point[2])
        marker.pose.orientation.w = 1.0
        
        if scale is None:
            marker.scale.x = self.get_parameter('point_size').value
            marker.scale.y = self.get_parameter('point_size').value
            marker.scale.z = self.get_parameter('point_size').value
        else:
            marker.scale.x = scale
            marker.scale.y = scale
            marker.scale.z = scale
        
        if color is None:
            marker.color.r = self.get_parameter('point_color_r').value
            marker.color.g = self.get_parameter('point_color_g').value
            marker.color.b = self.get_parameter('point_color_b').value
            marker.color.a = self.get_parameter('point_color_a').value
        else:
            marker.color = color
        
        marker.lifetime.sec = int(self.marker_lifetime)
        marker.lifetime.nanosec = int((self.marker_lifetime - int(self.marker_lifetime)) * 1e9)
        
        return marker
    
    def create_text_marker(self, point, text, marker_id, color=None, scale=None, namespace="text"):
        """Create a text marker for displaying IDs"""
        marker = Marker()
        marker.header.frame_id = self.world_frame
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = namespace
        marker.id = marker_id
        marker.type = Marker.TEXT_VIEW_FACING
        marker.action = Marker.ADD
        
        # Position text slightly above the point
        marker.pose.position.x = float(point[0])
        marker.pose.position.y = float(point[1])
        marker.pose.position.z = float(point[2]) + 0.3
        marker.pose.orientation.w = 1.0
        
        if scale is None:
            marker.scale.z = self.get_parameter('text_size').value
        else:
            marker.scale.z = scale
        
        if color is None:
            marker.color.r = 1.0
            marker.color.g = 1.0
            marker.color.b = 1.0
            marker.color.a = 1.0
        else:
            marker.color = color
        
        marker.text = text
        marker.lifetime.sec = int(self.marker_lifetime)
        marker.lifetime.nanosec = int((self.marker_lifetime - int(self.marker_lifetime)) * 1e9)
        
        return marker
    
    def create_line_marker(self, points, marker_id, color=None, thickness=0.05, namespace="trajectory"):
        """Create a line strip marker for trajectory visualization"""
        marker = Marker()
        marker.header.frame_id = self.world_frame
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = namespace
        marker.id = marker_id
        marker.type = Marker.LINE_STRIP
        marker.action = Marker.ADD
        
        for point_data in points:
            p = Point()
            p.x = float(point_data[0][0])  # point_data is ((x,y,z), timestamp)
            p.y = float(point_data[0][1])
            p.z = float(point_data[0][2])
            marker.points.append(p)
        
        marker.scale.x = thickness  # Line width
        
        if color is None:
            marker.color.r = 0.0
            marker.color.g = 1.0
            marker.color.b = 1.0
            marker.color.a = 0.5
        else:
            marker.color = color
        
        marker.lifetime.sec = int(self.marker_lifetime * 2)
        marker.lifetime.nanosec = int((self.marker_lifetime * 2 - int(self.marker_lifetime * 2)) * 1e9)
        
        return marker
    
    def create_centroid_marker(self, point, centroid_id, color=None, scale=None, namespace="centroids"):
        """Create a special marker for centroids with ID"""
        # Create sphere
        sphere_marker = self.create_point_marker(
            point, 
            centroid_id * 2,  # Use even IDs for spheres
            color=color or ColorRGBA(
                r=self.get_parameter('centroid_color_r').value,
                g=self.get_parameter('centroid_color_g').value,
                b=self.get_parameter('centroid_color_b').value,
                a=self.get_parameter('centroid_color_a').value
            ),
            scale=scale or self.get_parameter('centroid_size').value,
            namespace="centroids"
        )
        
        # Create text label
        text_marker = self.create_text_marker(
            point,
            f"ID:{centroid_id}",
            centroid_id * 2 + 1,  # Use odd IDs for text
            namespace="centroid_labels"
        )
        
        return sphere_marker, text_marker
    
    def publish_markers(self):
        """Timer callback to publish all markers"""
        marker_array = MarkerArray()
        marker_id = 0
        
        # ----- Publish raw points -----
        for i, point in enumerate(self.points):
            marker = self.create_point_marker(point, marker_id)
            marker_array.markers.append(marker)
            marker_id += 1
        
        # ----- Publish centroids with IDs -----
        for centroid_id, (point, timestamp) in self.centroids.items():
            sphere, text = self.create_centroid_marker(point, centroid_id)
            sphere.id = marker_id
            marker_array.markers.append(sphere)
            marker_id += 1
            text.id = marker_id
            marker_array.markers.append(text)
            marker_id += 1
            
            # Optional: Publish trajectory for this centroid
            if centroid_id in self.centroid_history and len(self.centroid_history[centroid_id]) > 1:
                traj_marker = self.create_line_marker(
                    self.centroid_history[centroid_id],
                    marker_id,
                    namespace=f"trajectory_{centroid_id}"
                )
                if traj_marker.points:  # Only add if there are points
                    marker_array.markers.append(traj_marker)
                    marker_id += 1
        
        # ----- Publish all markers -----
        if marker_array.markers:
            self.marker_publisher.publish(marker_array)
        
        # Optional: Log number of markers published
        # self.get_logger().debug(f'Published {len(marker_array.markers)} markers')


def main(args=None):
    rclpy.init(args=args)
    
    node = Rviz3DPointVisualizer()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()