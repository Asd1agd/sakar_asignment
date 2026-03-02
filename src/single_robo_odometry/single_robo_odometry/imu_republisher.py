#!/usr/bin/env python3
import rclpy
import time
from rclpy.node import Node
from sensor_msgs.msg import Imu

class ImuRepublisher(Node):
    def __init__(self):
        super().__init__('imu_republisher_node')
        
        # Create publisher with queue size 10
        self.imu_pub = self.create_publisher(Imu, "imu_ekf", 10)
        
        # Create subscriber
        self.imu_sub = self.create_subscription(Imu, "imu", self.imu_callback, 10)
        
        self.get_logger().info("IMU Republisher started")
        self.get_logger().info("Subscribing to: imu")
        self.get_logger().info("Publishing to: imu_ekf")
        self.get_logger().info("Frame ID: imu_link_ekf")
    
    def imu_callback(self, imu_msg):
        """Callback for IMU messages"""
        # Create a new message to avoid modifying the original
        new_imu = Imu()
        
        # Copy all data
        new_imu.header = imu_msg.header
        new_imu.orientation = imu_msg.orientation
        new_imu.orientation_covariance = imu_msg.orientation_covariance
        new_imu.angular_velocity = imu_msg.angular_velocity
        new_imu.angular_velocity_covariance = imu_msg.angular_velocity_covariance
        new_imu.linear_acceleration = imu_msg.linear_acceleration
        new_imu.linear_acceleration_covariance = imu_msg.linear_acceleration_covariance
        
        # Set the frame_id that matches the static transform
        new_imu.header.frame_id = "imu_link_ekf"  # This must match the static transform!
        
        # Publish the modified message
        self.imu_pub.publish(new_imu)

def main(args=None):
    rclpy.init(args=args)
    
    # Create and spin the node
    node = ImuRepublisher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()