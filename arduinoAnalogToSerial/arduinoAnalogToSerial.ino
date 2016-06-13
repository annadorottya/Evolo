/*
  Analog input, serial output

  Potentiometer connected to the A0 pin of Arduino
  
This code is based on the example code shipped with Arduino IDE. That code is in the public domain and created by:

 created 29 Dec. 2008
 modified 9 Apr 2012
 by Tom Igoe
 
 */

// These constants won't change.  They're used to give names
// to the pins used:
const int analogInPin = A10;  // Analog input pin that the potentiometer is attached to
int sensorValue = 0;        // value read from the pot

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
}

void loop() {
  // read the analog in value:
  sensorValue = analogRead(analogInPin);

  Serial.println(sensorValue);

  // wait 200 milliseconds before the next loop
  // for the analog-to-digital converter to settle
  // after the last reading:
  delay(200);
}
