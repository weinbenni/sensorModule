
import RPi.GPIO as GPIO
import time
import rospy
from sensor_msgs.msg import Range
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins1
GPIO_TRIGGER1 = 23
GPIO_ECHO1 = 24

#set GPIO Pins2
GPIO_TRIGGER2 = 25
GPIO_ECHO2 = 8

#set GPIO Pins3
GPIO_TRIGGER3 = 23
GPIO_ECHO3 = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER1, GPIO.OUT)
GPIO.setup(GPIO_ECHO1, GPIO.IN)
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER2, GPIO.OUT)
GPIO.setup(GPIO_ECHO2, GPIO.IN)
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER3, GPIO.OUT)
GPIO.setup(GPIO_ECHO3, GPIO.IN)
 
def distance(GPIO_TRIGGER, GPIO_ECHO):
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 343) / 2
 
    return distance
 
def publishSensor(sensor,measRange):
    pub = rospy.Publisher(sensor, Range, queue_size = 10)
    rospy.init_node('raspiRange', anonymous = True)
    rate = rospy.Rate(6)
    msg = Range()
    msg.header.frame_id = sensor
    msg.field_of_view = 50/146.0*3.14159
    msg.radiation_type = msg.ULTRASOUND
    msg.max_range = 4
    msg.min_range = 0.02
    msg.range = measRange
    
    rospy.loginfo(msg)
    pub.publish(msg)
    rate.sleep()

 
if __name__ == '__main__':
    try:
        while True:
            dist1 = distance(GPIO_TRIGGER1,GPIO_ECHO1)
            #print ("Measured Distance = %.1f cm" % dist)
            publishSensor("US1", dist1 )
            dist2 = distance(GPIO_TRIGGER2,GPIO_ECHO2)
            publishSensor("US2", dist2 )
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()