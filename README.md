# ESP32 Yapay Zeka Destekli Robotik El Kontrol Sistemi

Bu proje, bilgisayar kamerası üzerinden alınan el hareketlerini görüntü işleme teknikleriyle analiz edip, elde edilen verileri eşzamanlı olarak ESP32 mikrokontrolcüsüne ileterek servo motor tabanlı bir mekanik sistemi kontrol eden yapay zeka destekli bir altyapıdır. Hareket takibi ve veri işleme süreçleri için OpenCV ve MediaPipe kütüphaneleri kullanılmıştır.

## Sistem Önizlemesi

<img width="476" height="848" alt="el_taklit_deneme-ezgif com-video-to-gif-converter (1)" src="https://github.com/user-attachments/assets/4d895cf5-ecc9-4821-a860-524a68f6d5a8" />

<img width="899" height="1599" alt="image" src="https://github.com/user-attachments/assets/e8185d78-3800-4ec0-83aa-72919b9b37aa" />
<img width="1080" height="1920" alt="image" src="https://github.com/user-attachments/assets/c854bced-1dff-4c76-9b6c-b1c7b7bf36bd" />


## Temel Özellikler

- **Oto-Kalibrasyon Altyapısı:** Kullanıcının el anatomisini ve kameraya olan mesafesini başlangıç aşamasında analiz ederek, minimum ve maksimum servo açı sınırlarını dinamik olarak belirler.
- **Titreşim Önleyici Filtre:** Görüntüdeki anlık ışık değişimlerini ve istemsiz el titremelerini matematiksel yumuşatma algoritmalarıyla sönümler.
- **3 Boyutlu Eklem Takibi:** Parmak bükülme oranını hesaplarken derinlik ($z$ ekseni) verilerini de sürece dahil ederek, üç boyutlu uzayda hassas konumlandırma sağlar.

  ## Kullanım Alanları ve Projenin Vizyonu

Bu proje, pahalı sensörlü eldivenlere veya karmaşık donanımlara ihtiyaç duymadan insan-makine etkileşimini sağlaması açısından stratejik bir öneme sahiptir. Projenin temelini oluşturduğu ve yol gösterici olduğu potansiyel uygulama alanları şunlardır:

- **Tehlikeli Ortam Operasyonları:** Radyoaktif bölgeler, kimyasal sızıntı alanları, arama-kurtarma veya bomba imha gibi insan hayatı için yüksek risk taşıyan ortamlarda, robotik kolların güvenli bir mesafeden insan hassasiyetiyle kontrol edilmesi.
- **Biyomedikal ve Akıllı Protez Geliştirme:** Kamera verisi ve yapay zeka aracılığıyla kontrol edilebilen, düşük maliyetli ve fiziksel sensör kısıtlaması olmayan erişilebilir biyonik protezlerin üretimine altyapı sağlaması.
- **Endüstri 4.0 ve İnsan-Makine Etkileşimi:** Akıllı fabrikalardaki otomasyon sistemlerinin ve işbirlikçi robotların, karmaşık kontrol panelleri yerine doğrudan operatörün el hareketleri ve jestleriyle sezgisel olarak yönetilmesi.
- **Akademik Araştırma ve Eğitim:** Bilgisayarlı görü, kinematik modelleme ve gömülü sistemler disiplinlerini bir araya getiren bu sistem, robotik alanında araştırma yapmak isteyen geliştiriciler için açık kaynaklı bir referans modelidir.

  ## Kullanılan Donanımlar

- ESP32 Geliştirme Kartı
- Servo Motor (SG90 / MG996R)
- 3D Yazıcı ile Üretilmiş / Hazır Mekanik Parmak Parçaları
- Jumper Kablolar ve Güç Kaynağı

## Mevcut Kısıtlamalar ve Geliştirme Yol Haritası 

Proje altyapısı tam bir robotik eli kontrol edecek şekilde tasarlanmış olsa da, mevcut donanım ve parça eksiklikleri sebebiyle prototip aşamasında **tek servo motor ve tek parmak** kullanılarak test edilmiştir. 

Gelecek güncellemelerde projeye eklenmesi planlanan özellikler şunlardır:
- **5 Parmak Entegrasyonu:** Gerekli donanım sağlandığında diğer parmakların da sisteme dahil edilmesi.
- **Kablosuz İletişim (Bluetooth/Wi-Fi):** USB Serial haberleşmesinin kaldırılarak, bilgisayar ile ESP32 arasındaki veri aktarımının Bluetooth veya Wi-Fi üzerinden kablosuz sağlanması.

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
