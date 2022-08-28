/*
 SerialPassthrough sketch
 with SoftwareSeral option

 created in August 2019 for WiFiEspAT library
 by Juraj Andrassy https://github.com/jandrassy
 */

 /*
 Perus AT käskyjä
 AT
 AT+CWMODE?
 AT+CWSTATE?
 AT+CWJAP
 AT+CIPSTART="TCP","192.168.48.249",5555
 AT+CIPSEND=5
 hello
 AT+CIPCLOSE
  */

//#define SAMD_FLOW_CONTROL

//Alusta ESP8266
#define SerialAT Serial1
#define AT_BAUD_RATE 115200

//Alusta GY521
#include "GY521.h"
GY521 sensor(0x68);
uint32_t counter = 0;

void setup() {

  Serial.begin(115200);
  while (!Serial);

  //Alusta ESP8266
  SerialAT.begin(AT_BAUD_RATE);

  //Alusta GY521
  Serial.println();
  Serial.println(__FILE__);
  Serial.print("GY521_LIB_VERSION: ");
  Serial.println(GY521_LIB_VERSION);

  Wire.begin();

  delay(100);
  while (sensor.wakeup() == false)
  {
    Serial.print(millis());
    Serial.println("\tCould not connect to GY521");
    delay(1000);
  }
  sensor.setAccelSensitivity(2);  // 8g
  sensor.setGyroSensitivity(1);   // 500 degrees/s

  sensor.setThrottle();
  Serial.println("start...");

  // set calibration values from calibration sketch.
  /*
  sensor.axe = 0.574;
  sensor.aye = -0.002;
  sensor.aze = -1.043;
  sensor.gxe = 10.702;
  sensor.gye = -6.436;
  sensor.gze = -0.676;
  */
  sensor.axe = 0.0218555;
  sensor.aye = -0.0054102;
  sensor.aze = -0.9415015;
  sensor.gxe = 2.7876336;
  sensor.gye = -0.8454962;
  sensor.gze = 1.2333587;

}

void loop() {

  sensor.read();
  float pitch = sensor.getPitch();
  float roll  = sensor.getRoll();
  float yaw   = sensor.getYaw();

  //Kirjoita serial OUTiin.
  if (counter % 10000 == 0)
  {
    Serial.println("\nCNT\tPITCH\tROLL\tYAW");
  }

  if (counter % 1000 == 0)
  {
  Serial.print(counter);
  Serial.print('\t');
  Serial.print(pitch, 3);
  Serial.print('\t');
  Serial.print(roll, 3);
  Serial.print('\t');
  Serial.print(yaw, 3);
  Serial.println();
  }
  counter++;

  if (counter % 10000 == 0)
  {
  /*if (SerialAT.available()) {
    Serial.write(SerialAT.read());
  }*/

    
    SerialAT.println("AT+CIPSTART=\"TCP\",\"192.168.48.249\",5555");
    SerialAT.println("AT+CIPSEND=5");
    SerialAT.println("hello");
    SerialAT.println("AT+CIPCLOSE");

    Serial.println("AT+CIPSTART=\"TCP\",\"192.168.48.249\",5555");
    Serial.println("AT+CIPSEND=5");
    Serial.println("hello");
    Serial.println("AT+CIPCLOSE");
  }
  
  /*
  while (Serial.available()) {
    SerialAT.write(Serial.read());
  }
  while (SerialAT.available()) {
    Serial.write(SerialAT.read());
  }
  */
}

#if defined(ARDUINO_ARCH_SAMD) && defined(SAMD_FLOW_CONTROL)
void SERCOM3_Handler() {
  SerialAT.IrqHandler();
}
#endif
