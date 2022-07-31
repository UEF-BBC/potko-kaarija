#include <LiquidCrystal.h>

#define Hall_Sensor A0          //A0 used with analog output, D2 with digital output
#define HALL_PIN A1 //Hall-anturin luku

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

const int switchPin = 6;
int switchState = 0;
int prevSwitchState = 0;
int reply;
int tictoc = 0;

//Hall anturin asetukset

int Val1=0,Val2=0;             //Here you can store both values, the Val2 can be boolean



void setup() {
  // put your setup code here, to run once:
  lcd.begin(16, 2);
  pinMode(switchPin, INPUT);
  lcd.print("Hei vaan");
  //lcd.setCursor(0,1);
  //lcd.print("Rivi 2.  123");

  pinMode(HALL_PIN,INPUT);


}

void loop() {
  // put your main code here, to run repeatedly:
  if (tictoc == 0) {
    tictoc = 1;
    lcd.setCursor(0,0);
    lcd.print("tic 0    ");
    }
  else {
    tictoc = 0;
    lcd.setCursor(0,0);
    lcd.print("toc 1    ");
    }
  delay(500);

    //Hall-anturi
    lcd.setCursor(0,1);

   Val1=analogRead(Hall_Sensor);            //We read both values and display them raw on the serial monitor
   lcd.print(Val1);
   Val2=digitalRead(HALL_PIN);
   lcd.print("   ");
   lcd.print(Val2);


}
