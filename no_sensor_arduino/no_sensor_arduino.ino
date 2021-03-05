// Created by RIGEL KELLER 04MAR21
// IN PROGRESS
// Code intended to run with out sensors attached. Fixed values will be displayed. 

// Libraries
#include "DHT.h"
#include "Servo.h"

// Declare Global Variables
float temp,hum;
#define echoPin 3 // attach pin D2 Arduino to pin Echo of HC-SR04
#define trigPin 4 //attach pin D3 Arduino to pin Trig of HC-SR04
long duration;
float distance;
char cmd;
//char resetted = 'o';
float pot;
int hallSensorPin = 2; 
int hallDrivePin = 1;
int buzzer = 8;
Servo servo;
Servo serv2;
int potpin = A5;
int mags = 0;

//DHT11 set-up
#define DHTPIN 7   // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);


void setup() {
  Serial.begin(9600);
  

  pinMode(trigPin, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPin, INPUT); // Sets the echoPin as an INPUT
  pinMode(buzzer, OUTPUT);
  pinMode(hallDrivePin, OUTPUT);
  pinMode(hallSensorPin, INPUT);    
 

dht.begin();
  
  // Servo Motor code
  servo.attach(5);
  servo.write(135);
  serv2.attach(9);
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
        break;
      case 'l':
        servo.write(0);
        Serial.print("door locked\n");
        //resetted ='g';
        break;
      case 'o':
        servo.write(135);
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
        Serial.print("Unknown Command use rlobqxy\n");
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

      //Reading Data
      /*
      // Reads the echoPin, returns the sound wave travel time in microseconds
      duration = pulseIn(echoPin, HIGH);
      // Calculating the distance
      distance = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)  
      temp = dht.readTemperature();
      hum = dht.readHumidity();
      digitalWrite(hallDrivePin,HIGH);
      mags = digitalRead(hallSensorPin);
      pot = analogRead(potpin)/1023.0;
      */
      
       //Uncomment for fixed data. Useful when sensors are not available.
       distance = 2021;
       temp = 2021;
       hum = 2021;
       mags = 2021;
       pot = 2021;
       
      //Printing Data
      Serial.print(distance);
      Serial.print(",");
      Serial.print(temp);
      Serial.print(",");
      Serial.print(hum);
      Serial.print(",");
      Serial.print(mags);
      Serial.print(",");
      Serial.print(pot);
      Serial.print(digitalRead(buzzer));
      Serial.print("\n");
      Serial.flush();
       digitalWrite(hallDrivePin,LOW);
       delayMicroseconds(2);
       digitalWrite(hallDrivePin,HIGH);
  }
