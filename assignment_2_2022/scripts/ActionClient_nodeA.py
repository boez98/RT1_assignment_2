#! /usr/bin/env python

## @package assignment_2_2022
#\file action_client.py
#\brief This script sends goals to an action server and publishes the position and velocity of the robot on a custom topic.
#\author Andrea Bolla
#\version 0.1 
#\date 24/02/2023
#
#\details This script initializes a ROS node and sets up a publisher to the "/pos_and_vel" topic to publish the position and velocity
# of the robot. It also sets up a subscriber to the "/odom" topic to receive the robot's position and velocity. Finally, it
# sends goals to an action server upon receiving keyboard input.
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





def callback(msg):

    ##
    #\brief Callback function for the Odometry subscriber.
    #
    # This function is called every time a message is received on the "/odom" topic. It extracts the robot's position and linear
    # velocity, creates a custom message, and publishes it to the "/pos_and_vel" topic.
    #
    #\param msg The message received from the "/odom" topic.
    #
    #

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

    ##
    #\brief Client function that sends goals to the action server.
    #
    # This function sends goals to an action server upon receiving keyboard input. It waits for the server to start up and listen
    # for goals before sending a goal. It cancels the goal if the user enters "c" and the robot is reaching the goal position.
    #
    #

    
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
    ##
    #\brief Main function that initializes the node, sets up the publisher and subscriber, and starts the client.
    #
    #
    
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
