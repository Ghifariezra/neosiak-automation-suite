# Neosiak Automation Suite 🤖🎓

Kumpulan skrip otomatisasi (RPA) berbasis Python dan **SeleniumBase** untuk menyederhanakan akses dan eksekusi tugas pada portal akademik Neosiak Universitas Pancasila.

Saat ini, *suite* ini mendukung otomatisasi multi-bot yang dapat diakses langsung melalui antarmuka terminal interaktif, termasuk layanan mahasiswa, pengisian KRS, dan pencarian/unduh soal UAS. Proyek ini dikelola melalui `pyproject.toml` dan modul utamanya berada di folder `src/`, dengan entry point utama di `main.py` pada root repository. Panduan penggunaan yang lebih lengkap tersedia di [docs/HOW-TO-USE.md](docs/HOW-TO-USE.md).

---

## 🗺️ Roadmap (Rencana Pengembangan)
- [x] **Layanan Mahasiswa Bot:** Otomatisasi pengisian survei evaluasi layanan kampus.
- [x] **Pengisian KRS Bot:** Otomatisasi pengecekan status jadwal dan navigasi menu pengisian KRS.
- [x] **Absen UAS Bot:** Otomatisasi pencarian mata kuliah dan unduh file soal UAS dari tabel portal.
- [x] **Interactive CLI:** Antarmuka terminal dengan ASCII Art untuk navigasi program yang mudah.
- [x] **Unit Testing & CI/CD:** Implementasi pengujian otomatis terintegrasi dengan GitHub Actions.
- [x] **Package Migration:** Menggunakan `pyproject.toml`, package modular, dan entry point root.
- [ ] *[Coming Soon]* Fitur otomatisasi akademik lainnya (Cek nilai, unduh KHS, dll).

---

## ✨ Fitur Utama

* **Menu Interaktif (CLI):** Antarmuka terminal interaktif yang ramah pengguna, lengkap dengan *error handling* untuk input yang tidak valid, validasi tipe data, dan transisi layar yang mulus.
* **Bypass Deteksi Bot:** Menggunakan mode *Undetected ChromeDriver* (UC Mode) yang dikelola langsung pada layer driver untuk menjaga konsistensi sesi browser.
* **Injeksi UI & Efek Blur Modern:** Menggunakan manipulasi DOM via JavaScript asinkron untuk menyuntikkan *custom overlay* dengan efek latar belakang blur (`backdrop-filter`) serta *centered alert toast* berwarna merah elegan untuk memberikan *feedback* visual langsung di peramban ketika mendeteksi anomali.
* **Injeksi Native JS Super Cepat:** Navigasi antarmuka Bootstrap 5, pengisian *radio button*, transisi *stepper*, dan interaksi tabel UAS dieksekusi murni via JavaScript di dalam DOM *browser*, menghilangkan masalah *race-condition* akibat jaringan lambat.
* **Automated Testing & CI/CD:** Dilengkapi dengan cakupan *unit test* menyeluruh (menggunakan `pytest` dan `unittest.mock`) yang memisahkan pengujian alur kerja bot dan fungsionalitas inti *core*. Berjalan otomatis setiap ada aktivitas *push* ke repositori via GitHub Actions.

---

## 📂 Struktur Direktori

```bash
neosiak-automation-suite/
├── .github/
│   └── workflows/
│       └── test.yml                # Pipeline CI/CD GitHub Actions
├── scripts/
│   └── ps/
│       └── run-test.ps1            # Skrip runner test untuk Windows PowerShell
├── src/
│   ├── bots/
│   │   ├── __init__.py
│   │   ├── absen_uas.py            # Bot pencarian mata kuliah dan unduh soal UAS
│   │   ├── layanan_mahasiswa.py    # Logika spesifik pengisian form survei layanan
│   │   └── pengisian_krs.py        # Logika spesifik alur eksekusi pengisian KRS
│   ├── core/
│   │   ├── __init__.py
│   │   ├── base_menu.py            # Abstract class (Kontrak blueprint menu)
│   │   ├── driver.py               # Konfigurasi browser SeleniumBase
│   │   ├── neosiak.py              # Base class bot (Autentikasi & open_sidebar)
│   │   └── singleton.py            # Metaclass untuk Singleton pattern
│   └── utils/
│       ├── __init__.py
│       └── display_menu.py         # Implementasi UI Terminal (ASCII Art & Input Handler)
├── tests/                          # Kumpulan Unit Test (Mock Testing)
│   ├── __init__.py
│   ├── bots/
│   │   ├── absen_uas_test.py
│   │   ├── layanan_mahasiswa_test.py
│   │   └── pengisian_krs_test.py
│   ├── core/
│   │   ├── base_menu_test.py
│   │   ├── driver_test.py
│   │   ├── neosiak_test.py
│   │   └── singleton_test.py
│   ├── utils/
│   │   └── display_menu_test.py
│   ├── conftest.py                 # Konfigurasi Pytest hooks
│   └── main_test.py                # Pengujian exit path aplikasi
├── main.py                         # Entry point aplikasi (Menu CLI Utama & Sub-menu)
├── pyproject.toml                  # Metadata library & dependencies
├── .env                            # Kredensial & Kustomisasi (Diabaikan oleh Git)
├── .env.example                    # Template environment variables
├── .gitignore                      # Aturan pengecualian Git
└── README.md                       # Dokumentasi proyek
```

