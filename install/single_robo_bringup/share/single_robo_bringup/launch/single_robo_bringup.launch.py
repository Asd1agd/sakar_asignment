import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, TimerAction
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    single_robo_bringup_pkg = get_package_share_directory('single_robo_bringup')
    
    # RViz config path
    rviz_config_path = os.path.join(
        single_robo_bringup_pkg,
        'config',
        'rviz_map_config.rviz'  # Changed to amcl.rviz for clarity
    )

    use_sim_time_arg = DeclareLaunchArgument(
        "use_sim_time",
        default_value="true",
        description="Use simulation time"
    )

    use_sim_time = LaunchConfiguration("use_sim_time")

    # 1. Launch Gazebo spawn
    spawn_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                single_robo_bringup_pkg,
                'launch',
                'single_robo_spawn.launch.py'
            ])
        ])
    )

    # 2. Launch navigation and mapping
    nav_map_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                single_robo_bringup_pkg,
                'launch',
                'single_robo_nav_map.launch.py'
            ])
        ])
    )

    # 2. Launch navigation and mapping
    nav2_stack_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                single_robo_bringup_pkg,
                'launch',
                'single_robo_navigation.launch.py'
            ])
        ])
    )

    # RViz2 node
    rviz2_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_path],
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}]
    )

    # Create launch description
    ld = LaunchDescription()
    ld.add_action(use_sim_time_arg)
    ld.add_action(spawn_launch)
    ld.add_action(nav_map_launch)
    ld.add_action(nav2_stack_launch)

    # 4. RViz2 (start after everything is ready)
    ld.add_action(TimerAction(
        period=10.0,
        actions=[rviz2_node]
    ))

    return ld