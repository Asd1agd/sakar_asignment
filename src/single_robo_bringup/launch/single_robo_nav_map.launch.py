from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, TimerAction
from launch.conditions import LaunchConfigurationEquals
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, TextSubstitution
from launch_ros.actions import Node, LifecycleNode
from launch_ros.substitutions import FindPackageShare
import os
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Get package directories
    single_robo_discription_pkg = get_package_share_directory('single_robo_discription')
    single_robo_bringup_pkg = get_package_share_directory('single_robo_bringup')
    
    # Path to your costmap configuration
    params_file = os.path.join(
        single_robo_bringup_pkg,
        'config',
        'costmap.yaml'
    )
    
    # RViz config path
    rviz_config_path = os.path.join(
        single_robo_bringup_pkg,
        'config',
        'rviz_map_config.rviz'  # Changed to amcl.rviz for clarity
    )
    
    # Declare launch arguments
    map_name_arg = DeclareLaunchArgument(
        "map_name",
        default_value="small_warehouse",
        description="Name of the map to load"
    )
    
    use_sim_time_arg = DeclareLaunchArgument(
        "use_sim_time",
        default_value="true",
        description="Use simulation time"
    )
    
    amcl_config_arg = DeclareLaunchArgument(
        "amcl_config",
        default_value=os.path.join(
            single_robo_bringup_pkg,
            "config",
            "amcl.yaml"
        ),
        description="Full path to AMCL yaml config file"
    )

    
    # Get launch argument values
    map_name = LaunchConfiguration("map_name")
    use_sim_time = LaunchConfiguration("use_sim_time")
    amcl_config = LaunchConfiguration("amcl_config")
    
    # Map path - using TextSubstitution to handle LaunchConfiguration properly
    map_path = PathJoinSubstitution([
        TextSubstitution(text=single_robo_discription_pkg),
        "maps",
        map_name,  # This is now a LaunchConfiguration
        "my_map.yaml"  # Changed to standard naming convention
    ])
    
    # Map Server node
    map_server_node = Node(
        package="nav2_map_server",
        executable="map_server",
        name="map_server",
        output="screen",
        parameters=[
            {"yaml_filename": map_path},
            {"use_sim_time": use_sim_time}
        ],
        remappings=[("/tf", "tf"), ("/tf_static", "tf_static")]
    )
    
    # AMCL node
    amcl_node = Node(
        package="nav2_amcl",
        executable="amcl",
        name="amcl",
        output="screen",
        parameters=[
            amcl_config,
            {"use_sim_time": use_sim_time},
        ],
        remappings=[
            ("scan", "/scan"),  # Make sure this matches your laser topic
            ("tf", "tf"),
            ("tf_static", "tf_static")
        ]
    )

     # Create the node action
    costmap_node = Node(
        package='nav2_costmap_2d',
        executable='nav2_costmap_2d',
        name='nav2_costmap_2d',
        output='screen',
        parameters=[params_file],
        # Optional: add namespace if needed
        # namespace='',
        # Optional: add remappings if needed
        # remappings=[
        #     ('/tf', 'tf'),
        #     ('/tf_static', 'tf_static')
        # ]
    )
    
    # Lifecycle Manager - FIXED: Use correct node names
    lifecycle_manager = Node(
        package="nav2_lifecycle_manager",
        executable="lifecycle_manager",
        name="lifecycle_manager_localization",
        output="screen",
        parameters=[
            {
                "node_names": ["map_server", "amcl"], #"costmap/costmap"],
                "autostart": True,
                "use_sim_time": use_sim_time
            }
        ]
    )
    
    # RViz2 node
    rviz2_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_path],
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
        condition=LaunchConfigurationEquals('use_rviz', 'true')
    )
    
    # Optional: Add transform publisher for robot localization
    # This publishes the transform from map to odom (AMCL will provide this)
    
    # Create launch description
    ld = LaunchDescription()
    
    # Add launch arguments
    ld.add_action(map_name_arg)
    ld.add_action(use_sim_time_arg)
    ld.add_action(amcl_config_arg)
    
    # Add nodes in proper order
    # 1. Map server
    ld.add_action(map_server_node)
    
    # 2. AMCL (start after map server)
    ld.add_action(TimerAction(
        period=2.0,
        actions=[amcl_node]
    ))

    # ld.add_action(TimerAction(
    #     period=2.0,
    #     actions=[costmap_node]
    # ))

    # ld.add_action(costmap_node)

    # 3. Lifecycle manager (start after both nodes)
    ld.add_action(TimerAction(
        period=3.0,
        actions=[lifecycle_manager]
    ))
    
    # # 4. RViz2 (start after everything is ready)
    # ld.add_action(TimerAction(
    #     period=16.0,
    #     actions=[rviz2_node]
    # ))
    
    return ld