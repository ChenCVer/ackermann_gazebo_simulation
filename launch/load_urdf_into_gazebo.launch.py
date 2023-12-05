import os

from ament_index_python.packages import get_package_share_directory

from launch_ros.substitutions import FindPackageShare

from launch import LaunchDescription
# from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():


    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name='argus_gazebo'
    world_file_path = 'worlds/empty_world.model'
    
    pkg_path = os.path.join(get_package_share_directory(package_name))
    pkg_share = FindPackageShare(package=package_name).find(package_name)
    world_path = os.path.join(pkg_path, world_file_path)  

    xacro_name = "autocar_urdf_ackermann.xacro"
    urdf_name = "autocar_urdf_ackermann.urdf"
    urdf_model_path = os.path.join(pkg_share, f'urdf/{urdf_name}')
    xacro_model_path = os.path.join(pkg_share, f'urdf/{xacro_name}')

    cmd = "xacro {} > {}".format(xacro_model_path, urdf_model_path)
    print(cmd)
    os.system(cmd)

    default_rviz_config_path = os.path.join(pkg_share ,'rviz/urdf.rviz')
    robot_description = ParameterValue(Command(['xacro ', urdf_model_path]),
                                       value_type=str)
        
    # Pose where we want to spawn the robot
    spawn_x_val = '0.0'
    spawn_y_val = '0.0'
    spawn_z_val = '0.3593'
    spawn_yaw_val = '0.0'
  
    mbot = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','mbot.launch.py'
                )]), launch_arguments={'use_sim_time': 'true', 'world': world_path,
                 'urdf':urdf_model_path, 'xacro':xacro_model_path, 'pkg_name': package_name}.items()
    )

    # Include the Gazebo launch file, provided by the gazebo_ros package
    start_gazebo_cmd = ExecuteProcess(
        cmd=["gazebo", "--verbose", "-s", "libgazebo_ros_factory.so"], output="screen"
    )

    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'orbbec_hunter2',
                                   '-x', spawn_x_val,
                                   '-y', spawn_y_val,
                                   '-z', spawn_z_val,
                                   '-Y', spawn_yaw_val],
                        output='screen')

    ld = LaunchDescription([mbot, start_gazebo_cmd, spawn_entity])
    return ld
