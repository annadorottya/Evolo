#include <LiquidCrystal.h>

const int analogInPin = A10;  // Analog input pin that the potentiometer is attached to
int sensorValue = 0;        // value read from the pot
int mode;
int oldmode = -1;

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
}

void loop() {
  // read the analog in value and calcukate the average of it for 5 measures
  sensorValue = 0;
  for(int i=0; i < 5; i++){
    sensorValue += analogRead(analogInPin);
    delay(100); // for the analog-to-digital converter to settle
  }
  sensorValue /= 5;
  
  if(sensorValue < 180 || sensorValue > 890)
    mode = 0; //Off
  else if(sensorValue < 430)
    mode = 1; //Aggressive
  else if(sensorValue < 660)
    mode = 2; //Moderate
  else
    mode = 3; //Gracious
    
  Serial.println(mode); //send it to the Raspberry
  
  if(oldmode != mode){ //if mode has changed, display it
    oldmode = mode;
    lcd.setCursor(0, 0); //set cursor to first row
    lcd.print("Mode: ");
    if(mode == 0)
      lcd.print("Off       ");
    else if(mode == 1)
      lcd.print("Aggressive");
    else if(mode == 2)
      lcd.print("Moderate  ");
    else if(mode == 3)
      lcd.print("Gracious  ");
  }

  if(Serial.available() > 0){
    lcd.setCursor(0, 1); //set the cursor to the beginning of the second row
    lcd.print("                "); //delete the previous message
    lcd.setCursor(0, 1);
  }
  int i=0;
  while(Serial.available() > 0){ //if incoming log data, display it
    if(i == 16) break; //if 16 characters printed, exit
    char incomingByte = Serial.read();
    if(incomingByte == -1) continue; //-1 means no data
    lcd.print(incomingByte);
    delay(10); //wait for next character
    i++;
  }
  delay(200);
}
