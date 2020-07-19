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

#include <Servo.h>

#define TRIG_PIN 12 //US anturin trikkaus
#define ECHO_PIN 10 //US anturin luku
#define HALL_PIN 2 //Hall-anturin luku
#define SYL_PIN 3 //Hydraylisylinterin ohjaus
#define MOOT_PIN 4 //Hydraulimoottorin ohjaus
#define SYLINTERI_MAX 1400 //Hydraulisylinterin maksimipituus
#define SYLINTERI_MIN 200 //Hydraulisylinterin minimipituus

//Pysäytys
boolean STOP = false;
boolean AJA = false;

//US anturi
SR04 sr04 = SR04(ECHO_PIN,TRIG_PIN); //US-anturin luku
long d_sylinteri = 0; //US anturin mittaama lukema mm tarkkuudella.
long d_sylinteri_vanhempi; //US anturin mittaama lukema mm tarkkuudella.
long d_sylinteri_vanhin; //US anturin mittaama lukema mm tarkkuudella.

//Hall-anturin pinni
const byte interruptPin = HALL_PIN; //Pinni
volatile long hallcount = 0; //Magneettien ohituslaskuri
unsigned long time = 0; 
long num = 0;

//Servot
Servo sylinteri;
Servo moottori;
int s_asento[5] = {90, 104, 120, 139, 180};
int m_asento[5] = {90, 104, 120, 139, 180};
int s_nopeus = 0; //välillä 0-4
int m_nopeus = 0; //välillä 0-4

//Laskennan muuttujat
float kierros = 1;
float suhde = 0;
long tyhjamm = 200;
long paaliliike = 0;

void setup() {
  // put your setup code here, to run once:
   Serial.begin(9600);//Initialization of Serial Port

  // Hall-anturin luku
  attachInterrupt(digitalPinToInterrupt(interruptPin), hallanturi, RISING);
  time = millis(); 

  //Servo
  sylinteri.attach(SYL_PIN);// Keskimmäinen servon johto SYL_PIN pinniin
  moottori.attach(MOOT_PIN);// Keskimmäinen servon johto MOOT_PIN pinniin
  sylinteri.write(90);// Servo keskiasentoon -> 90°
  moottori.write(90);// Servo keskiasentoon -> 90°
}


// ------------PÄÄ LOOPPI -----------------------------------------
void loop() {

  // put your main code here, to run repeatedly:
   d_sylinteri_vanhin =   d_sylinteri_vanhempi;//Otetaan vanhat arvot ylös
   d_sylinteri_vanhempi = d_sylinteri;
   d_sylinteri=sr04.Distance(); //US anturin mittaama lukema mm tarkkuudella.


  //Lähde ajamaan kun tulee käsky ifrapunasensorilta
  while(AJA)
  { 
    
   
   Serial.print(d_sylinteri);   Serial.print("mm ");
   paaliliike = d_sylinteri - tyhjamm;
   Serial.print(paaliliike);   Serial.print("mm ");

  while (num != hallcount)
  {
    num = hallcount;
    kierros = float(hallcount)/2;

  //Sylinterin liikuttava 50mm/kierros +-20mm. 
  suhde = paaliliike/kierros;
    if ( paaliliike < kierros*50 - 20) {
    //nopeuta sylinteriä tai hidasta käärijää
    Serial.print(" Liian vähän ");
    if (s_nopeus < 4 )
        s_nopeus ++;
    else if (m_nopeus > 0 )
        m_nopeus --;
    }
    else if ( paaliliike > kierros*50 + 20) {
    //hidasta sylinteriä tai nopeuta käärijää
    Serial.print(" Liikaa ");
    if (s_nopeus > 0 )
        s_nopeus --;
    else if (m_nopeus < 4 )
        m_nopeus ++;
    }
    else {
    Serial.print(" Hyvä ");
    }
    //Käännä servot
    sylinteri.write(s_asento[s_nopeus]);// move servos to center position -> 90°
    moottori.write(m_asento[m_nopeus]);// move servos to center position -> 60°
  }

  //Kirjoita tuloksia
  Serial.print(hallcount);Serial.print(" ");Serial.print(kierros);
  Serial.print(" ");Serial.print(kierros*50);

  //Sylinterin liikuttava 50mm/kierros +-20mm. 
  suhde = paaliliike/kierros;
    if ( paaliliike < kierros*50 - 20) {
    //nopeuta sylinteriä tai hidasta käärijää
    Serial.print(" Liian vähän ");
    }
    else if ( paaliliike > kierros*50 + 20) {
    //hidasta sylinteriä tai nopeuta käärijää
    Serial.print(" Liikaa ");
    }
    else {
    Serial.print(" Hyvä ");
    }
  
  //Kirjoita tuloksia
  Serial.print(" ");Serial.println("");



  if (false){
  sylinteri.write(90);// move servos to center position -> 90°
  delay(500);
  sylinteri.write(60);// move servos to center position -> 60°
  delay(500);
  moottori.write(90);// move servos to center position -> 90°
  delay(500);
  moottori.write(60);// move servos to center position -> 60°
  }
  

  }

  delay(500);


  //Jos ajaa perille, pysäytä
  if (d_sylinteri > SYLINTERI_MAX) {
    sylinteri.write(0);
    moottori.write(90);
    delay(5000); //aja alkuasentoon
    sylinteri.write(90);

    STOP = true;
    }

  if (STOP) {
    moottori.write(90);
    sylinteri.write(90);
    delay(1000);
    cli();
    while(1);
    }
  //sleep_enable();
  //sleep_cpu();

}

void hallanturi() {
    if ((millis() - time) > 100)
        hallcount ++;
    time = millis();
}
