/* This code is to be used with KY-024 Hall effect sensor
 * It displays both Analog and Digital values given by the sensor
 * Refer to www.surtrtech.com for more details
 */
 //koodi kopsittu
 // https://create.arduino.cc/projecthub/SurtrTech/interfacing-hall-effect-sensor-with-arduino-ee3bbe

#define Hall_Sensor A0          //A0 used with analog output, D2 with digital output
#define HALL_PIN A1 //Hall-anturin luku

int Val1=0,Val2=0;             //Here you can store both values, the Val2 can be boolean


void setup() {
  Serial.begin(9600);
  pinMode(HALL_PIN,INPUT);
 

}

void loop() {
  
   Val1=analogRead(Hall_Sensor);            //We read both values and display them raw on the serial monitor
   Serial.print(Val1);
   Val2=digitalRead(HALL_PIN);
   Serial.print("\t");
   Serial.println(Val2);

   delay(500);
}
