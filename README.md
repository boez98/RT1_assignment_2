# Research Track 1 - Assignment 2

Andrea Bolla - 4482930

# Introduction
In this assignment, I developed, by using **ROS**, three nodes and the lauch file:
- (A) A node that implements an action client, allowing the user to set a target (x, y) or to cancel it. The node also publishes the robot position and velocity as a custom message (x,y, vel_x, vel_z), by relying on the values published on the topic /odom. 
- (B) A service node that, when called, prints the number of goals reached and cancelled;
- (C) A node that subscribes to the robot’s position and velocity (using the custom message) and prints the distance of the robot from the target and the robot’s average speed. Use a parameter to set how fast the node publishes the information.
-  Create a launch file to start the whole simulation. Set the value for the frequency with which node (C) publishes
the information.

# Doxygen Documentation
The project documentation, generated with Doxygen can be found in the following link:

boez98.github.io/RT1_assignment_2/assignment_2_2022/docs/html/files.html.html

# Nodes
There are six nodes in the package:

- `bug_as.py` is the action server node that calls the  services to move the robot to the goal position
- `go_to_point_service.py` is the service node to move the robot to the goal position
- `wall_follow_service.py` is the service node to avoid obstacles

and the other three node implemented by myself

- `ActionClient_nodeA.py` is the action client node, allowing the user to set a target, x and y, or to cancel it. The node also publishes the robot position and velocity as a custom message on the /*pos_and_vel* topic, by relying on the values published on the topic /*odom*. 
- `Number_Goal_rc_nodeB.py` is the service node that, when called, prints the number of goals reached and cancelled 
-  `Dist_Speed_nodeC.py` is the node that subscribes to the robot’s position and velocity from the */pos_and_vel* topic as a custom message and prints the distance of the robot from the target and the robot’s average speed with a frequency setted as a parameter in the lauch file

![rosgraph](https://user-images.githubusercontent.com/107572039/211221770-f5538c04-3884-4336-9099-b9ee421dbd1a.png)

After the program has started, you can interact with four windows:

- **Rviz** is a ROS visualization 
- **Gazebo** is the 3D simulator environment with the obstacles and the robot 
- **ActionClient_nodeA.py** is the window where the user can set the goal position or cancel it from keyboard
- **Dist_Speed_nodeC.py** is the window where distance from target and average speed of the robot are showed

- To know the number of goals reached and canceled, type on another tab:

      rosservice call /n_goal


- You can set the frequency from the launch file `assignment1.launch` inside of the `launch` folder, by changing the value and relaunch the program.

# Installing and Running
-  First of all, you have to install **xterm**:

       sudo apt install xterm

- after that, download my package  `assignment_2_2022 `inside the `src` folder of your ROS workspace

- now run the master by typing:

      roscore 

- from another tab, go to your ROS workspace run the command:

      catkin_make

- to run the code, type the following command:

      roslaunch assignment_2_2022 assignment1.launch



# Improvment
- Improve user interface by being more clear in how set the inputs and give error message if the inputs are wrong
- Improve the node B, distance and average speed are not in real time and are not very accurate
# Flowchart node_A
![Blank diagram.pdf](https://github.com/boez98/RT1_assignment_2/files/10372052/Blank.diagram.pdf)
