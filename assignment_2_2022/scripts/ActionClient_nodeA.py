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



def callback(msg):

    global pub
 
    # Get the position 
    position_ = msg.pose.pose.position
    
    # Get the linear velocity
    vel_lin = msg.twist.twist.linear
    
    # Create custom message
    pos_vel = Pos_and_Vel()
    pos_vel.pos_x = position_.x
    pos_vel.pos_y = position_.y
    pos_vel.vel_x = vel_lin.x
    pos_vel.vel_y = vel_lin.y
    
    # Publish the custom message
    pub.publish(pos_vel)
        
        
        
def Client():
    
    # Creates the SimpleActionClient, passing the type of the action to the constructor.
    client = actionlib.SimpleActionClient('/reaching_goal', assignment_2_2022.msg.PlanningAction)

    # Waits until the action server has started up and started listening for goals.
    client.wait_for_server()

    # Status goal is true if the robot is reaching the position otherwise is false
    status_goal = False
	
    while not rospy.is_shutdown():
        
        # Get the keyboard inputs
        print("Please insert a new position or type c to cancel it ")
        x = input("x: or c: ")
        y = input("y: or c: ")
        
 	# If user entered 'c' and the robot is reaching the goal position, cancel the goal
        if x == "c" and status_goal == True:
            
            # Cancel the goal
            client.cancel_goal()
            status_goal = False

        else:
            # Convert numbers from string to float
            x = float(x)
            y = float(y)
            
            # Create the goal to send to the server
            goal = assignment_2_2022.msg.PlanningGoal()

            goal.target_pose.pose.position.x = x
            goal.target_pose.pose.position.y = y
					
            # Send the goal to the action server
            client.send_goal(goal)
            
            status_goal = True


       
def main():

    global pub
    
    try:
        # Initializes a rospy node so that the SimpleActionClient can publish and subscribe over ROS.
        rospy.init_node('action_client_py')
        
        # Publisher to /pos_and_vel topic the position and velocity
        pub = rospy.Publisher("/pos_and_vel", Pos_and_Vel, queue_size=10)
        
        # Subscriber to /odom topic to get position and velocity
        sub = rospy.Subscriber('/odom', Odometry, callback)
        
        # Start client
        Client()
        
               
    except rospy.ROSInterruptException:
        print("program interrupted before completion")
        
        
   
if __name__ == '__main__':
    main()
