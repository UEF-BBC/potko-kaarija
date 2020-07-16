/*
Pötkökäärijä koodi ohjaa AIV-käärijää. 
Tavoite: Yhdellä käärijän kierroksella paali liikkuu 5cm +-2cm.

  * Paalia työntävän hydraulisylinterin ulostyöntymä mitataan UÄ-anturilla
  * Käärijän pyörähdys mitataan hall-anturilla ja kahdella magneetilla. 
      -> Kaksi magneetin ohitusta on yksi kierros
  * Optiona käärintämuovin katkeamisen mittaus joko ultraäänianturilla tai hall-anturilla ja magneetilla
  * Käärijää ohjataan kääntelemällä hydraulivipuja kahdella servolla.
  
  * Järjestelmän pitää osata säätää hydraulisylinterin ja käärijää pyörittävän hydraulisylinterin 
    välisen suhteellinen nopeus niin että Tavoite täyttyy.
*/

/*
  Hall-anturin lukeminen:
  - Luetaan attachInterrupt käskyllä
  - säästetään muutama edellinen arvo, jotta voidaan mitata nopeus.
  https://www.arduino.cc/reference/en/language/functions/external-interrupts/attachinterrupt/ 
*/

#include "SR04.h" //US anturin lukukoodi, löytyy 
//https://www.elegoo.com/tutorial/Elegoo%20The%20Most%20Complete%20Starter%20Kit%20for%20MEGA2560%20V2.0.2020.6.17.zip
//US anturin alta

#define TRIG_PIN 12 //US anturin trikkaus
#define ECHO_PIN 10 //US anturin luku

//US anturi
SR04 sr04 = SR04(ECHO_PIN,TRIG_PIN); //US-anturin luku
long d_sylinteri; //US anturin mittaama lukema mm tarkkuudella.

//Hall-anturin pinni
const byte interruptPin = 2; //Pinni
volatile long hallcount = 0; //Magneettien ohituslaskuri
unsigned long time = 0; 
long num = 0;

//Servot

//Laskennan muuttujat
float kierros = 0;
float suhde = 0;

void setup() {
  // put your setup code here, to run once:
   Serial.begin(9600);//Initialization of Serial Port

  // Hall-anturin luku
  attachInterrupt(digitalPinToInterrupt(interruptPin), hallanturi, RISING);
  time = millis(); 
}

void loop() {
  // put your main code here, to run repeatedly:
   d_sylinteri=sr04.Distance(); //US anturin mittaama lukema mm tarkkuudella.
      Serial.print(d_sylinteri);   Serial.println("mm");

  while (num != hallcount)
  {
    num = hallcount;
    kierros = hallcount/2;
  }

  //Sylinterin liikuttava 50mm/kierros +-20mm. 
  suhde = d_sylinteri/kierros;
    if ( d_sylinteri < 50*kierros - 20) {
    //nopeuta sylinteriä tai hidasta käärijää
    }
    else if ( d_sylinteri > 50*kierros + 20) {
    //hidasta sylinteriä tai nopeuta käärijää
    }


  //Kirjoita tuloksia
  Serial.println(kierros);

}

void hallanturi() {
    if ((millis() - time) > 100)
        hallcount ++;
    time = millis();
}
