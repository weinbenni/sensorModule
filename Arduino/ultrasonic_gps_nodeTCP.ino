#include <SPI.h>
#include <Ethernet.h>

#define ROSSERIAL_ARDUINO_TCP
#include <ros.h>
#include <sensor_msgs/NavSatFix.h>
#include <std_msgs/UInt16.h>
#include <SoftwareSerial.h>
#include <VMA430_GPS.h> 




byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
IPAddress ip(192, 168, 0, 177);

// Set the rosserial socket server IP address
IPAddress server(192,168,0,11);
// Set the rosserial socket server port
const uint16_t serverPort = 11411;


ros::NodeHandle  nh;

SoftwareSerial ss(3, 2); // RX, TX
VMA430_GPS gps(&ss);     // Pass the softwareserial connection info the the GPS module library

//sensor_msgs::Range range_msg;
std_msgs::UInt16 ultrasonicLeft_msg;
std_msgs::UInt16 ultrasonicFront_msg;
std_msgs::UInt16 ultrasonicRight_msg;
sensor_msgs::NavSatFix gpsData_msg;
ros::Publisher pub_int1( "/ultrasonicLeft", &ultrasonicLeft_msg);
ros::Publisher pub_int2( "/ultrasonicFront", &ultrasonicFront_msg);
ros::Publisher pub_int3( "/ultrasonicLeft", &ultrasonicRight_msg);
ros::Publisher pub_gps( "/ultrasonicLeft", &ultrasonicRight_msg);


int pingPinFront = 8;
int inPinFront = 9;
char frameid[] = "/ultrasonic";
int range_time = 500;


void setup() {
  // Use serial to monitor the process
  //Serial.begin(115200);

  // Connect the Ethernet
  Ethernet.begin(mac, ip);

  // Let some time for the Ethernet Shield to be initialized
  delay(1000);

  // Set the connection to rosserial socket server
  nh.getHardware()->setConnection(server, serverPort);
  nh.initNode();

  nh.advertise(pub_int1);
  nh.advertise(pub_int2);
  nh.advertise(pub_int3);
  // range_msg.radiation_type = sensor_msgs::Range::ULTRASOUND;
  // range_msg.header.frame_id =  frameid;
  // range_msg.field_of_view = 0.1;  // fake
  // range_msg.min_range = 3.0;
  // range_msg.max_range = 600.47;

  gps.begin(9600);
  gps.setUBXNav(); // Enable the UBX mavigation messages to be sent from the GPS module

}

void loop()
{
  if (gps.getUBX_packet()) // If a valid GPS UBX data packet is received...
  {
    gps.parse_ubx_data(); // Parse the new data
    if (gps.utc_time.valid) // If the utc_time passed from the GPS is valid...
    {
      // Print UTC time hh:mm:ss
      //th = gps.utc_time.hour;
      //tm = gps.utc_time.minute;
      //ts = gps.utc_time.second;
    }
      gpsData_msg.latitude = gps.location.latitude;
      gpsData_msg.longitude = gps.location.longitude;
      pub_gps.publish(&gpsData_msg);
  }
  


  if ( millis() >= range_time ){
      int r =0;  
      if (nh.connected()){
        //Serial.println("Connected");
        ultrasonicLeft_msg.data = getRange(pingPinFront, inPinFront) * 1;
        ultrasonicFront_msg.data = getRange(pingPinFront, inPinFront) * 1;
        ultrasonicRight_msg.data = getRange(pingPinFront, inPinFront) * 1;
        // ultrasonicLeft_msg.header.stamp = nh.now();
        //ultrasonicFront_msg.header.stamp = nh.now();
        //ultrasonicRight_msg.header.stamp = nh.now();
        pub_int1.publish(&ultrasonicLeft_msg);
        pub_int2.publish(&ultrasonicFront_msg);
        pub_int3.publish(&ultrasonicRight_msg);
        range_time =  millis() + 50;
      }
      else {
        //Serial.println("Not Connected");
      }
        
        
    nh.spinOnce();
    delay(1);
  }
}

long microsecondsToCentimeters(long microseconds)
{
// The speed of sound is 340 m/s or 29 microseconds per centimeter
return microseconds / 29.1 / 2;
}

float getRange(int pingPin, int inPin)
{
    
    // establish variables for duration of the ping,
  // and the distance result in inches and centimeters:
  long duration, cm;
  
  // The PING))) is triggered by a HIGH pulse of 2 or more microseconds.
  // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
  pinMode(pingPin, OUTPUT);
  digitalWrite(pingPin, LOW);
  delayMicroseconds(2);
  digitalWrite(pingPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(pingPin, LOW);
  
  // The same pin is used to read the signal from the PING))): a HIGH
  // pulse whose duration is the time (in microseconds) from the sending
  // of the ping to the reception of its echo off of an object.
  pinMode(inPin, INPUT);
  duration = pulseIn(inPin, HIGH);
  
  // convert the time into a distance
  return microsecondsToCentimeters(duration);
}
