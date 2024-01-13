#! /usr/bin/env python3
"""
module: node_b

Python module for the second assignment of Research Track I course
   
description:

This node return the last desired target of a robot
    
"""

import rospy
from assignment_2_2023.srv import GetLastTarget
from assignment_2_2023.msg import RobotMsg
from nav_msgs.msg import Odometry

last_target = None  # Variable to store the last target coordinates

def get_last_target(request):
    """
    Callback function for the service. It returns the coordinates of the last target sent by the user.
    """
    global last_target
    response = RobotMsg()
    
    if last_target is not None:
        response.x = last_target[0]
        response.y = last_target[1]
        rospy.loginfo("Returning the last target coordinates: (%f, %f)", response.x, response.y)
    else:
        rospy.logwarn("No target has been set yet.")
    
    return response

def callback(msg):
    """
    Callback function to update the last_target variable whenever a new target is set.
    """
    global last_target
    last_target = (msg.pose.pose.position.x, msg.pose.pose.position.y)

if __name__ == '__main__':
    rospy.init_node("last_target_service_node")
    
    # Define a service to get the last target coordinates
    rospy.Service('get_last_target', GetLastTarget, get_last_target)
    
    # Define a subscriber to the Odometry message and call the callback function
    rospy.Subscriber("/odom", Odometry, callback)
    
    rospy.loginfo("Last Target Service Node has started.")
    
    # Spin to keep the node running
    rospy.spin()
