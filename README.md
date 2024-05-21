Research Track I - Second Assignment
======================================
ROS Robot Simulator using Gazebo - Parisa Farvardin (S6101141)
=======================================================================================

Project Description
----------------------

It is the purpose of this assignment to develop a ROS package containing three ROS nodes that provide a way to interact with the environment in Gazebo. 

The aim of the assignment is to create a package, in which the following nodes will be developed:
- `Node A`: A node that implements an action client, allowing the user to set a target (x, y), cancel it, and exit the program if necessary. The node also publishes the robot position and velocity as a custom message (x, y, vel_x, vel_z), by relying on the values published on the topic /odom;
- `Node B`: A service node that, when called, returns the coordinates of the last target sent by the user;
- `Node C`: A node that subscribes to the robot's position and velocity (using the custom message) and implements a server to retrieve the distance of the robot from the target and the robot's average speed.

Then, it is asked to create a launch file to start the whole simulation.

How to Install and Run the project
--------------------------------
The simulator requires a ROS installation, then to have this project, it is required to clone the project from this repository using this line:

```bash
$ git clone https://github.com/PariFarv/ResearchTrack1_Assignment2.git
```
After cloning, you need to create your workspace in ROS. To do so, a small modification in `bashrc` file is needed. You should add this line in the `bashrc` file:
```bash
source ~/your own directory/devel/setup.bash
```
Now for having the new package which is `assignment_2_2023` you should introduce it to the ROS by writing this line in the terminal while you are in the workspace directory:
```bash
$ catkin_create_pkg <your package name>
```
And then a catkin command in the workspace directory is needed:
```bash
$ catkin_make
```
Finally to run the project, first you should run the `launch` file and then for having the node_c open another window and run this node separately:
```bash
$ roslaunch assignment_2_2023 assignment1.launch
```
```
$ rosrun assignment_2_2023 node_c.py
```

Code
-------------------------
### node_a ###
This piece of code is provided to receive coordinate inputs x and y from the user by entering the number `1` and setting these coordinates a target for the robot to reach. And then by entering number `2` the mission of reaching the location is going to be canceled. Finally by entering `3` you would exit from the program.

### node_b ###
This piece of code is provided to return the last coordinates that user-defined for the robot to reach that. A service in this code returns the first target position when it is called.

### node_c ###
This piece of code is provided to return the distance between the target position and the actual position of the robot, the velocity of the robot, and calculate the average velocity.

Node_a pseudo code
-----------------------
Initialize ROS node "node_a"

1. Define a global publisher "/pos_vel" for RobotMsg custom message

2. Define a subscriber for "/odom" topic, listening to Odometry messages, and set the callback function to "callback"

Create a new action client for "/reaching_goal" with the action type PlanningAction
Wait for the action server to be ready to receive goals

Call the UI function "user_action"

3. Define a callback function "callback" that takes an Odometry message as input:
    Create a RobotMsg custom message
    Set the position and linear velocity of the robot using data from the Odometry message
    Publish the RobotMsg on the "/pos_vel" topic

4. Define a function "set_target" to collect user input for a target position:
    Get x and y coordinates from the user
    Print the selected coordinates
    Create a goal message with the target coordinates
    Send the goal to the action server
    Print a success message
    Call the UI function "user_action"

5. Define a function "user_action" to present a menu to the user:
    Display a guide for controlling the robot
    Ask the user to select a mission (1 for setting a target, 2 for canceling, 3 for exiting)
    Based on the user's choice:
        - If 1, set a target using "set_target"
        - If 2, cancel the goal and print a success message, then call "user_action" again
        - If 3, print an exit message and exit the program
        - Otherwise, print an error message and call "user_action" again

6. If the script is executed directly:
    Initialize the ROS node
    Subscribe to the "/odom" topic and publish on "/pos_vel"
    Create an action client and wait for the server to be ready
    Call the "user_action" function to start the user interface

Run with Jupyter Notebook
--------------------------------
In order to run the project from Jupyter Notebook, first it is mandatory to modify the "launch" file so that node_a, node_b, and node_c have to be deleted from the file.
Then in the terminal run the launch file:
```bash
$ roslaunch assignment_2_2023 assignment1.launch
```
Now it is time to run the Jupyter Notebook using this command in the terminal:
```bash
$ jupyter notebook --allow-root --ip 0.0.0.0
```
After all, it should run the code from Jupyter Notebook and control the robot. After running the code, the visualized part will appear in Jupyter, making it possible to select the position and set or cancel the goal. Moreover, a graph for recording how many times it has been reached or canceled can be seen and a live plot in order to follow the route is provided.

