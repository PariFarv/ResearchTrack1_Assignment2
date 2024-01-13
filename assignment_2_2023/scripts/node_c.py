#! /usr/bin/env python3

"""
module: node_c

Python module for the second assignment of Research Track I course
   
description:

This node prints the robot speed and the distance from the desired target
    
"""

import rospy
import math
import time

from assignment_2_2023.msg import RobotMsg

# Variable for calculating average velocity
velocities = []
window_size = 10  # Default window size for calculating average velocity

def callback_subscriber(msg):
    """
    Function that calculates the distance between the robot and the goal and the speed of the robot
    
    Args: 
    - msg (RobotMsg): Contains the coordinates and velocity of the robot
    """
    global velocities

    # Get the desired position from the ROS parameter server
    des_x = rospy.get_param("des_pos_x")
    des_y = rospy.get_param("des_pos_y")
    
    # Get the window size for the velocity calculation from the parameter server
    #velocity_window_size = rospy.get_param('/window_size')
    

    # Calculate the distance between the current and the desired position
    distance = math.sqrt(pow(des_x - msg.x, 2) + pow(des_y - msg.y, 2))
        
    # Calculate the velocity   
    vel = math.sqrt(pow(msg.vel_x, 2) + pow(msg.vel_y, 2))
    
    # Add the current velocity to the list
    velocities.append(vel)
    
    if len(velocities) > window_size:
        velocities.pop(0)

    # Calculate the average velocity
    avg_velocity = sum(velocities) / len(velocities)
        
    # Print distance and velocity
    print("Distance to the goal: ", distance)
    print("The velocity: ", vel)  
    print("Average speed: ", avg_velocity)

if __name__ == '__main__':
    
    # Init the Node
    rospy.init_node("node_c")
    
    # Subscribe to the RobotMsg topic and pass the info to the callback function
    rospy.Subscriber('/pos_vel', RobotMsg, callback_subscriber)
    
    # Keep the node running
    rospy.spin()
