#include "SR04.h"

#define TRIG_PIN 8
#define ECHO_PIN 9 
#define Nmuisti 5 // Ota talteen N viimeisintä mittausarvoa
#define DEBUG 0

//Alusta ultraäänianturi
SR04 sr04 = SR04(ECHO_PIN,TRIG_PIN);
long a; //US anturin mittaama lukema cm tarkkuudella.
long aMittaukset[Nmuisti];  //Viimeiset Nmuisti mittausta
long average = 0;
int errorcount = 0;
int counter = 0;

void setup() {
   Serial.begin(9600);//Initialization of Serial Port
   delay(1000);

  for (int i = 0; i < Nmuisti; i = i + 1) {  // Alusta arrayn muuttujat
    aMittaukset[i] = 0; //Laitetaan alkuun arvot nolla
  }

}

int keskiarvo() {
   //Laske keskiarvo
   int total = 0;
   for (int i = 0; i < Nmuisti; i = i + 1) {
     total = total + aMittaukset[i];
   }
   int ave = total/Nmuisti;
   return ave;
  }


void paivita_muisti() {
   for (int i = Nmuisti - 1; i > 0; i = i - 1) {
     aMittaukset[i] = aMittaukset[i-1]; //Siirretään arvoja yhdellä eteenpäin
   }
   aMittaukset[0] = a;
 }  
 
///////////////////////////////////////////////////////////////////////////////////////////
void loop() {
  counter = counter + 1;
   delay(200);

  //Mitttaa etäisyys ultraäänianturilla
   a=sr04.Distance();

   //Mittausarvojen pitäisi muuttua aika tasaisesti. Jos on iso hyppy niin hylkää mittaus
   average = keskiarvo();
   if (DEBUG){
     Serial.print(average);
     Serial.println(" Keskiarvo");
   }

   //Tarkista, että average ja uusi mittaus eivät eroa liian paljon (yli 10 cm)
   int tolerance = 10;
   if (average - tolerance < a && average + tolerance > a) {

     paivita_muisti();
    
    }
    else {
      if (DEBUG) {  
        Serial.println("Toleranssin ulkopuolella"); 
        }
       errorcount = errorcount + 1;
       //Jos virhemittaus toistuu monesti niin silloin se on varmaankin oikea mittaus.
       if (errorcount >= Nmuisti) {
        errorcount = 0;
        paivita_muisti();
        }
      }


   //kirjoita mittaustulos sarjaporttiin
   Serial.print(aMittaukset[0]);
   Serial.print(" cm  Counter = ");//The difference between "Serial.print" and "Serial.println" is that "Serial.println" can change lines.
   Serial.println(counter);
}
