from serial import Serial
from pynmeagps import NMEAReader
import rospy
from sensor_msgs.msg import NavSatFix


def talker(lat,lon):
    pub = rospy.Publisher('GPS', NavSatFix, queue_size = 10)
    rospy.init_node('raspi', anonymous = True)
    rate = rospy.Rate(1)
    msg = NavSatFix()
    msg.header.frame_id = 'gps'
    msg.latitude = lat
    msg.longitude = lon
    msg.altitude = 0
    rospy.loginfo(msg)
    pub.publish(msg)
    rate.sleep()
  
  
    
    
i = 0
while(True):
    
    stream = Serial('/dev/ttyACM0', 9600, timeout=3)
    nmr = NMEAReader(stream)
    (raw_data, parsed_data) = nmr.read()
    print(parsed_data)
    
    try:
        if(i>0):
            if(parsed_data.lat != ''):
                print(parsed_data.lat)
                talker(parsed_data.lat,parsed_data.lon)
        i =1
    except Exception as e:
        print("Wron NMEA Format")
    
