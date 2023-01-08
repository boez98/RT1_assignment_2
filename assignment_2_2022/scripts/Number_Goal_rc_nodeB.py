#! /usr/bin/env python

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
    
    return  Num_Goal_rcResponse(num_r, num_c)



def main():
	
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
