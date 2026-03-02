#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from nav_msgs.msg import Odometry
import math
import random
import numpy as np

class WheelOdometryNode(Node):
    def __init__(self):
        super().__init__('wheel_odometry_node')
        
        # Robot parameters
        self.declare_parameter('wheel_radius', 0.1)  # meters
        self.declare_parameter('wheel_separation', 0.425)  # meters
        self.declare_parameter('odom_frame_id', 'odom')
        self.declare_parameter('base_frame_id', 'base_footprint_error')
        self.declare_parameter('publish_rate', 50.0)  # Hz
        
        # Wheel noise parameters - standard deviations (σ)
        self.declare_parameter('enable_noise', True)
        self.declare_parameter('left_wheel_noise_std', 0.2)  # radians
        self.declare_parameter('right_wheel_noise_std', 0.2)  # radians
        
        # Error propagation mode
        # 0: Use true values for next iteration (non-accumulative error)
        # 1: Use noisy values for next iteration (accumulative error)
        self.declare_parameter('error_propagation_mode', 1)
        
        # Get parameters
        self.wheel_radius = self.get_parameter('wheel_radius').value
        self.wheel_separation = self.get_parameter('wheel_separation').value
        self.odom_frame_id = self.get_parameter('odom_frame_id').value
        self.base_frame_id = self.get_parameter('base_frame_id').value
        publish_rate = self.get_parameter('publish_rate').value
        
        # Get noise parameters
        self.enable_noise = self.get_parameter('enable_noise').value
        self.left_wheel_noise_std = self.get_parameter('left_wheel_noise_std').value
        self.right_wheel_noise_std = self.get_parameter('right_wheel_noise_std').value
        self.error_propagation_mode = self.get_parameter('error_propagation_mode').value
        
        # True wheel positions (from encoders, no noise)
        self.true_left_wheel_pos = 0.0
        self.true_right_wheel_pos = 0.0
        
        # Last wheel positions (for delta calculation)
        # These will be either true or noisy based on propagation mode
        if self.error_propagation_mode == 0:  # Non-accumulative: use true values
            self.last_left_wheel_pos = 0.0  # True value
            self.last_right_wheel_pos = 0.0  # True value
        else:  # Accumulative: will use noisy values
            self.last_left_wheel_pos = 0.0  # Noisy value
            self.last_right_wheel_pos = 0.0  # Noisy value
        
        # Current noisy wheel positions (calculated each iteration)
        self.noisy_left_wheel_pos = 0.0
        self.noisy_right_wheel_pos = 0.0
        
        # Robot pose (true values - accumulated from true wheel positions)
        self.x_true = 0.0
        self.y_true = 0.0
        self.theta_true = 0.0
        
        # Robot pose (noisy values - accumulated from noisy wheel positions)
        self.x_noisy = 0.0
        self.y_noisy = 0.0
        self.theta_noisy = 0.0
        
        # Robot velocities (calculated from deltas)
        self.vx = 0.0
        self.vtheta = 0.0
        
        # Time tracking
        self.last_time = self.get_clock().now()
        
        # First update flag
        self.first_update = True
        
        # Subscribers
        self.joint_state_sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )
        
        # Publishers
        self.odom_pub = self.create_publisher(
            Odometry,
            '/odom_error',
            10
        )
        
        # Timer for regular publishing
        self.timer = self.create_timer(1.0/publish_rate, self.update_odometry)
        
        self.get_logger().info(f'Wheel Odometry Node started')
        self.get_logger().info(f'Wheel radius: {self.wheel_radius}m, Separation: {self.wheel_separation}m')
        
        if self.enable_noise:
            self.get_logger().info(f'Wheel noise enabled:')
            self.get_logger().info(f'  Left wheel noise: σ={self.left_wheel_noise_std:.6f}rad')
            self.get_logger().info(f'  Right wheel noise: σ={self.right_wheel_noise_std:.6f}rad')
            mode_str = "non-accumulative (use true values)" if self.error_propagation_mode == 0 else "accumulative (use noisy values)"
            self.get_logger().info(f'  Error propagation: {mode_str}')
    
    def joint_state_callback(self, msg):
        """Callback for joint states topic - store true wheel positions"""
        try:
            # Find left and right wheel indices
            left_idx = msg.name.index('base_left_wheel_joint')
            right_idx = msg.name.index('base_right_wheel_joint')
            
            # Update true wheel positions (from encoders, no noise)
            self.true_left_wheel_pos = msg.position[left_idx]
            self.true_right_wheel_pos = msg.position[right_idx]
            
            # If first reading, initialize last positions
            if self.first_update:
                if self.error_propagation_mode == 0:  # Non-accumulative: use true values
                    self.last_left_wheel_pos = self.true_left_wheel_pos
                    self.last_right_wheel_pos = self.true_right_wheel_pos
                else:  # Accumulative: add noise to initial values
                    self.last_left_wheel_pos = self.true_left_wheel_pos + random.gauss(0.0, self.left_wheel_noise_std)
                    self.last_right_wheel_pos = self.true_right_wheel_pos + random.gauss(0.0, self.right_wheel_noise_std)
                self.first_update = False
                
        except ValueError:
            self.get_logger().warn('Could not find wheel joints in joint states', once=True)
    
    def add_wheel_noise(self):
        """Add Gaussian noise to wheel positions"""
        if not self.enable_noise:
            self.noisy_left_wheel_pos = self.true_left_wheel_pos
            self.noisy_right_wheel_pos = self.true_right_wheel_pos
            return
        
        # Add Gaussian noise to wheel positions
        self.noisy_left_wheel_pos = self.true_left_wheel_pos + random.gauss(0.0, self.left_wheel_noise_std)
        self.noisy_right_wheel_pos = self.true_right_wheel_pos + random.gauss(0.0, self.right_wheel_noise_std)
    
    def update_odometry(self):
        """Calculate odometry from wheel encoder readings"""
        current_time = self.get_clock().now()
        dt = (current_time - self.last_time).nanoseconds / 1e9
        
        if dt <= 0.0:
            return
        
        # Add noise to current wheel positions
        self.add_wheel_noise()
        
        # Calculate wheel deltas
        if self.error_propagation_mode == 0:
            # Non-accumulative mode: delta = (current_noisy - previous_true)
            delta_left = self.noisy_left_wheel_pos - self.last_left_wheel_pos
            delta_right = self.noisy_right_wheel_pos - self.last_right_wheel_pos
        else:
            # Accumulative mode: delta = (current_noisy - previous_noisy)
            delta_left = self.noisy_left_wheel_pos - self.last_left_wheel_pos
            delta_right = self.noisy_right_wheel_pos - self.last_right_wheel_pos
        
        # Calculate linear distances (meters)
        delta_left_m = delta_left * self.wheel_radius
        delta_right_m = delta_right * self.wheel_radius
        
        # Calculate linear and angular displacements
        delta_distance = (delta_right_m + delta_left_m) / 2.0
        delta_theta = (delta_right_m - delta_left_m) / self.wheel_separation
        
        # Update true pose (from true wheel positions, for reference)
        true_delta_left = self.true_left_wheel_pos - self.last_left_wheel_pos
        true_delta_right = self.true_right_wheel_pos - self.last_right_wheel_pos
        true_delta_left_m = true_delta_left * self.wheel_radius
        true_delta_right_m = true_delta_right * self.wheel_radius
        true_delta_distance = (true_delta_right_m + true_delta_left_m) / 2.0
        true_delta_theta = (true_delta_right_m - true_delta_left_m) / self.wheel_separation
        
        # Update true position (for debugging/comparison)
        self.x_true += true_delta_distance * math.cos(self.theta_true + true_delta_theta / 2.0)
        self.y_true += true_delta_distance * math.sin(self.theta_true + true_delta_theta / 2.0)
        self.theta_true += true_delta_theta
        self.theta_true = math.atan2(math.sin(self.theta_true), math.cos(self.theta_true))
        
        # Update noisy position (what we actually publish)
        self.x_noisy += delta_distance * math.cos(self.theta_noisy + delta_theta / 2.0)
        self.y_noisy += delta_distance * math.sin(self.theta_noisy + delta_theta / 2.0)
        self.theta_noisy += delta_theta
        self.theta_noisy = math.atan2(math.sin(self.theta_noisy), math.cos(self.theta_noisy))
        
        # Calculate velocities
        self.vx = delta_distance / dt
        self.vtheta = delta_theta / dt
        
        # Update last positions based on propagation mode
        if self.error_propagation_mode == 0:
            # Non-accumulative: use true values for next iteration
            self.last_left_wheel_pos = self.true_left_wheel_pos
            self.last_right_wheel_pos = self.true_right_wheel_pos
        else:
            # Accumulative: use noisy values for next iteration
            self.last_left_wheel_pos = self.noisy_left_wheel_pos
            self.last_right_wheel_pos = self.noisy_right_wheel_pos
        
        # Publish noisy odometry message
        self.publish_odometry_message(current_time)
        
        # Debug logging (optional)
        # if random.random() < 0.01:  # Log ~1% of updates
        #     self.get_logger().info(f'True: ({self.x_true:.3f}, {self.y_true:.3f}, {math.degrees(self.theta_true):.2f}°) | '
        #                           f'Noisy: ({self.x_noisy:.3f}, {self.y_noisy:.3f}, {math.degrees(self.theta_noisy):.2f}°)')
        
        self.last_time = current_time
    
    def publish_odometry_message(self, current_time):
        """Publish odometry message with noisy values"""
        odom_msg = Odometry()
        
        odom_msg.header.stamp = current_time.to_msg()
        odom_msg.header.frame_id = self.odom_frame_id
        odom_msg.child_frame_id = self.base_frame_id
        
        # Set position (using noisy values)
        odom_msg.pose.pose.position.x = self.x_noisy
        odom_msg.pose.pose.position.y = self.y_noisy
        odom_msg.pose.pose.position.z = 0.0
        
        # Convert yaw to quaternion
        q = self.yaw_to_quaternion(self.theta_noisy)
        odom_msg.pose.pose.orientation.x = q[0]
        odom_msg.pose.pose.orientation.y = q[1]
        odom_msg.pose.pose.orientation.z = q[2]
        odom_msg.pose.pose.orientation.w = q[3]
        
        # Set covariance based on noise level
        if self.enable_noise:
            # Calculate approximate position variance from wheel noise
            # This is a simplified model - actual error propagation would be more complex
            position_variance = (self.left_wheel_noise_std**2 + self.right_wheel_noise_std**2) * self.wheel_radius**2
            orientation_variance = (self.left_wheel_noise_std**2 + self.right_wheel_noise_std**2) * (self.wheel_radius**2 / self.wheel_separation**2)
            
            odom_msg.pose.covariance[0] = position_variance  # x
            odom_msg.pose.covariance[7] = position_variance  # y
            odom_msg.pose.covariance[35] = orientation_variance  # yaw
        else:
            odom_msg.pose.covariance[0] = 0.001  # x
            odom_msg.pose.covariance[7] = 0.001  # y
            odom_msg.pose.covariance[35] = 0.001  # yaw
        
        # Set velocities
        odom_msg.twist.twist.linear.x = self.vx
        odom_msg.twist.twist.linear.y = 0.0
        odom_msg.twist.twist.angular.z = self.vtheta
        
        # Set velocity covariance
        velocity_variance = (self.left_wheel_noise_std**2 + self.right_wheel_noise_std**2) * (self.wheel_radius**2) / (self.last_time.nanoseconds/1e9)**2
        angular_velocity_variance = velocity_variance / (self.wheel_separation**2)
        
        odom_msg.twist.covariance[0] = velocity_variance if self.enable_noise else 0.001
        odom_msg.twist.covariance[35] = angular_velocity_variance if self.enable_noise else 0.001
        
        self.odom_pub.publish(odom_msg)
    
    def yaw_to_quaternion(self, yaw):
        """Convert yaw angle to quaternion"""
        return [
            0.0,
            0.0,
            math.sin(yaw / 2.0),
            math.cos(yaw / 2.0)
        ]

def main(args=None):
    rclpy.init(args=args)
    node = WheelOdometryNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

