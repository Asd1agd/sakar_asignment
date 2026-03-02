#!/usr/bin/env python3
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
from launch.actions import TimerAction
import os

def generate_launch_description():
    ld = LaunchDescription()
    
    # 1. Static transform publisher
    static_transform_publisher = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="static_transform_publisher",
        arguments=[
            '--x', '0',
            '--y', '0',
            '--z', '0.1',
            '--qx', '0.0',
            '--qy', '0.0',
            '--qz', '0.0',
            '--qw', '1.0',
            '--frame-id', 'base_footprint_ekf',
            '--child-frame-id', 'imu_link_ekf'
        ],
        output='screen'
    )
    
    # 2. EKF node with 2-second delay
    robot_localization = Node(
        package="robot_localization",
        executable="ekf_node",
        name="ekf_filter_node",
        output="screen",
        parameters=[os.path.join(get_package_share_directory("single_robo_discription"), 
                                "config", "ekf.yaml")],
    )
    
    # 3. IMU republisher
    imu_republisher_py = Node(
        package="single_robo_odometry",
        executable="imu_republisher",
        name='imu_republisher',
        output='screen'
    )
    
    # Add nodes with proper timing
    ld.add_action(static_transform_publisher)
    ld.add_action(imu_republisher_py)
    
    # Add EKF node after 2 seconds
    ld.add_action(TimerAction(
        period=5.0,
        actions=[robot_localization]
    ))
    
    return ld