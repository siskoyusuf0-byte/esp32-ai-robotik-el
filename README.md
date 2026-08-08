# ESP32 Yapay Zeka Destekli Robotik El Kontrol Sistemi

Bu proje, bilgisayar kamerası üzerinden alınan el hareketlerini görüntü işleme teknikleriyle analiz edip, elde edilen verileri eşzamanlı olarak ESP32 mikrokontrolcüsüne ileterek servo motor tabanlı bir mekanik sistemi kontrol eden yapay zeka destekli bir altyapıdır. Hareket takibi ve veri işleme süreçleri için OpenCV ve MediaPipe kütüphaneleri kullanılmıştır.

## Sistem Önizlemesi

![Robotik El Takibi](demo.gif)

## Temel Özellikler

- **Oto-Kalibrasyon Altyapısı:** Kullanıcının el anatomisini ve kameraya olan mesafesini başlangıç aşamasında analiz ederek, minimum ve maksimum servo açı sınırlarını dinamik olarak belirler.
- **Titreşim Önleyici Filtre (EMA):** Görüntüdeki anlık ışık değişimlerini ve istemsiz el titremelerini matematiksel yumuşatma (Exponential Moving Average) algoritmalarıyla sönümler.
- **3 Boyutlu Eklem Takibi:** Parmak bükülme oranını hesaplarken derinlik ($z$ ekseni) verilerini de sürece dahil ederek, üç boyutlu uzayda hassas konumlandırma sağlar.

## Kurulum ve Çalıştırma Adımları

### 1. Donanım (ESP32) Gereksinimleri
1. Servo motorun sinyal pinini ESP32 üzerinde **GPIO 27** pinine bağlayın.
2. Depoda bulunan `esp32_servo_kontrol.ino` dosyasını Arduino IDE aracılığıyla karta yükleyin.

### 2. Yazılım (Python) Gereksinimleri
Projenin çalışması için gereken kütüphaneleri komut satırı üzerinden sisteminize kurun:

```bash
pip install opencv-python mediapipe pyserial
```
Yapay zeka modelini ve takip sistemini başlatmak için aşağıdaki komutu çalıştırın:
```bash
python ai_el_takip.py

```
