#! /usr/bin/env python3

"""
module: node_a

Python module for the second assignment of Research Track I

description:
This node implements an action client allowing the user to set a target (x,y) or to cancel it at any time. 
Also it publishes the robot position and velocity as a custom message by reling on the topic /odom.  
	
"""

import rospy
import os
import actionlib
import actionlib.msg
import assignment_2_2023
import assignment_2_2023.msg

from std_srvs.srv import *
from geometry_msgs.msg import Point, Pose, Twist
from nav_msgs.msg import Odometry
from assignment_2_2023.msg import RobotMsg

def callback(msg):
	"""
	Callback function to publish position and velocity of the robot taken from */odom* topic
	*msg(Odometry)*: Contains the odometry of the robot
	
	"""
	global pub
	
	# Create a custom message for having the location and velocities
	my_msg = RobotMsg()
	
	# Use the message to set the robot position and linear velocity
	my_msg.x = msg.pose.pose.position.x
	my_msg.y = msg.pose.pose.position.y
	my_msg.vel_x = msg.twist.twist.linear.x
	my_msg.vel_y = msg.twist.twist.linear.y
    
	# Publish the message
	pub.publish(my_msg)


def set_target():
	"""
	Function that collect user input for a target position (x, y) that
	the robot must reach inside the simulation environment and send the target (goal) to the action server
	"""
	# Get target position from terminal
	x_pos = float(input("Enter the x value (x<=9, x>=-9): "))
	y_pos = float(input("Enter the y value (y<=9, y>=-9): "))

	# Print the selected coordinates 
	print("The position of the target is: (", x_pos, ", ", y_pos, ")")

	# Creates a goal message with the target coordinates
	goal = assignment_2_2023.msg.PlanningGoal()
	goal.target_pose.pose.position.x = x_pos
	goal.target_pose.pose.position.y = y_pos
    
	# Send the goal to the action server
	client.send_goal(goal)
	print("The target has been successfully sent to the sever!!")
 
	user_action()	 # Back to the interface function

def user_action():
	"""
	The function is called at the beginning of the program
	The user can choose to set a goal, to cancel it or to exit the program by entering the correct number
	""" 

	print(" A Guid to Control the Robot  \n")
	print("   Enter 1: Target Position   \n")
	print("   Enter 2: Cancel            \n")
	print("   Enter 3: Exit              \n")	 
        
	# Ask the user to select a mission
	mission = input("Select 1, 2 or 3 and then press Enter: ")
        
	# Check what is the mission
	if   (mission == "1"):
		print("I'll go to the location!")
		set_target()
	elif (mission == "2"):
		print("Oh, It seems the mission is cancled!")
		client.cancel_goal()
		print("The target has been cancelled successfully!!")
		user_action() # Back to the interface function     	
	elif (mission == "3"):
		print("It's Exit! I'm no longer able to go anywhere:(")
		exit()  
	else:
		print("Wrong choise!! Please read the instruction!")
		user_action()      
	
if __name__ == '__main__':

	# Init Node
	rospy.init_node("node_a")
	
	# Define a global publisher in order to publish the RobotMsg custom message
	global pub
	pub = rospy.Publisher("/pos_vel", RobotMsg, queue_size = 1)

	# Define a subscriber which listen to the Odometry message and calls the callback function
	rospy.Subscriber("/odom", Odometry, callback)
    
	# Create a new client
	client = actionlib.SimpleActionClient('/reaching_goal', assignment_2_2023.msg.PlanningAction)	
    
	# Wait for the server to be ready to receive the goal 
	client.wait_for_server()
    
	# Call the UI function
	user_action()

