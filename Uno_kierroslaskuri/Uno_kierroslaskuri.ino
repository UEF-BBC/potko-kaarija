#include <LiquidCrystal.h>  //LCD näytön ohjauskirjasto
#include "SR04.h"
#define Hall_Sensor A0          //A0 Luetaan Hall-anturin arvo pinnistä A0
#define HALL_PIN 2 //Hall-anturin digitaalisen arvon luku A1 pinnistä 
#define Nmuisti 5 // Ota talteen N viimeisintä arvoa ja kellonaikaa

//Ultraäänianturi
#define TRIG_PIN 8
#define ECHO_PIN 9 


//Alusta lcd näyttö
LiquidCrystal lcd(12, 11, 5, 4, 6, 7);  //LCD-näyttöä ohjataan pinneillä 12,11,5,4,6,7
int laskurilcd = 0; //Päivitä näyttö kun mangeetti ohittanut hall-anturin


//Kierrosluvun laskemista
int Nmagneetit = 1; //Magneettien lukumäärä per kierros 
volatile unsigned long aika; // aika millisekunneissa arduinon käynnistymisestä. Nollautuu 50 päivän välein. 
unsigned long iAjat_ms[Nmuisti];  //Ajanhetket, jolloin magneetti ohittaa Hall-anturin
float rps = 0; //kierrosnopeus sekunneissa;
int laskuri = 0; //Ohitusten lukumäärä

//Ultraäänianturi
SR04 sr04 = SR04(ECHO_PIN,TRIG_PIN);
long a; //US anturin mittaama lukema mm tarkkuudella.

void setup() {
  // put your setup code here, to run once:

  //Hall anturin alustusta
  pinMode(HALL_PIN,INPUT);

  //Kierroslaskennan alustusta
  aika = millis(); // aika millisekunneissa arduinon käynnistymisestä. 
  laskuri = 0;
  for (int i = 0; i < Nmuisti; i = i + 1) {
    iAjat_ms[i] = aika + i*3000; //Laitetaan suht isot arvot alkuun, jotta pyöriminen määriteltäisiin hitaaksi
  }

  //Interruptin alustus
  attachInterrupt(digitalPinToInterrupt(HALL_PIN), magneetinOhitus, RISING);

   // Ultraäänianturi
   Serial.begin(9600);//Initialization of Serial Port
   delay(1000);
  
}

void loop() {
  // put your main code here, to run repeatedly:


   if (iAjat_ms[0]+100 <aika) { //Estetään, että yhtä magneetin ohitusta ei lasketa monesti.
     for (int i = Nmuisti - 1; i > 0; i = i - 1) {
       iAjat_ms[i] = iAjat_ms[i-1]; //Siirretään arvoja yhdellä eteenpäin
     }
     iAjat_ms[0] = aika;
     laskuri = laskuri + 1;
     rps = ( float(Nmuisti) / float(Nmagneetit) )/(float( iAjat_ms[0] - iAjat_ms[Nmuisti-1] ) /1000 );
   }

   //LCD näytön päivitys
   if ( laskurilcd != laskuri ) {
     laskurilcd = laskuri;

     lcd.setCursor(0,0);

 
     lcd.print(iAjat_ms[0]/1000);
     lcd.print(" ");
     lcd.print(iAjat_ms[Nmuisti-1]/1000);
     lcd.print(" ");
     lcd.print(laskuri);
     lcd.print(" ");
     lcd.print(rps);
   }



//Ultraäänianturi  
   a=sr04.Distance();
   Serial.print(a);
   Serial.println("mm");//The difference between "Serial.print" and "Serial.println" 
                        //is that "Serial.println" can change lines.
   delay(500);
   
}

void magneetinOhitus() {
  aika = millis(); // aika millisekunneissa arduinon käynnistymisestä. 
}
