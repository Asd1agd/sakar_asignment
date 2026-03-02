#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped, Quaternion
from tf2_ros import TransformBroadcaster
import math

class OdometryTfPublisher(Node):
    def __init__(self):
        super().__init__('odometry_tf_publisher')
        
        # Parameters
        self.declare_parameter('odom_frame', 'odom_calculated')
        self.declare_parameter('base_frame', 'base_footprint')
        self.declare_parameter('publish_rate', 50.0)
        self.declare_parameter('warning_threshold', 0.5)
        self.declare_parameter('invert_transform', True)  # New parameter
        
        # Get parameters
        self.odom_frame = self.get_parameter('odom_frame').value
        self.base_frame = self.get_parameter('base_frame').value
        publish_rate = self.get_parameter('publish_rate').value
        self.warning_threshold = self.get_parameter('warning_threshold').value
        self.invert_transform = self.get_parameter('invert_transform').value
        
        # Store latest odometry data
        self.latest_odom = None
        self.latest_odom_time = self.get_clock().now()
        self.warned_old_data = False
        
        # TF Broadcaster
        self.tf_broadcaster = TransformBroadcaster(self)
        
        # Subscriber to odometry
        self.odom_sub = self.create_subscription(
            Odometry,
            '/odom_calculated',
            self.odom_callback,
            10
        )
        
        # Timer for publishing TF even if odometry updates are slow
        self.timer = self.create_timer(1.0/publish_rate, self.publish_tf)
        
        if self.invert_transform:
            self.get_logger().info(f'Odometry TF Publisher started (INVERTED MODE)')
            self.get_logger().info(f'  Parent frame: {self.base_frame}')
            self.get_logger().info(f'  Child frame: {self.odom_frame}')
        else:
            self.get_logger().info(f'Odometry TF Publisher started (NORMAL MODE)')
            self.get_logger().info(f'  Parent frame: {self.odom_frame}')
            self.get_logger().info(f'  Child frame: {self.base_frame}')
            
        self.get_logger().info(f'  Subscribed to: /odom_calculated')
        
    def odom_callback(self, msg):
        """Callback for odometry messages"""
        self.latest_odom = msg
        self.latest_odom_time = self.get_clock().now()
        self.warned_old_data = False
        
        # Publish TF immediately when new odometry arrives
        self.publish_tf_from_odom(msg)
    
    def publish_tf(self):
        """Publish TF transform based on latest odometry (timer callback)"""
        if self.latest_odom is None:
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
    
    def invert_pose(self, position, orientation):
        """Invert a pose (position + quaternion)"""
        # For a unit quaternion, inverse is conjugate: [ -x, -y, -z, w ]
        q_inv = Quaternion()
        q_inv.x = -orientation.x
        q_inv.y = -orientation.y
        q_inv.z = -orientation.z
        q_inv.w = orientation.w
        
        # For position: p_inv = - (q_inv * p * q)
        # Using simplified approach for common case where orientation is mostly around Z
        # For full 3D, we'd need proper quaternion rotation
        
        # Since odometry is typically 2D (x, y, yaw), we can use 2D inversion
        # For full 3D, use the quaternion_rotate_vector method below
        
        # Get yaw from quaternion
        yaw = math.atan2(2.0 * (orientation.w * orientation.z + orientation.x * orientation.y),
                        1.0 - 2.0 * (orientation.y * orientation.y + orientation.z * orientation.z))
        
        # Invert 2D transform
        cos_yaw = math.cos(yaw)
        sin_yaw = math.sin(yaw)
        
        # p_inv = -R^T * p
        x_inv = -(position.x * cos_yaw + position.y * sin_yaw)
        y_inv = -(-position.x * sin_yaw + position.y * cos_yaw)
        
        return (x_inv, y_inv, 0.0), q_inv
    
    def quaternion_rotate_vector(self, q, v):
        """Rotate vector v by quaternion q"""
        # Extract vector and scalar parts
        u = [q.x, q.y, q.z]
        s = q.w
        
        # Formula: v_rot = v + 2.0 * cross(u, cross(u, v) + s * v)
        # cross(u, v)
        cross1 = [
            u[1] * v[2] - u[2] * v[1],
            u[2] * v[0] - u[0] * v[2],
            u[0] * v[1] - u[1] * v[0]
        ]
        
        # cross(u, v) + s * v
        temp = [
            cross1[0] + s * v[0],
            cross1[1] + s * v[1],
            cross1[2] + s * v[2]
        ]
        
        # cross(u, temp)
        cross2 = [
            u[1] * temp[2] - u[2] * temp[1],
            u[2] * temp[0] - u[0] * temp[2],
            u[0] * temp[1] - u[1] * temp[0]
        ]
        
        # v_rot = v + 2.0 * cross2
        v_rot = [
            v[0] + 2.0 * cross2[0],
            v[1] + 2.0 * cross2[1],
            v[2] + 2.0 * cross2[2]
        ]
        
        return v_rot
    
    def publish_tf_from_odom(self, odom_msg):
        """Publish TF immediately from odometry message"""
        try:
            transform = TransformStamped()
            
            # Use current time instead of odometry stamp for TF consistency
            current_time = self.get_clock().now()
            transform.header.stamp = current_time.to_msg()
            
            if self.invert_transform:
                # INVERTED: base_footprint -> odom_calculated
                transform.header.frame_id = self.base_frame  # Parent: base_footprint
                transform.child_frame_id = self.odom_frame   # Child: odom_calculated
                
                # Calculate inverse transform
                pos_inv, orient_inv = self.invert_pose(
                    odom_msg.pose.pose.position,
                    odom_msg.pose.pose.orientation
                )
                
                # Set inverted position
                transform.transform.translation.x = pos_inv[0]
                transform.transform.translation.y = pos_inv[1]
                transform.transform.translation.z = pos_inv[2]
                
                # Set inverted orientation
                transform.transform.rotation = orient_inv
            else:
                # NORMAL: odom_calculated -> base_footprint
                transform.header.frame_id = self.odom_frame  # Parent: odom_calculated
                transform.child_frame_id = self.base_frame   # Child: base_footprint
                
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