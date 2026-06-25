
#include <Arduino.h>
#include <EEPROM.h>
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>


#define led1_g D1
#define led1_y D2
#define led1_r D5

#define led2_g D6 
#define led2_y D2
#define led2_r D7



String inputString = "";         // a String to hold incoming data
boolean stringComplete = false;  // whether the string is complete

void setup() {
  // initialize serial:
  Serial.begin(115200);
  // reserve 200 bytes for the inputString:
  inputString.reserve(200);

  pinMode(led1_g,OUTPUT);
  pinMode(led1_y,OUTPUT);
  pinMode(led1_r,OUTPUT);

  
  pinMode(led2_g,OUTPUT);
  pinMode(led2_y,OUTPUT);
  pinMode(led2_r,OUTPUT);


}



void loop() {
  
  while (Serial.available() > 0) {
    char inChar = (char)Serial.read();
    if(inChar == '\n') {
      stringComplete = true;
    }
    else{
      inputString += inChar;
    }
  }


  if(stringComplete){
    Serial.println(inputString);
    int index1 = inputString.indexOf("<cnt>");
    int index2 = inputString.indexOf("</cnt>");
    
    if(index1 != -1 && index2 != -1){
      String cnt = inputString.substring(index1+5, index2);
      
    }

    if(inputString.indexOf("GREEN1") != -1){
        digitalWrite(led1_g,HIGH);
        digitalWrite(led1_y,LOW);
        digitalWrite(led1_r,LOW);
    }
    if(inputString.indexOf("GREEN2") != -1){
        digitalWrite(led2_g,HIGH);
        digitalWrite(led2_y,LOW);
        digitalWrite(led2_r,LOW);
    }

    

    if(inputString.indexOf("YELLOW") != -1){
        digitalWrite(led1_g,LOW);
        digitalWrite(led1_y,HIGH);
        digitalWrite(led1_r,LOW);
    }
    if(inputString.indexOf("RED1") != -1){
        digitalWrite(led1_g,LOW);
        digitalWrite(led1_y,LOW);
        digitalWrite(led1_r,HIGH);
    }
    if(inputString.indexOf("RED2") != -1){
        digitalWrite(led2_g,LOW);
        digitalWrite(led2_y,LOW);
        digitalWrite(led2_r,HIGH);
    }

    if(inputString.indexOf("OFFALL") != -1){
        digitalWrite(led1_g,LOW);
        digitalWrite(led1_y,LOW);
        digitalWrite(led1_r,LOW);
        digitalWrite(led2_g,LOW);
        digitalWrite(led2_y,LOW);
        digitalWrite(led2_r,LOW);
    }
    
    stringComplete = false;
    inputString = "";
  }     
  
}
