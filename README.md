# Analisis Statistik Kompresi JPEG: Linearitas vs Eksponensial

[![Language](https://img.shields.io/badge/Language-Python_3.8%2B-blue.svg)](https://www.python.org/)
[![Analysis](https://img.shields.io/badge/Analysis-R_Language-blue.svg)](https://www.r-project.org/)
[![Platform](https://img.shields.io/badge/Platform-Google_Colab-orange.svg)](https://colab.research.google.com/)

Repositori ini berisi perangkat lunak (*toolkit*) untuk akuisisi data, validasi dataset, dan pengukuran eksperimental terkait perilaku algoritma kompresi JPEG. Proyek ini bertujuan untuk membuktikan secara empiris hubungan non-linear antara parameter *Quality* dan ukuran file (*File Size*).

## 📋 Latar Belakang

Algoritma JPEG menggunakan *Quantization Matrices* yang menyebabkan perubahan ukuran file tidak bersifat linear terhadap pengaturan kualitasnya. Repositori ini menyediakan pipeline otomatis untuk:
1.  Mengunduh sampel gambar acak terstandarisasi.
2.  Memvalidasi integritas dataset.
3.  Melakukan kompresi iteratif (Quality 1-100) dan mencatat metrik ukuran file.

## 📂 Sumber Data

Sampel citra digital yang digunakan dalam eksperimen ini diambil secara acak menggunakan API publik:
* **Sumber**: [Lorem Picsum](https://picsum.photos/)
* **Metode**: Pengunduhan otomatis dengan resolusi tetap ($S \times S$) untuk memastikan variabel kontrol yang konsisten.

## 🛠️ Arsitektur Sistem

Sistem terdiri dari tiga modul Python yang bekerja secara sekuensial:

| Modul | Fungsi | Deskripsi Akademis |
| :--- | :--- | :--- |
| `sample.py` | **Akuisisi Data** | Mengambil sampel gambar acak ($N$ sampel) dan melakukan standarisasi resolusi. |
| `check.py` | **Validasi Data** | Memeriksa integritas file (*header check*) dan kelengkapan urutan sampel (*sequence continuity*). |
| `measure.py` | **Pengukuran** | Melakukan kompresi iteratif (100 iterasi per gambar) dan mencatat hasil ke dalam format CSV. |

---

## 🚀 Instruksi Penggunaan

Pastikan Python 3.x dan library `Pillow` sudah terinstal:
```bash
pip install requests Pillow

```

### Tahap 1: Generasi Sampel

Mengunduh 30 gambar sampel dengan resolusi 1000x1000 piksel. Gunakan flag `-f` untuk memaksa *overwrite* jika memulai eksperimen baru.

```bash
python sample.py -n 30 -s 1000 -f

```

### Tahap 2: Validasi Integritas

Memastikan tidak ada file yang korup atau hilang sebelum proses pengukuran dimulai.

```bash
python check.py -n 30

```

*Pastikan output menunjukkan: "Dataset STATUS: HEALTHY"*

### Tahap 3: Eksekusi Eksperimen

Menjalankan loop kompresi pada seluruh dataset dan menyimpan hasil pengukuran ke file CSV.

```bash
python measure.py -i ./samples -o ./out -c final_data.csv

```

---

## 📊 Analisis Statistik (R Language)

Analisis data dilakukan menggunakan bahasa pemrograman **R** untuk membandingkan performa **Model Linear Naif** () dengan **Model Transformasi Log-Linear**. Analisis mencakup uji asumsi klasik, visualisasi *Residual Plot*, dan deteksi *Heteroskedastisitas*.

Hasil analisis lengkap, visualisasi grafik, dan interpretasi matematis dapat diakses melalui Google Colab Notebook berikut:

**Topik Analisis:**

1. Exploratory Data Analysis (EDA) menggunakan `ggplot2`.
2. Pembuktian bias pada Regresi Linear ().
3. Penerapan Transformasi Logaritma Natural ().
4. Evaluasi *Goodness-of-Fit* () dan pola Residual.

---

## 📂 Struktur Direktori

```text
.
├── sample.py           # Skrip downloader
├── check.py            # Skrip validator
├── measure.py          # Skrip pengukuran (analyzer)
├── samples/            # Direktori penyimpanan gambar mentah (Generated)
├── out/                # Direktori output hasil pengukuran
│   └── final_data.csv  # Dataset hasil eksperimen
└── README.md           # Dokumentasi proyek

```

## 📜 Lisensi & Atribut

* **Code License**: MIT License.
* **Image Source**: Gambar disediakan oleh [Lorem Picsum](https://picsum.photos/). Hak cipta gambar tunduk pada lisensi masing-masing fotografer kontributor Unsplash/Picsum.