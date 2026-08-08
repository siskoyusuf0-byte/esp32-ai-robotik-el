#include <ESP32Servo.h>
#include <math.h>

Servo parmakServosu;
const int servoPin = 27;


const int ACI_MIN = 5;   
const int ACI_MAX = 90;  


enum Durum { OTOMATIK, DURDURULDU, MANUEL };
Durum mevcutDurum = OTOMATIK;


const unsigned long HAREKET_SURESI = 600; 
const unsigned long BEKLEME_SURESI = 400; 


int baslangicAci = ACI_MIN;
int hedefAci = ACI_MAX;
int mevcutAci = ACI_MIN;

unsigned long hareketBaslangicZamani = 0;
unsigned long beklemeBaslangicZamani = 0;
bool hareketEdiyor = true;

void setup() {
  Serial.begin(115200);

  ESP32PWM::allocateTimer(0);
  parmakServosu.setPeriodHertz(50);
  parmakServosu.attach(servoPin);

  parmakServosu.write(ACI_MIN);
  hareketBaslangicZamani = millis();

  Serial.println("==========================================");
  Serial.println("   DUR / BAŞLA KONTROLLÜ İNSANSI EL");
  Serial.println("==========================================");
  Serial.println("-> 'dur'   : Hareketi anında durdurur.");
  Serial.println("-> 'başla' : Hareketi kaldığı yerden başlatır.");
  Serial.println("-> 5 - 90  : İstenen açıya sabitler.");
  Serial.println("==========================================");
}

void loop() {
  
  if (Serial.available() > 0) {
    String girdi = Serial.readStringUntil('\n');
    girdi.trim();
    girdi.toLowerCase(); 

    
    if (girdi == "dur") {
      mevcutDurum = DURDURULDU;
      Serial.println("\n[SİSTEM] -> Parmak DURDURULDU.");
    } 
    
    else if (girdi == "başla" || girdi == "basla" || girdi == "a") {
      if (mevcutDurum != OTOMATIK) {
        mevcutDurum = OTOMATIK;
        hareketEdiyor = true;
        baslangicAci = mevcutAci;
        hareketBaslangicZamani = millis();
        Serial.println("\n[SİSTEM] -> Otomatik insansı hareket BAŞLATILDI.");
      }
    } 
    
    else {
      int girilenAci = girdi.toInt();
      if (girilenAci >= ACI_MIN && girilenAci <= ACI_MAX) {
        mevcutDurum = MANUEL;
        mevcutAci = girilenAci;
        parmakServosu.write(mevcutAci);
        Serial.print("\n[SİSTEM] -> MANUEL MOD | Açı: ");
        Serial.print(mevcutAci);
        Serial.println("°");
      }
    }
  }

  
  if (mevcutDurum == OTOMATIK) {
    unsigned long suankiZaman = millis();

    if (hareketEdiyor) {
      unsigned long gecenSure = suankiZaman - hareketBaslangicZamani;

      if (gecenSure >= HAREKET_SURESI) {
        mevcutAci = hedefAci;
        parmakServosu.write(mevcutAci);
        
        hareketEdiyor = false;
        beklemeBaslangicZamani = suankiZaman;
      } 
      else {
        
        float ilerleme = (float)gecenSure / HAREKET_SURESI;
        float yumusakIlerleme = (1.0 - cos(ilerleme * M_PI)) / 2.0;
        
        mevcutAci = baslangicAci + (hedefAci - baslangicAci) * yumusakIlerleme;
        parmakServosu.write(mevcutAci);
      }
    } 
    else {
      
      if (suankiZaman - beklemeBaslangicZamani >= BEKLEME_SURESI) {
        baslangicAci = mevcutAci;
        hedefAci = (hedefAci == ACI_MAX) ? ACI_MIN : ACI_MAX;
        
        hareketBaslangicZamani = suankiZaman;
        hareketEdiyor = true;
      }
    }
  }
}
