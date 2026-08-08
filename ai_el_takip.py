import cv2
import mediapipe as mp
import serial
import time
import math


SERIAL_PORT = 'COM6'
BAUD_RATE = 115200

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
    time.sleep(2)
    print(f"[BAŞARILI] {SERIAL_PORT} portuna bağlandı.")
except Exception as e:
    print(f"[HATA] Seri porta bağlanılamadı: {e}")
    ser = None


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    model_complexity=1,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)


ACI_MIN = 5   
ACI_MAX = 90  


durum = "BEKLEME_ACIK"
zamanlayici_baslangic = time.time()
acik_oranlar = []
kapali_oranlar = []
MIN_ORAN = 0.20  
MAX_ORAN = 0.85  


yumusatilmis_aci = float(ACI_MIN)
ALPHA = 0.25
son_gonderilen_aci = -1

cap = cv2.VideoCapture(0)
print("--- OTO-KALİBRASYONLU EL TAKİBİ BAŞLATILDI ---")

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)
    
    oran = None

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            pt_tip = hand_landmarks.landmark[8]
            pt_mcp = hand_landmarks.landmark[5]
            pt_wrist = hand_landmarks.landmark[0]

            parmak_mesafesi = math.sqrt((pt_tip.x - pt_mcp.x)**2 + (pt_tip.y - pt_mcp.y)**2 + (pt_tip.z - pt_mcp.z)**2)
            referans_mesafe = math.sqrt((pt_mcp.x - pt_wrist.x)**2 + (pt_mcp.y - pt_wrist.y)**2 + (pt_mcp.z - pt_wrist.z)**2)

            oran = parmak_mesafesi / (referans_mesafe + 1e-6)

    
    su_an = time.time()
    gecen_sure = su_an - zamanlayici_baslangic

    if durum == "BEKLEME_ACIK":
        cv2.putText(image, "1. ADIM: Elini TAM ACIK Tut! (3 Sn)", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        if gecen_sure > 3:
            durum = "KAYIT_ACIK"
            zamanlayici_baslangic = su_an
            
    elif durum == "KAYIT_ACIK":
        cv2.putText(image, "ACIK el olculuyor. Sabit tut...", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        if oran is not None:
            acik_oranlar.append(oran)
        if gecen_sure > 2:
            durum = "BEKLEME_KAPALI"
            zamanlayici_baslangic = su_an
            
    elif durum == "BEKLEME_KAPALI":
        cv2.putText(image, "2. ADIM: Isaret Parmagini BUK! (3 Sn)", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        if gecen_sure > 3:
            durum = "KAYIT_KAPALI"
            zamanlayici_baslangic = su_an
            
    elif durum == "KAYIT_KAPALI":
        cv2.putText(image, "KAPALI el olculuyor. Sabit tut...", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        if oran is not None:
            kapali_oranlar.append(oran)
        if gecen_sure > 2:
            
            if len(acik_oranlar) > 0 and len(kapali_oranlar) > 0:
                MAX_ORAN = sum(acik_oranlar) / len(acik_oranlar)
                MIN_ORAN = sum(kapali_oranlar) / len(kapali_oranlar)
                print(f"Kalibrasyon Tamam! MIN: {MIN_ORAN:.2f} | MAX: {MAX_ORAN:.2f}")
            durum = "TAKIP_MODU"

    elif durum == "TAKIP_MODU":
        if oran is not None:
            
            norm_oran = max(MIN_ORAN, min(MAX_ORAN, oran))
            ham_aci = ACI_MAX - ((norm_oran - MIN_ORAN) / (MAX_ORAN - MIN_ORAN + 1e-6)) * (ACI_MAX - ACI_MIN)

            
            yumusatilmis_aci = (ALPHA * ham_aci) + ((1.0 - ALPHA) * yumusatilmis_aci)
            son_aci = int(yumusatilmis_aci)

            if abs(son_aci - son_gonderilen_aci) >= 2:
                son_gonderilen_aci = son_aci
                if ser and ser.is_open:
                    komut = f"{son_aci}\n"
                    ser.write(komut.encode())

            cv2.putText(image, f"Servo Aci: {son_aci} deg", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.putText(image, f"Oran: {oran:.2f}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

    cv2.imshow('Oto-Kalibrasyonlu El Takibi', image)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
if ser:
    ser.close()
