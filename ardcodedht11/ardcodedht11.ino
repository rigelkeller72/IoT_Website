
#include <dht.h>

dht DHT;
float temp,hum;
#define echoPin 3 // attach pin D2 Arduino to pin Echo of HC-SR04
#define trigPin 4 //attach pin D3 Arduino to pin Trig of HC-SR04
long duration;
float distance;
char cmd;
//char resetted = 'o';
float pot;
int hallSensorPin = 2; 
int potpin = A5;
int mags = 0;
#define DHT11_PIN 7
void setup() {
   pinMode(trigPin, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPin, INPUT); // Sets the echoPin as an INPUT
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(hallSensorPin, INPUT);    
  // put your setup code here, to run once:
  Serial.begin(9600);
  
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
        digitalWrite(LED_BUILTIN, HIGH);
        Serial.print("LIGHT_ON\n");
        //resetted ='g';
        break;
      case 'o':
        digitalWrite(LED_BUILTIN, LOW);
        Serial.print("LIGHT_OFF\n");
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
      digitalWrite(trigPin, LOW);
      delayMicroseconds(2);
      // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
      digitalWrite(trigPin, HIGH);
      delayMicroseconds(10);
      digitalWrite(trigPin, LOW);
      // Reads the echoPin, returns the sound wave travel time in microseconds
      duration = pulseIn(echoPin, HIGH);
      // Calculating the distance
      distance = duration * 0.034 / 2.0; // Speed of sound wave divided by 2 (go and back)
      dht DHT;
      #define DHT11_PIN 7
      // Displays the distance on the Serial Monitor
      int test1 = DHT.read11(DHT11_PIN);
      temp = DHT.temperature;
      hum = DHT.humidity;
      mags = digitalRead(hallSensorPin);
      //pot = analogRead(potpin)/1023.0;
      Serial.print(distance);
      Serial.print(",");
      Serial.print(temp);
      Serial.print(",");
      Serial.print(hum);
      Serial.print(",");
      Serial.print(mags);
      Serial.print("\n");
      Serial.flush();
  }
