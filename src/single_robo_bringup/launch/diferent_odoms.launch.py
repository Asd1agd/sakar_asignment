from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription, RegisterEventHandler, TimerAction
from launch.event_handlers import OnProcessStart
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Path to various package directories
    single_robo_odometry_pkg = FindPackageShare('single_robo_odometry')
    
    # 2. odom_tf_pub node
    odom_tf_pub_node = Node(
        package='single_robo_odometry',
        executable='odom_tf_pub',
        name='odom_tf_pub',
        output='screen'
    )
    
    # 3. odometry_calculation node
    odometry_calculation_node = Node(
        package='single_robo_odometry',
        executable='odometry_calculation',
        name='odometry_calculation',
        output='screen'
    )
    
    # 4. odom_tf_pub_w_error node
    odom_tf_pub_w_error_node = Node(
        package='single_robo_odometry',
        executable='odom_tf_pub_w_error',
        name='odom_tf_pub_w_error',
        output='screen'
    )
    
    # 5. odometry_error node
    odometry_error_node = Node(
        package='single_robo_odometry',
        executable='odometry_error',
        name='odometry_error',
        output='screen'
    )

    # Create launch description
    ld = LaunchDescription()
     
    # Add odometry nodes
     # Phase 2: Wait for Gazebo, then start robot nodes
    ld.add_action(TimerAction(
        period=5.0,
        actions=[
            odom_tf_pub_node,
            odometry_calculation_node,
            odom_tf_pub_w_error_node,
            odometry_error_node
        ]
    ))

    return ld

