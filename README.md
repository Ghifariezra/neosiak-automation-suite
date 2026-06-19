# Neosiak Automation Suite 🤖🎓

Kumpulan skrip otomatisasi (RPA) berbasis Python dan **SeleniumBase** untuk menyederhanakan akses dan eksekusi tugas pada portal akademik Neosiak Universitas Pancasila. 

Saat ini, *suite* ini berfokus pada **Layanan Mahasiswa Bot** untuk melakukan proses *login* dan pengisian survei evaluasi secara otomatis.

---

## 🗺️ Roadmap (Rencana Pengembangan)
- [x] **Layanan Mahasiswa Bot:** Otomatisasi pengisian survei evaluasi layanan kampus.
- [ ] *[Coming Soon]* Fitur otomatisasi akademik lainnya (Cek nilai, unduh KHS, dll).

---

## ✨ Fitur Utama (Layanan Mahasiswa Bot)

* **Bypass Deteksi Bot:** Menggunakan mode *Undetected ChromeDriver* (CDP) yang dikelola melalui pola arsitektur *Singleton* untuk performa memori yang optimal.
* **Auto-Login Aman:** Kredensial pengguna (NIM dan Password) disimpan secara aman menggunakan *Environment Variables* (`.env`).
* **Injeksi Native JS Super Cepat:** Navigasi antarmuka Bootstrap 5, pengisian *radio button*, dan transisi *stepper* dieksekusi murni via JavaScript di dalam DOM *browser*, menghilangkan masalah *race-condition* atau gagal klik.
* **Pengecekan Textarea Dinamis:** Bot secara otomatis mendeteksi form isian teks (Saran/Masukan), membedakan antara field *required* (wajib) dan *optional*, lalu mengisinya dengan parameter yang telah ditentukan.
* **Auto-Submit:** Mengirimkan hasil survei secara otomatis setelah seluruh *stepper* selesai dijawab.

---

## 📂 Struktur Direktori

```text
neosiak-automation-suite/
├── src/
│   ├── main.py                     # Entry point aplikasi
│   ├── bots/
│   │   └── layanan_mahasiswa.py    # Logika spesifik pengisian form dan navigasi survei
│   └── core/
│       ├── driver.py               # Konfigurasi SeleniumBase
│       └── singleton.py            # Metaclass untuk Singleton pattern
├── .env                            # Kredensial lokal (Diabaikan oleh Git)
├── .env.example                    # Template environment variables
├── .gitignore                      # Aturan pengecualian Git
├── requirements.txt                # Daftar dependency Python
└── README.md                       # Dokumentasi proyek
```

---

## 🚀 Cara Instalasi & Persiapan
Pastikan Anda telah menginstal Python 3.10+ dan browser Google Chrome terbaru di sistem Anda.

1. Persiapan Environment Sangat disarankan menggunakan virtual environment agar package atau pustaka tidak bentrok dengan sistem utama.
    ```
    python -m venv venv

    # Aktifkan di Windows:
    venv\Scripts\activate

    # Aktifkan di macOS/Linux:
    source venv/bin/activate
    ```
2. Instalasi Dependencies Instal seluruh pustaka yang dibutuhkan (termasuk seleniumbase dan `python-dotenv`).
   ```
   pip install -r requirements.txt
   ```
3. Konfigurasi Kredensial (.env) Bot ini membutuhkan NIM atau Email dan Password portal akademik untuk dapat beroperasi. Data ini disimpan secara lokal.
    - Buat salinan dari file `.env.example` dan ubah namanya menjadi `.env.`
    - Buka file `.env` dan masukkan data Anda tanpa tanda kutip ekstra:
    ```
    NIM_OR_EMAIL=452421XXXX
    PASSWORD=password_rahasia_anda
    ```

---

## 💻 Cara Penggunaan
Setelah semua konfigurasi selesai, jalankan skrip utama dari direktori root (pastikan virtual environment masih aktif).
```
python src/main.py
```

Kustomisasi Jawaban: Secara bawaan (default), bot akan mengisi form dengan pilihan "Sangat Setuju" dan mengisi textarea (jika wajib) dengan teks "Pelayanan perpustakaan dan akademik sudah sangat memuaskan.". Anda dapat mengubah nilai ini di dalam pemanggilan fungsi bot.answer_questions() pada file src/main.py.

--- 

## ⚠️ Disclaimer
Skrip ini dibuat untuk tujuan edukasi dan pembelajaran terkait Otomatisasi Peramban (Browser Automation) dan Document Object Model (DOM) Manipulation. Pengguna bertanggung jawab penuh atas segala risiko atau penyalahgunaan terhadap layanan akademik yang bersangkutan.