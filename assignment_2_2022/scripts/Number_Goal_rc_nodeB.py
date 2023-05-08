#! /usr/bin/env python

## @package assignment_2_2022
#\file action_client.py
#\brief  This script implements a ROS node that provides a service to count the number of goals that are reached and canceled.
#\author Andrea Bolla
#\version 0.1 
#\date 24/02/2023
#
#


import rospy
from geometry_msgs.msg import Point, Pose, Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import math
import actionlib
import actionlib.msg
import assignment_2_2022.msg
from tf import transformations
from std_srvs.srv import *
import time
import sys
import select
from assignment_2_2022.msg import Pos_and_Vel
from assignment_2_2022.srv import Num_Goal_rc, Num_Goal_rcResponse



# Variables initialization
num_c = 0;
num_r = 0;



def callback(msg):
    ##
    #\brief Callback function to get the status of the /reaching_goal/result topic and update the counters.
    #
    #\param msg A message containing the status of the goal.
    #
    #


    global num_c, num_r

    # Get the status 
    status = msg.status.status

    # If status is 2 the goal is canceled
    if status == 2:
        num_c = num_c + 1

    # If status is 3 the goal is reached
    elif status == 3:
        num_r = num_r + 1
		


def update_n_goal(req):
    ##
    #\brief Function that updates the counter and returns the number of goals reached and canceled.
    #
    #\param req A request message containing no data.
    #\return A response message with the number of goals reached and canceled.
    #
    #

    return  Num_Goal_rcResponse(num_r, num_c)



def main():
    ##
    #\brief Main function that initializes the node, sets up the publisher and subscriber, and starts the client.
    #
    #

    # Initialize the node
    rospy.init_node('n_goal_rc_server')
	
    # Subscriber to /reaching_goal/result topic to get status
    sub = rospy.Subscriber('/reaching_goal/result', assignment_2_2022.msg.PlanningActionResult, callback)
    
    # Provide the service /n_goal
    s = rospy.Service('/n_goal', Num_Goal_rc, update_n_goal)
    
    # Wait
    rospy.spin()
    
    

if __name__ == "__main__":
    main()