---

## 🚀 Cara Instalasi & Persiapan
Pastikan Anda telah menginstal Python 3.10+ dan browser Google Chrome terbaru di sistem Anda.

1. Persiapan Environment Sangat disarankan menggunakan virtual environment agar package atau pustaka tidak bentrok dengan sistem utama.
```bash
python -m venv venv

# Aktifkan di Windows:
venv\Scripts\activate

# Aktifkan di macOS/Linux:
source venv/bin/activate
```
2. Instalasi Proyek (Editable Mode)
Proyek ini dikelola menggunakan `pyproject.toml`. Instal suite ini beserta seluruh dependensinya melalui pip:
```bash
# Untuk instalasi standar (produksi)
pip install -e .

# Untuk instalasi pengembangan (termasuk pytest)
pip install -e .[dev]
```
3. Konfigurasi Kredensial (.env)
Bot ini membutuhkan kredensial portal akademik untuk dapat beroperasi. Data ini disimpan secara lokal.
- Buat salinan dari file `.env.example` dan ubah namanya menjadi `.env`.
- Buka file `.env` dan masukkan data Anda tanpa tanda kutip ekstra:
```bash
NIM_OR_EMAIL=45XXXXXXXX
PASSWORD=password_rahasia_anda

# Kustomisasi Jawaban Survei
PILIHAN_JAWABAN="Sangat Setuju"
TEKS_SARAN="Pelayanan perpustakaan dan akademik sudah sangat memuaskan."
```

---

## 💻 Cara Penggunaan
Setelah semua konfigurasi selesai, jalankan skrip utama dari direktori root (pastikan virtual environment masih aktif).
```bash
python main.py
```

Untuk panduan penggunaan yang lebih lengkap, lihat [docs/HOW-TO-USE.md](docs/HOW-TO-USE.md).

Jika Anda ingin memakai bot sebagai library di proyek lain, impor langsung dari paket `src`.
```python
from src.bots import AbsenUASBot, LayananMahasiswaBot, PengisianKRSBot
```

Kustomisasi Jawaban Survei:
- Secara bawaan (default), bot akan mengisi form dengan pilihan `"Sangat Setuju"` dan mengisi textarea `(jika wajib)` dengan teks "Pelayanan sudah sangat baik, terima kasih.".
- Anda dapat mengubah nilainya melalui variabel environment `PILIHAN_JAWABAN` dan `TEKS_SARAN` di file `.env`.

Menu bot yang tersedia saat ini:
- `Layanan Mahasiswa Bot` untuk survei evaluasi layanan.
- `Pengisian KRS Bot` untuk masuk ke alur pengisian KRS dan menangani kondisi jadwal yang ditutup.
- `Absen UAS Bot` untuk mencari mata kuliah pada tabel soal UAS, membaca jam mulai, lalu membuka file unduhan bila tersedia.

## 🧪 Menjalankan Unit Test
Proyek ini dilengkapi dengan mock testing untuk memverifikasi logika tanpa harus membuka browser. Anda dapat menjalankan tes secara lokal menggunakan skrip yang telah disediakan:

**Untuk Pengguna Windows (PowerShell):**
```bash
.\scripts\ps\run-test.ps1
```

**Perintah Manual (Universal):**
```bash
python -m pytest -v ./tests/
```

--- 

## ⚠️ Disclaimer
Skrip ini dibuat untuk tujuan edukasi dan pembelajaran terkait Otomatisasi Peramban (Browser Automation) dan Document Object Model (DOM) Manipulation. Pengguna bertanggung jawab penuh atas segala risiko atau penyalahgunaan terhadap layanan akademik yang bersangkutan.