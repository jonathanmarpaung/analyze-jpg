# Dataset Integrity Checker

Diagnostic tool untuk memvalidasi kelengkapan (*completeness*) dan kesehatan (*health*) dataset gambar. Script ini dirancang untuk mendeteksi file yang hilang berdasarkan urutan indeks numerik dan mengidentifikasi file rusak (*corrupted*) yang dapat menyebabkan kegagalan pada proses analisis selanjutnya.

## Features

* **Sequence Validation**: Mendeteksi celah (gap) pada penomoran file (contoh: `sample_1`, `sample_3` -> `sample_2` missing).
* **Corrupt Detection**: Memverifikasi header setiap file gambar untuk memastikan file tidak rusak/0-byte.
* **Out-of-Bounds Detection**: Memberikan peringatan jika ada file di luar rentang yang diharapkan.

## Requirements

* Python 3.8+
* Pillow (PIL Fork)

```bash
pip install Pillow

```

## Usage

Perintah dasar untuk memeriksa direktori default (`./samples`) dengan ekspektasi 30 gambar:

```bash
python check.py

```

### Command Line Arguments

| Flag | Long Flag | Description | Default |
| --- | --- | --- | --- |
| `-i` | `--input` | Direktori dataset yang akan diperiksa. | `./samples` |
| `-n` | `--number` | Jumlah total sampel yang diharapkan (1 s/d N). | `30` |
| `-p` | `--prefix` | Prefix nama file yang dicari. | `sample_` |
| `-e` | `--extension` | Ekstensi file yang diharapkan. | `.jpg` |
|  | `--no-integrity` | Lewati pemeriksaan fisik file (Hanya cek urutan nama). Gunakan ini jika dataset sangat besar. | `False` |

## Examples

**1. Pemeriksaan Standar (Default)**
Memeriksa apakah ada file yang hilang atau rusak di folder `./samples` untuk urutan 1-30.

```bash
python check.py

```

**2. Memeriksa Dataset Besar**
Jika Anda memiliki 1.000 sampel dan ingin pemeriksaan cepat (hanya cek kelengkapan nomor):

```bash
python check.py -n 1000 --no-integrity

```

**3. Custom Directory & Format**
Memeriksa folder lain dengan format file PNG.

```bash
python check.py -i ./training_data -p img_ -e .png -n 50

```

## Understanding the Report

Script akan mencetak laporan status di terminal:

* **❌ MISSING IDs**: Menunjukkan nomor urut yang tidak ditemukan filenya.
* *Solusi*: Jalankan ulang `sample.py` dengan flag `-f` (force) atau `-n` yang sesuai.


* **❌ CORRUPTED FILES**: File ada di folder, tetapi header-nya rusak atau tidak bisa dibaca oleh library gambar.
* *Solusi*: Hapus file yang rusak manual, lalu jalankan downloader lagi.


* **✅ Dataset STATUS: HEALTHY**: Semua file dari 1 sampai N lengkap dan bisa dibuka. Dataset siap untuk diproses oleh `measure.py`.