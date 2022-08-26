#include "Adafruit_VL53L0X.h"
Adafruit_VL53L0X lox = Adafruit_VL53L0X();
void setup() {
 Serial.begin(9600);
 while (! Serial) {
 delay(1);
 }
 Serial.println("VL53L0X sensor test");
 if (!lox.begin()) {
 Serial.println(F("Failed to boot VL53L0X"));
 while (1);
 }
}
void loop() {
 VL53L0X_RangingMeasurementData_t measure;
 Serial.print("Reading measurement - ");
 lox.rangingTest(&measure, false);
 if (measure.RangeStatus != 4) {
 Serial.print("Distance (mm): ");
 Serial.println(measure.RangeMilliMeter);
 } else {
 Serial.println("Out of range!");
 }
 delay(1000);
}
