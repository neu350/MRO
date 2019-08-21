/* servoControl-microseconds

v1.0, 2016-06-15
v1.1, 2016-06-17: verbose to troubleshoot position signal.
v1.2, 2016-02-26 : rebuild to accommodate moving in either direction with any command.
v1.3, 2019-08-15: open pos expectation from 0:15 to 0:30

servo control over serial
input: position 0:15 and speed a (slow) through f (fast) or r to retract

*/ 

#include <Servo.h> 
 
Servo myservo;  // create servo object to control a servo 

int pos=0;          // target position for each function call (in mm displacement)
char ch;            // initialize serial byte variable 
int outPin=3;
int anlgOut=0; 
int target=0;       // target position in microseconds
int current=2000;    // incremental position in microseconds
int increment = 0;  // step size according to speed


void setup() 
{ 
  Serial.begin(9600); // initialize serial connection, baud rate 9600 
  myservo.attach(9); // attaches the servo on pin 9 to the servo object 
  myservo.writeMicroseconds(2000); 
  Serial.println("Servo Control Clockwise Pull V1.3"); // display in serial monitor
  Serial.println("Enter command: "); 
} 
 
void loop() 
{ 

  if ( Serial.available()>0) {
    ch = Serial.read();

    
    switch(ch) { 

      case '0'...'9': 
        pos = pos*10+ch-'0';    
        pos = constrain(pos,0,179); 
        target=map(pos,0,30,2000,1000);
// this map statement changes if you want a ccw pull instead of clockwise;
// switch 2000 and 1000 to reverse
        break;

      case 'f':
        current = target;
        myservo.writeMicroseconds(current);    
        anlgOut=map(current,1000,2000,1,254); 
        analogWrite(outPin,anlgOut);
        pos=0;   
        break; 
        
      case 'r': 
        pos=0;  
        for (current; current<=2000; current-=10) {
//reverse to zero also changes: >=1000 instead of <=2000.
        myservo.writeMicroseconds(current);    
        anlgOut=map(current,1000,2000,1,254); 
        analogWrite(outPin,anlgOut);
        delay(10);  
        } 
        break;
        
      case 'a': 
        increment = 2;

        if (current < target) {
          extend(current, target, increment);
        }
        else if (current > target) {
          retract(current, target, increment);
        }
        
        current = target;       
        pos = 0;  
        break; 
        
      case 'b': 
        increment = 4;

        if (current < target) {
          extend(current, target, increment);
        }
        else if (current > target) {
          retract(current, target, increment);
        }
        
        current = target;       
        pos = 0;  
        break; 
        
      case 'c': 
        increment = 6;

        if (current < target) {
          extend(current, target, increment);
        }
        else if (current > target) {
          retract(current, target, increment);
        }
        
        current = target;       
        pos = 0;  
        break; 
        
      case 'd': 
         increment = 8;

        if (current < target) {
          extend(current, target, increment);
        }
        else if (current > target) {
          retract(current, target, increment);
        }
        
        current = target;       
        pos = 0;  
        break; 
                  
      case 'e': 
        increment = 10;

        if (current < target) {
          extend(current, target, increment);
        }
        else if (current > target) {
          retract(current, target, increment);
        }
        
        current = target;       
        pos = 0;  
        break;   
    }
  }
  else
  {
  anlgOut=map(current,1000,2000,1,254); 
  analogWrite(outPin,anlgOut);  
 

  }

}

void extend(int current, int target, int increment)
{

  for(current; current <= target; current+=increment) {
    myservo.writeMicroseconds(current);
    anlgOut=map(current,1000,2000,1,254); 
    analogWrite(outPin,anlgOut); 
    delay(10);  
  }
}

void retract(int current, int target, int decrement)
{
  for(current; current >= target; current-=decrement) {
    myservo.writeMicroseconds(current);
    anlgOut=map(current,1000,2000,1,254); 
    analogWrite(outPin,anlgOut); 
    delay(10); 
  }
}
