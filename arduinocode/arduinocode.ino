#include "dht.h"
#include "Servo.h"

dht DHT;
float temp,hum;
#define echoPin 2 // attach pin D2 Arduino to pin Echo of HC-SR04
#define trigPin 3 //attach pin D3 Arduino to pin Trig of HC-SR04
long duration;
float distance;
char cmd;
//char resetted = 'o';
int pir;
int hallSensorPin = A2; 
int hallDrivePin = A1;
int buzzer = 8;
Servo servo;
Servo serv2;
int pirpin = A5;
int mags = 0;
#define DHT11_PIN 13
void setup() {
   pinMode(trigPin, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPin, INPUT); // Sets the echoPin as an INPUT
  pinMode(buzzer, OUTPUT);
  pinMode(hallDrivePin, OUTPUT);
  pinMode(hallSensorPin, INPUT);    
  // put your setup code here, to run once:
  Serial.begin(9600);
  servo.attach(5);
  servo.write(135);
  serv2.attach(6);
  serv2.write(135);
  
}

void loop() {
  if(Serial.available() > 0)
  {
    cmd = Serial.read();
      switch (cmd)
      {
      case 'r':
        readsensors();
        //serial.print(1,20,6,10);
        break;
      case 'l':
        servo.write(0);
        serv2.write(0);
        Serial.print("door locked\n");
        //resetted ='g';
        break;
      case 'o':
        servo.write(135);
        serv2.write(135);
        Serial.print("LIGHT_OFF\n");
        break;
       case 'b':
        digitalWrite(buzzer, HIGH);
        Serial.print("AHHHH\n");
        break;
        case 'q':
          digitalWrite(buzzer, LOW);
          Serial.print("AHHHH\n");
        break;
        case 'x':
        serv2.write(180);
        Serial.print("left\n");
        break;
        case 'y':
        serv2.write(0);
        Serial.print("right\n");
        break;
      default:
        Serial.print("Unknown Command use rlo\n");
        break;
      
  }
  //Serial.print(resetted);
  }


}
void readsensors(){
      // Clears the trigPin condition
    digitalWrite(hallDrivePin,LOW);
       delayMicroseconds(2);
       digitalWrite(hallDrivePin,HIGH); 
     digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)
      dht DHT;
      #define DHT11_PIN 13
      // Displays the distance on the Serial Monitor
      int test1 = DHT.read11(DHT11_PIN);
      temp = DHT.temperature;
      hum = DHT.humidity;
       digitalWrite(hallDrivePin,HIGH);
      mags = digitalRead(hallSensorPin);
      pir = digitalRead(pirpin);
      Serial.print(distance);
      Serial.print(",");
      Serial.print(temp);
      Serial.print(",");
      Serial.print(hum);
      Serial.print(",");
      Serial.print(mags);
      Serial.print(",");
      Serial.print(pir);
      Serial.print("\n");
      Serial.flush();
       digitalWrite(hallDrivePin,LOW);
       delayMicroseconds(2);
       digitalWrite(hallDrivePin,HIGH);
  }
