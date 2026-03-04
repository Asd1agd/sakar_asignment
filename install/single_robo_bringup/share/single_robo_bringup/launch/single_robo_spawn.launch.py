from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription, RegisterEventHandler, TimerAction
from launch.event_handlers import OnProcessStart
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Path to various package directories
    single_robo_discription_pkg = FindPackageShare('single_robo_discription')
    
    # Path to parameter file
    param_file_path = PathJoinSubstitution([
        single_robo_discription_pkg,
        'config',
        'ps4_config.yaml'
    ])

    rviz_config_path = PathJoinSubstitution([
        single_robo_discription_pkg,
        'config',
        'rviz_config.rviz'
    ])

    # print(param_file_path) 
    # print(rviz_config_path)

    # 1. Launch Gazebo spawn
    gazebo_spawn_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                single_robo_discription_pkg,
                'launch',
                'spawn_gazebo.launch.py'
            ])
        ])
    )
    
    # 6. joy_node
    joy_node = Node(
        package='joy',
        executable='joy_node',
        name='joy_node',
        output='screen'
    )
    
    # 7. teleop_twist_joy node with parameter file
    teleop_node = Node(
        package='teleop_twist_joy',
        executable='teleop_node',
        name='teleop_twist_joy_node',
        # arguments=['--ros-args', '--params-file', param_file_path],
        output='screen',
        parameters=[param_file_path]
    )
    
    # 8. rviz2 - using Node instead of ExecuteProcess
    rviz2_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_path],  # Optional: load specific config
        output='screen'
    )


    # Create launch description
    ld = LaunchDescription()
    
    # Add gazebo spawn first
    ld.add_action(gazebo_spawn_launch)

    # Add joystick control nodes
    ld.add_action(joy_node)
    ld.add_action(teleop_node)
    
    # # Add delayed rviz2
    # ld.add_action(TimerAction(
    #     period=10.0,
    #     actions=[rviz2_node]
    # ))
    
    return ld

