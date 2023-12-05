source /opt/ros/humber/setup.zsh
colcon build --packages-up-to argus_gazebo
cd install
source local_setup.zsh
ros2 launch argus_gazebo load_urdf_into_gazebo.launch.py
ros2 topic list
ros2 topic pub /orbbec_hunter2/cmd_vel geometry_msgs/msg/Twist "{linear:{x: 2.0, y: 0.0,z: 0.0}, angular:{x: 0.0,y:  0.0, z: 0.5}}"
