#include "Adafruit_Si7021.h"

Adafruit_Si7021 sensor = Adafruit_Si7021();

int WaterRelay_3 = 3;
int LightsRelay_2 = 2;  
int FanRelay_1 = 6;     
void setup()   /****** SETUP: RUNS ONCE ******/
{
Serial.begin(115200);
pinMode(LightsRelay_2, OUTPUT);      // sets the digital pin as output
digitalWrite(LightsRelay_2, HIGH);
pinMode(WaterRelay_3, OUTPUT); 
digitalWrite(WaterRelay_3, HIGH);
pinMode(FanRelay_1, OUTPUT);
digitalWrite(FanRelay_1, HIGH);
sensor.begin(); 
}
void loop() {   
String tempsensor = "On";
String c ="";
boolean l;
boolean w;
boolean f;

while (Serial.available() > 0) {
    char inChar = Serial.read();
    c += inChar;
  } 
 
    if(c.charAt(4) == '1'){
       l = LOW;
    }else{
       l = HIGH;
    } if(c.charAt(9) == '1'){
       w = LOW;
    }else{
       w = HIGH;
  } if(c.charAt(14) == '1'){
       f = LOW;
    }else{
       f = HIGH;
    }
    digitalWrite(LightsRelay_2, l);
    digitalWrite(WaterRelay_3, w);
    delay(8000);
      if(w == LOW){
      digitalWrite(WaterRelay_3, HIGH);
       delay(8000);
      }
    digitalWrite(FanRelay_1, f);
    c = "";

 if(tempsensor.equals("On")){
   double humidity = sensor.readHumidity();
   double temperature = sensor.readTemperature();
   double tempfarenheit = (1.8 * temperature) + 32;
    //int humidity = sensor.readHumidity();
     //int temperature = sensor.readTemperature();
   /* Serial.print("H");*/ Serial.print(String(humidity)); Serial.print("|");
   /* Serial.print("T");*/ Serial.print(String(tempfarenheit)); Serial.print("\n");
    delay(300);
}
 }



