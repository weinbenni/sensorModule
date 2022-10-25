#!/usr/bin/env python

import rospy
from std_msgs.msg import UInt16
from UltrasonicSensor import *
from RosCommunication import *
import threading
      

ultrasonicLeftData = RosCommunicationUint16()
ultrasonicRightData = RosCommunicationUint16()
ultrasonicRefData = RosCommunicationUint16()
temperatureData = RosCommunicationUint16()


def run_thread():
    rate = rospy.Rate(1) # Ros-Rate at 1Hz
    ### INIT___________________________________________________
    
    ultrasonicSensorLeft = UltrasonicSensor()
    ultrasonicSensorRight = UltrasonicSensor()
    
    ### END_INIT_______________________________________________
    while not rospy.is_shutdown():
        ### CYCLIC___________________________________________________
        
        global ultrasonicLeftData
        #rospy.loginfo(ultrasonicLeftData.GetUINT16Data())
        global ultrasonicRightData
        #rospy.loginfo(ultrasonicRightData.GetUINT16Data())
        global ultrasonicRefData
        #rospy.loginfo('Time reference ultrasonic: ' + str(ultrasonicRefData.GetUINT16Data()))
        global temperatureData
        #rospy.loginfo('Temperature: ' + str(temperatureData.GetUINT16Data()))
        
        UltrasonicSensor.CalculateSpeedOfLight(temperatureData.GetUINT16Data(), ultrasonicRefData.GetUINT16Data())
        ultrasonicSensorLeft.WriteTime(ultrasonicLeftData.GetUINT16Data())
        ultrasonicSensorRight.WriteTime(ultrasonicRightData.GetUINT16Data())
        rospy.loginfo('Distance left ultrasonic: ' + str(ultrasonicSensorLeft.GetDistance()))
        rospy.loginfo('Distance right ultrasonic: ' + str(ultrasonicSensorRight.GetDistance()))
        rospy.loginfo('Speed of light: ' + str(UltrasonicSensor.GetSpeedOfLight()))
        
        ### END_CYCLIC________________________________________________
        rate.sleep()
       

if __name__ == '__main__':
    try:
        # the main entry point
        rospy.init_node('Subscriber_Node', anonymous=True)
        rospy.Subscriber('/ultrasonicLeft', UInt16, ultrasonicLeftData.callback) 
        rospy.Subscriber('/ultrasonicRight', UInt16, ultrasonicRightData.callback) 
        rospy.Subscriber('/ultrasonicRef', UInt16, ultrasonicRefData.callback) 
        rospy.Subscriber('/temperature', UInt16, temperatureData.callback)
        worker = threading.Thread(target=run_thread)
        worker.start()
        
        rospy.spin()
        
    except rospy.ROSInterruptException:
        pass   
