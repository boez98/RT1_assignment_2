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
	
    # Get the desired position
    des_x = rospy.get_param("des_pos_x")
    des_y = rospy.get_param("des_pos_y")
        
    # Get the actual position and speed
    x = msg.pos_x
    y = msg.pos_y
    vx = msg.vel_x
    vy = msg.vel_y
        
    # Compute the distance
    dist = ((x-des_x)**2 + (y-des_y)**2)**0.5
    
    # Compute the average speed
    avg_speed = (vx**2 + vy**2)**0.5
    
    # Get frequency parameter
    freq = rospy.get_param("/set_frequency")
     
    # Print  
    print("Distance from the goal: " , dist)
    print("Average speed: ", avg_speed)
    print()
    
    # Sleep time depend on frequency  
    time.sleep(1/freq)
    
    

def main():

    # Initializes a rospy node
    rospy.init_node('dist_speed', anonymous=True)
    
    # Subscriber to /pos_and_vel topic to get the position and velocity
    sub = rospy.Subscriber('/pos_and_vel', Pos_and_Vel, callback)
	
    # Wait
    rospy.spin()
    
    
	
if __name__ == "__main__":
	main()	
