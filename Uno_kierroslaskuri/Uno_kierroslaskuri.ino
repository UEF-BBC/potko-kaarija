#include <LiquidCrystal.h>  //LCD näytön ohjauskirjasto
#define Hall_Sensor A0          //A0 Luetaan Hall-anturin arvo pinnistä A0
#define HALL_PIN 2 //Hall-anturin digitaalisen arvon luku A1 pinnistä 
#define Nmuisti 5 // Ota talteen N viimeisintä arvoa ja kellonaikaa


//Alusta lcd näyttö
LiquidCrystal lcd(12, 11, 5, 4, 6, 7);  //LCD-näyttöä ohjataan pinneillä 12,11,5,4,6,7
int laskurivanha = 0; //Päivitä näyttö kun mangeetti ohittanut hall-anturin


//Kierrosluvun laskemista
int Nmagneetit = 1; //Magneettien lukumäärä per kierros 
volatile unsigned long aika; // aika millisekunneissa arduinon käynnistymisestä. Nollautuu 50 päivän välein. 
unsigned long aAjat_ms[Nmuisti];  //Ajanhetket, jolloin magneetti ohittaa Hall-anturin
float rps = 0; //kierrosnopeus sekunneissa;
int laskuri = 0; //Ohitusten lukumäärä


// put your setup code here, to run once:
void setup() {

  //Hall anturin alustusta
  pinMode(HALL_PIN,INPUT);

  //Kierroslaskennan alustusta
  aika = millis(); // aika millisekunneissa arduinon käynnistymisestä. 
  laskuri = 0;
  for (int i = 0; i < Nmuisti; i = i + 1) {  // Alusta arrayn muuttujat
    aAjat_ms[i] = aika + i*3000; //Laitetaan suht isot arvot alkuun, jotta pyöriminen määriteltäisiin hitaaksi
  }

  //Interruptin alustus
  attachInterrupt(digitalPinToInterrupt(HALL_PIN), magneetinOhitus, RISING);

  //Sarjaportin alustus
   Serial.begin(9600);
  
}


//Skriptin funktiot 
void magneetinOhitus() {  //ajetaan kun interrupt tapahtuu
  aika = millis(); // aika millisekunneissa arduinon käynnistymisestä. Huom. millis ei päivity interruptin sisällä, mutta interrupt on niin nopea, että tämän ei pitäisi haitata
}


// put your main code here, to run repeatedly:
void loop() {

   if (aAjat_ms[0]+100 <aika) { //Estetään, että yhtä magneetin ohitusta ei lasketa monesti.
     for (int i = Nmuisti - 1; i > 0; i = i - 1) {
       aAjat_ms[i] = aAjat_ms[i-1]; //Siirretään arvoja yhdellä eteenpäin
     }
     aAjat_ms[0] = aika;
     laskuri = laskuri + 1;
     rps = ( float(Nmuisti) / float(Nmagneetit) )/(float( aAjat_ms[0] - aAjat_ms[Nmuisti-1] ) /1000 );
   }

   //Kirjoitus sarjaporttiin
   if ( laskurivanha != laskuri ) {
     Serial.print(rps);
     Serial.println(" kierrosta sekunnissa");
   }

   //LCD näytön päivitys
   if ( laskurivanha != laskuri ) {
     laskurivanha = laskuri;
     lcd.setCursor(0,0);
     lcd.print(aAjat_ms[0]/1000);
     lcd.print(" ");
     lcd.print(aAjat_ms[Nmuisti-1]/1000);
     lcd.print(" ");
     lcd.print(laskuri);
     lcd.print(" ");
     lcd.print(rps);
   }

}
