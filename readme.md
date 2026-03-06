# 🚗 Automatic Gate System with License Plate Recognition

Project ini merupakan **prototipe sistem gerbang otomatis berbasis kamera** yang menggunakan teknologi **Computer Vision** untuk mendeteksi dan membaca plat nomor kendaraan secara otomatis.

Sistem ini memanfaatkan kombinasi **YOLOv8** sebagai algoritma **object detection** untuk mendeteksi kendaraan dan plat nomor, serta **Tesseract-OCR** untuk melakukan **pembacaan teks pada plat nomor kendaraan**.

Hasil identifikasi kendaraan kemudian digunakan untuk mengontrol **gerbang otomatis melalui modul Wemos (ESP8266)** yang berfungsi sebagai pengendali aktuator. Sistem ini memungkinkan gerbang untuk **terbuka dan tertutup secara otomatis berdasarkan hasil deteksi kendaraan secara real-time**.

Prototipe ini dirancang sebagai solusi **akses gerbang modern berbasis kecerdasan buatan** yang mampu meningkatkan **keamanan, efisiensi, dan otomatisasi pada sistem akses kendaraan**.

Project ini dikembangkan sebagai bagian dari **project semester 5 pada bidang Computer Vision dan Internet of Things (IoT)**.

---

# 🚀 Features

Beberapa fitur utama dalam sistem ini antara lain:

### 🎥 Deteksi Kendaraan dan Plat Nomor
Sistem menggunakan **YOLOv8** untuk mendeteksi kendaraan dan plat nomor secara real-time melalui kamera.

### 🔎 Pembacaan Plat Nomor
Setelah plat nomor terdeteksi, sistem menggunakan **Tesseract OCR** untuk membaca teks pada plat nomor kendaraan.

### 🚪 Gerbang Otomatis
Jika plat nomor kendaraan dikenali, sistem akan mengirimkan perintah ke **modul Wemos (ESP8266)** untuk membuka gerbang secara otomatis.

### ⚡ Real-time Processing
Sistem mampu memproses deteksi kendaraan dan pembacaan plat nomor secara **real-time**.

### 📡 Integrasi IoT
Wemos berfungsi sebagai **penghubung antara sistem deteksi dan aktuator gerbang**.

### 🧠 Computer Vision Based System
Menggunakan teknologi **Artificial Intelligence dan Computer Vision** untuk meningkatkan efisiensi sistem akses kendaraan.

---

# 🛠 Tech Stack

Teknologi yang digunakan dalam pengembangan sistem ini:

| Technology | Description |
|-----------|-------------|
| Python | Bahasa pemrograman utama |
| YOLOv8 | Model object detection |
| OpenCV | Pengolahan citra dan video |
| Tesseract OCR | Pembacaan teks pada plat nomor |
| Wemos ESP8266 | Mikrokontroler untuk pengendali gerbang |
| Arduino IDE | Pemrograman Wemos |
| Camera Module | Input visual untuk sistem |

---

# 📂 Project Structure

Struktur folder utama pada project:

```
automatic-gate-lpr
│
├── dataset
│   ├── images
│   └── labels
│
├── models
│   └── yolov8_plate_model.pt
│
├── scripts
│   ├── detect_plate.py
│   ├── ocr_reader.py
│   └── gate_controller.py
│
├── arduino
│   └── wemos_gate_control.ino
│
├── results
│   └── detection_output
│
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

Ikuti langkah berikut untuk menjalankan project secara lokal.

### 1. Clone Repository

```bash
git clone https://github.com/username/automatic-gate-lpr.git
```

### 2. Masuk ke Folder Project

```bash
cd automatic-gate-lpr
```

### 3. Install Dependency Python

```bash
pip install -r requirements.txt
```

---

### 4. Install Tesseract OCR

Download dan install Tesseract OCR:

```
https://github.com/tesseract-ocr/tesseract
```

Tambahkan path Tesseract ke environment variable.

---

### 5. Jalankan Sistem Deteksi

```bash
python detect_plate.py
```

Sistem akan memproses input dari kamera dan mendeteksi plat nomor kendaraan.

---

# 📡 Hardware Integration

Sistem ini terintegrasi dengan **Wemos ESP8266** untuk mengontrol gerbang otomatis.

Alur sistem:

1. Kamera mendeteksi kendaraan
2. YOLOv8 mendeteksi plat nomor
3. Tesseract membaca teks plat nomor
4. Sistem memverifikasi plat nomor
5. Perintah dikirim ke **Wemos**
6. Gerbang terbuka secara otomatis

---

# 📸 System Workflow

Alur kerja sistem:

```
Camera Input
      ↓
YOLOv8 Detection
      ↓
Plate Cropping
      ↓
Tesseract OCR
      ↓
Plate Verification
      ↓
Send Signal to Wemos
      ↓
Automatic Gate Open
```

---

# 🎯 Project Goals

Tujuan utama dari pengembangan sistem ini:

- Mengembangkan sistem **Automatic License Plate Recognition (ALPR)**
- Mengintegrasikan teknologi **Computer Vision dengan IoT**
- Meningkatkan keamanan dan efisiensi sistem akses kendaraan
- Menerapkan teknologi AI pada sistem gerbang otomatis

---

# 📸 Application Preview

![alt text](https://github.com/Jimmy-hubb/Mobile-Cuan-Space-Semester-4/blob/main/assets/WhatsApp%20Image%202026-03-02%20at%2020.06.57.jpeg?raw=true)


---