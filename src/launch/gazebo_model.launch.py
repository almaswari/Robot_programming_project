import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    pkg_name = 'quadrotor_sim'
    
    # Process Xacro
    xacro_file = os.path.join(get_package_share_directory(pkg_name), 'model', 'robot.xacro')
    robot_description = xacro.process_file(xacro_file).toxml()

    # Gazebo Launch
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')]),
        launch_arguments={'gz_args': '-r -v 4 empty.sdf'}.items()
    )

    # Spawn Drone
    spawn_node = Node(
        package='ros_gz_sim', executable='create',
        arguments=['-name', 'quadrotor', '-topic', 'robot_description', '-z', '0.2'],
        output='screen'
    )

    # Robot State Publisher
    robot_state_pub = Node(
        package='robot_state_publisher', executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description, 'use_sim_time': True}]
    )

    # ROS-GZ Bridge
    bridge_params = os.path.join(get_package_share_directory(pkg_name), 'parameters', 'bridge_parameters.yaml')
    bridge_node = Node(
        package='ros_gz_bridge', executable='parameter_bridge',
        arguments=['--ros-args', '-p', f'config_file:={bridge_params}']
    )

    return LaunchDescription([gazebo, spawn_node, robot_state_pub, bridge_node])