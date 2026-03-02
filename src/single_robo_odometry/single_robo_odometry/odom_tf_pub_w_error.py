#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster
import math

class OdometryTfPublisher(Node):
    def __init__(self):
        super().__init__('odometry_tf_publisher')
        
        # Parameters
        self.declare_parameter('odom_frame', 'odom')
        self.declare_parameter('base_frame', 'base_footprint_error')
        self.declare_parameter('publish_rate', 50.0)
        self.declare_parameter('warning_threshold', 0.5)  # Reduced from 1.0 to 0.5 seconds
        
        # Get parameters
        self.odom_frame = self.get_parameter('odom_frame').value
        self.base_frame = self.get_parameter('base_frame').value
        publish_rate = self.get_parameter('publish_rate').value
        self.warning_threshold = self.get_parameter('warning_threshold').value
        
        # Store latest odometry data
        self.latest_odom = None
        self.latest_odom_time = self.get_clock().now()
        self.warned_old_data = False  # Flag to avoid spamming warnings
        
        # TF Broadcaster
        self.tf_broadcaster = TransformBroadcaster(self)
        
        # Subscriber to odometry
        self.odom_sub = self.create_subscription(
            Odometry,
            '/odom_error',
            self.odom_callback,
            10
        )
        
        # Timer for publishing TF even if odometry updates are slow
        self.timer = self.create_timer(1.0/publish_rate, self.publish_tf)
        
        self.get_logger().info(f'Odometry TF Publisher started')
        self.get_logger().info(f'  Odom frame: {self.odom_frame}')
        self.get_logger().info(f'  Base frame: {self.base_frame}')
        self.get_logger().info(f'  Subscribed to: /odom_calculated')
        
    def odom_callback(self, msg):
        """Callback for odometry messages"""
        self.latest_odom = msg
        self.latest_odom_time = self.get_clock().now()
        self.warned_old_data = False  # Reset warning flag when new data arrives
        
        # Publish TF immediately when new odometry arrives
        self.publish_tf_from_odom(msg)
    
    def publish_tf(self):
        """Publish TF transform based on latest odometry (timer callback)"""
        if self.latest_odom is None:
            # No odometry received yet
            return
        
        current_time = self.get_clock().now()
        
        # Check if odometry is too old
        time_since_odom = (current_time - self.latest_odom_time).nanoseconds / 1e9
        if time_since_odom > self.warning_threshold:
            if not self.warned_old_data:
                self.get_logger().warn(f'Odometry data is {time_since_odom:.2f} seconds old')
                self.warned_old_data = True
        
        # Always publish even if data is old (for continuity)
        self.publish_tf_from_odom(self.latest_odom)
    
    def publish_tf_from_odom(self, odom_msg):
        """Publish TF immediately from odometry message"""
        try:
            transform = TransformStamped()
            
            # Use current time instead of odometry stamp for TF consistency
            # This ensures TF tree doesn't break even if odometry is delayed
            current_time = self.get_clock().now()
            transform.header.stamp = current_time.to_msg()
            transform.header.frame_id = self.odom_frame
            transform.child_frame_id = self.base_frame 
            
            # Copy position from odometry
            transform.transform.translation.x = odom_msg.pose.pose.position.x
            transform.transform.translation.y = odom_msg.pose.pose.position.y
            transform.transform.translation.z = odom_msg.pose.pose.position.z
            
            # Copy orientation from odometry
            transform.transform.rotation = odom_msg.pose.pose.orientation
            
            # Broadcast the transform
            self.tf_broadcaster.sendTransform(transform)
        except Exception as e:
            self.get_logger().error(f'Error publishing TF: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = OdometryTfPublisher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard interrupt, shutting down...')
    except Exception as e:
        node.get_logger().error(f'Node error: {e}')
    finally:
        # Destroy node first, then shutdown
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()

if __name__ == '__main__':
    main()
