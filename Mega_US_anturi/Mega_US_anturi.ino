//www.elegoo.com
//2016.12.08
#include "SR04.h"

#define TRIG_PIN 8
#define ECHO_PIN 9 

SR04 sr04 = SR04(ECHO_PIN,TRIG_PIN);
long a; //US anturin mittaama lukema mm tarkkuudella.

void setup() {
   Serial.begin(9600);//Initialization of Serial Port
   delay(1000);
}

void loop() {
   a=sr04.Distance();
   Serial.print(a);
   Serial.println(" cm");//The difference between "Serial.print" and "Serial.println" is that "Serial.println" can change lines.
   delay(500);
}
