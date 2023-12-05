## 说  明：

本工程是一个完整的从solidworks中将一个三维模型通过插件sw2urdf将其转换为urdf文件，并通过若干修改后，最后成功在gazebo中进行阿克曼底盘仿真驱动。

三维模型文件存放在solidworks文件夹，rn2301_3d_20231016_asm.SLDASM需要用Solidworks2020版本，然后需要下载对应的SW2URDF插件，本工程采用的是[v1.6.0 (SolidWorks 2020)](https://github.com/ros/solidworks_urdf_exporter/releases/tag/1.6.0)。在solidworks中如何添加相关参考几何体，可以参考B站视频：https://www.bilibili.com/video/BV1Tx411o7rH/?spm_id_from=333.337.search-card.all.click&vd_source=5f11e9196e87fd56a0b5843d68ab6b65。本工程需要的ROS2版本为：foxy或humble。

如何编译运行参看：`cmd.sh`

对于urdf文件夹中的文件命令相关说明如下：

**autocar_urdf_from_sw2urdf.urdf**：初次从solidworks经过SW2URDF文件转出的urdf文件。

**autocar_urdf_ackermann_step0.xacro**：在autocar_urdf_from_sw2urdf.urdf基础上添加一些gazebo插件。

**autocar_urdf_ackermann_step1.xacro**：在autocar_urdf_ackermann_step0.xacro基础上修改mesh文件路径，修改一些link名字，添加libgazebo_ros_ackermann_drive插件。

**autocar_urdf_ackermann.xacro**：在autocar_urdf_ackermann_step1.xacro基础上，添加一些虚拟根节点link，修改一些link中的inertial中极小的异常值，添加steering以及steering_joint等。

**autocar_urdf_ackermann.urdf**：通过 xacro autocar_urdf_ackermann.xacro > autocar_urdf_ackermann.urdf获取，用于在RViz中显示。





