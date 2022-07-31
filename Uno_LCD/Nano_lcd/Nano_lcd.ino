#include <LiquidCrystal.h>
LiquidCrystal lcd(12, 11, 5, 4, 6, 7);

const int switchPin = 6;
int switchState = 0;
int prevSwitchState = 0;
int reply;
int tictoc = 0;

void setup() {
  // put your setup code here, to run once:
  lcd.begin(16, 2);
  lcd.print("Hei vaan");
  lcd.setCursor(0,1);
  lcd.print("Rivi 2.  123");

  lcd.print(" 4 ertyuioop");

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

}
