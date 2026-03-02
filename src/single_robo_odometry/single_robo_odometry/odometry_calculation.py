#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.duration import Duration
from sensor_msgs.msg import JointState
from nav_msgs.msg import Odometry
import math

class WheelOdometryNode(Node):
    def __init__(self):
        super().__init__('wheel_odometry_node')
        
        # Parameters (adjust these for your robot)
        self.declare_parameter('wheel_radius', 0.1)  # in meters
        self.declare_parameter('wheel_separation', 0.425)  # in meters
        self.declare_parameter('odom_frame_id', 'odom')
        self.declare_parameter('base_frame_id', 'base_footprint_calculated')
        self.declare_parameter('publish_rate', 50.0)  # Hz
        
        # Get parameters
        self.wheel_radius = self.get_parameter('wheel_radius').value
        self.wheel_separation = self.get_parameter('wheel_separation').value
        self.odom_frame_id = self.get_parameter('odom_frame_id').value
        self.base_frame_id = self.get_parameter('base_frame_id').value
        publish_rate = self.get_parameter('publish_rate').value
        
        # State variables
        self.left_wheel_pos = 0.0
        self.right_wheel_pos = 0.0
        self.last_left_wheel_pos = 0.0
        self.last_right_wheel_pos = 0.0
        
        # Robot pose
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        
        # Robot velocities
        self.vx = 0.0
        self.vy = 0.0
        self.vtheta = 0.0
        
        # Time tracking
        self.last_time = self.get_clock().now()
        self.last_joint_state_time = self.get_clock().now()
        
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
            '/odom_calculated',
            10
        )
        
        # Timer for regular publishing
        self.timer = self.create_timer(1.0/publish_rate, self.update_odometry)
        
        self.get_logger().info(f'Wheel Odometry Node started with:')
        self.get_logger().info(f'  Wheel radius: {self.wheel_radius} m')
        self.get_logger().info(f'  Wheel separation: {self.wheel_separation} m')
        self.get_logger().info(f'  Odom frame: {self.odom_frame_id}')
        self.get_logger().info(f'  Base frame: {self.base_frame_id}')
        
    def joint_state_callback(self, msg):
        """Callback for joint states topic"""
        try:
            # Find left and right wheel indices
            left_idx = msg.name.index('base_left_wheel_joint')
            right_idx = msg.name.index('base_right_wheel_joint')
            
            # Update wheel positions (in radians)
            self.left_wheel_pos = msg.position[left_idx]
            self.right_wheel_pos = msg.position[right_idx]
            
            # Store the timestamp
            self.last_joint_state_time = self.get_clock().now()
            
            # If this is the first reading, initialize last positions
            if self.last_left_wheel_pos == 0.0 and self.last_right_wheel_pos == 0.0:
                self.last_left_wheel_pos = self.left_wheel_pos
                self.last_right_wheel_pos = self.right_wheel_pos
                
        except ValueError as e:
            self.get_logger().warn(f'Could not find wheel joints in joint states: {e}')
        except Exception as e:
            self.get_logger().error(f'Error processing joint states: {e}')
    
    def update_odometry(self):
        """Calculate odometry from wheel encoder readings"""
        current_time = self.get_clock().now()
        dt = (current_time - self.last_time).nanoseconds / 1e9
        
        # Skip if no time has passed
        if dt <= 0.0:
            return
        
        # Calculate wheel movements (in radians)
        delta_left = self.left_wheel_pos - self.last_left_wheel_pos
        delta_right = self.right_wheel_pos - self.last_right_wheel_pos
        
        # Convert to linear distances (meters)
        delta_left_m = delta_left * self.wheel_radius
        delta_right_m = delta_right * self.wheel_radius
        
        # Calculate linear and angular displacements
        delta_distance = (delta_right_m + delta_left_m) / 2.0
        delta_theta = (delta_right_m - delta_left_m) / self.wheel_separation
        
        # Update pose if there was movement
        if abs(delta_left) > 0.0 or abs(delta_right) > 0.0:
            # Calculate velocities
            self.vx = delta_distance / dt
            self.vtheta = delta_theta / dt
            
            # Update position (using bicycle model)
            self.x += delta_distance * math.cos(self.theta + delta_theta / 2.0)
            self.y += delta_distance * math.sin(self.theta + delta_theta / 2.0)
            self.theta += delta_theta
            
            # Normalize theta to [-pi, pi]
            self.theta = math.atan2(math.sin(self.theta), math.cos(self.theta))
            
            # Update last positions
            self.last_left_wheel_pos = self.left_wheel_pos
            self.last_right_wheel_pos = self.right_wheel_pos
            
            # Publish odometry message
            self.publish_odometry_message(current_time)
        
        self.last_time = current_time
    
    def publish_odometry_message(self, current_time):
        """Publish odometry message"""
        odom_msg = Odometry()
        
        odom_msg.header.stamp = current_time.to_msg()
        odom_msg.header.frame_id = self.odom_frame_id
        odom_msg.child_frame_id = self.base_frame_id
        
        # Set position
        odom_msg.pose.pose.position.x = self.x
        odom_msg.pose.pose.position.y = self.y
        odom_msg.pose.pose.position.z = 0.0
        
        # Convert yaw to quaternion
        q = self.yaw_to_quaternion(self.theta)
        odom_msg.pose.pose.orientation.x = q[0]
        odom_msg.pose.pose.orientation.y = q[1]
        odom_msg.pose.pose.orientation.z = q[2]
        odom_msg.pose.pose.orientation.w = q[3]
        
        # Set covariance (adjust these values based on your robot's accuracy)
        odom_msg.pose.covariance[0] = 0.1  # x
        odom_msg.pose.covariance[7] = 0.1  # y
        odom_msg.pose.covariance[35] = 0.1  # yaw
        
        # Set velocities
        odom_msg.twist.twist.linear.x = self.vx
        odom_msg.twist.twist.linear.y = 0.0
        odom_msg.twist.twist.angular.z = self.vtheta
        
        # Set velocity covariance
        odom_msg.twist.covariance[0] = 0.1  # linear x
        odom_msg.twist.covariance[35] = 0.1  # angular z
        
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