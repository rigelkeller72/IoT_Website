
#include <dht.h>

dht DHT;
float temp,hum;
#define echoPin 2 // attach pin D2 Arduino to pin Echo of HC-SR04
#define trigPin 3 //attach pin D3 Arduino to pin Trig of HC-SR04
long duration;
int distance,inp;
float pot;
int potpin = A5;
char data[20];
#define DHT11_PIN 7
void setup() {
   pinMode(trigPin, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPin, INPUT); // Sets the echoPin as an INPUT
  pinMode(LED_BUILTIN, OUTPUT);
  // put your setup code here, to run once:
  Serial.begin(9600);
  
}

void loop() {
  
  while(true)
  {
    if(Serial.available() > 0)
     {
        break;
     }
     digitalWrite(LED_BUILTIN, LOW);
  }
  inp = Serial.read();
  delayMicroseconds(10);
  switch (inp)
  {
    case 'r':
      //readsensors();
      digitalWrite(LED_BUILTIN, HIGH);
      Serial.println("We got an r");
      break;
    case 'l':
      digitalWrite(LED_BUILTIN, HIGH);
      break;
    case 'o':
      digitalWrite(LED_BUILTIN, LOW);
      break;
    case -1:
    Serial.println("no data");
      break;
     default:
      Serial.println("AHAHAAHHHAH");
      
  }

  /*
  // put your main code here, to run repeatedly:
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
  distance = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)
  dht DHT;
  #define DHT11_PIN 7
  // Displays the distance on the Serial Monitor
  int test1 = DHT.read11(DHT11_PIN);
  temp = DHT.temperature;
  hum = DHT.humidity;
  pot = analogRead(potpin)/1023.0;
  Serial.print(distance);
  Serial.print(",");
  Serial.print(temp);
  Serial.print(",");
  Serial.print(hum);
  Serial.print(",");
  Serial.println(pot);
  Serial.flush();
  */
  
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
      distance = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)
      dht DHT;
      #define DHT11_PIN 7
      // Displays the distance on the Serial Monitor
      int test1 = DHT.read11(DHT11_PIN);
      temp = DHT.temperature;
      hum = DHT.humidity;
      pot = analogRead(potpin)/1023.0;
      Serial.print(distance);
      Serial.print(",");
      Serial.print(temp);
      Serial.print(",");
      Serial.print(hum);
      Serial.print(",");
      Serial.print(pot);
      Serial.print("\n");
      Serial.flush();
  }
