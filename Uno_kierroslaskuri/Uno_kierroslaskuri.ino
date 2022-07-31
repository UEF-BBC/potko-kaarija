#include <LiquidCrystal.h>  //LCD näytön ohjauskirjasto
#define Hall_Sensor A0          //A0 Luetaan Hall-anturin arvo pinnistä A0
#define HALL_PIN 2 //Hall-anturin digitaalisen arvon luku A1 pinnistä 
#define Nmuisti 5 // Ota talteen N viimeisintä arvoa ja kellonaikaa

//Alusta lcd näyttö
LiquidCrystal lcd(12, 11, 5, 4, 6, 7);  //LCD-näyttöä ohjataan pinneillä 12,11,5,4,6,7
int laskurilcd = 0; //Päivitä näyttö kun mangeetti ohittanut hall-anturin


//Kierrosluvun laskemista
int Nmagneetit = 1; //Magneettien lukumäärä per kierros 
volatile unsigned long aika; // aika millisekunneissa arduinon käynnistymisestä. Nollautuu 50 päivän välein. 
unsigned long iAjat_ms[Nmuisti];  //Ajanhetket, jolloin magneetti ohittaa Hall-anturin
float rps = 0; //kierrosnopeus sekunneissa;
int laskuri = 0; //Ohitusten lukumäärä

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
   
}

void magneetinOhitus() {
  aika = millis(); // aika millisekunneissa arduinon käynnistymisestä. 
}
