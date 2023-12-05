import os
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    package_name = 'argus_gazebo'
    xacro_name = "autocar_urdf_ackermann.xacro"
    urdf_name = "autocar_urdf_ackermann.urdf"

    ld = LaunchDescription()
    pkg_share = FindPackageShare(package=package_name).find(package_name) 
    urdf_model_path = os.path.join(pkg_share, f'urdf/{urdf_name}')
    xacro_model_path = os.path.jin(pkg_share, f'urdf/{xacro_fname}')

    cmd = "xacro {} > {}".format(xacro_model_path, urdf_model_path)
    print(cmd)
    os.system(cmd)

    default_rviz_config_path = os.path.join(pkg_share ,'rviz/urdf.rviz')

    robot_description = ParameterValue(Command(['xacro ', xacro_model_path]),
                                       value_type=str)
    
    rviz_arg = DeclareLaunchArgument(name='rvizconfig', default_value=str(default_rviz_config_path),
                                     description='Absolute path to rviz config file')
    
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}]
        )

    joint_state_publisher_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        arguments=[urdf_model_path]
        )
    rviz2_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', LaunchConfiguration('rvizconfig')],
        )
    ld.add_action(rviz_arg)
    ld.add_action(joint_state_publisher_node)
    ld.add_action(robot_state_publisher_node)
    ld.add_action(rviz2_node)
    return ld
