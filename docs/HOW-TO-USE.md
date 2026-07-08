## 💻 Cara Penggunaan

Pilih salah satu metode di bawah ini sesuai dengan kebutuhan Anda.

### Cara 1: Menjalankan Bot sebagai Aplikasi (Menu Interaktif CLI)
Cara ini adalah yang paling umum. Pilih metode ini jika Anda hanya ingin langsung menjalankan bot dan menggunakan menu interaktif di terminal.

**1. Clone Repositori**
Buka terminal di komputer Anda dan jalankan perintah berikut secara berurutan:
```bash
git clone [https://github.com/Ghifariezra/neosiak-automation-suite.git](https://github.com/Ghifariezra/neosiak-automation-suite.git)
cd neosiak-automation-suite
```

**2. Buat dan Aktifkan Virtual Environment**
(Opsional, namun sangat disarankan agar terisolasi dari package sistem)
```bash
python -m venv venv

# Aktivasi di Windows:
.\venv\Scripts\activate

# Aktivasi di Mac/Linux:
source venv/bin/activate
```

**3. Install Package Utama**
Karena Anda adalah pengguna akhir (end-user), cukup instal versi standarnya:
```bash
pip install .
```

**4. Siapkan Kredensial (.env)**
- Buat salinan (copy) dari file `.env.example` dan ubah namanya menjadi `.env.`
- Buka file `.env` tersebut, lalu isi nilai `NIM_OR_EMAIL` dan `PASSWORD` dengan akun Neosiak milik Anda.

**5. Jalankan Bot**
Setelah semuanya siap, mulai program utama dengan:
```bash
python src/main.py
```

### Cara 2: Menggunakan Bot sebagai Library di Script Anda Sendiri
Jika Anda seorang developer yang sedang membuat proyek dashboard atau skrip otomatisasi sendiri, Anda dapat "meminjam" modul bot (misal: AbsenUASBot) ke dalam proyek Anda tanpa perlu mengunduh antarmuka CLI-nya.

**1. Install Langsung dari GitHub**
Di dalam terminal proyek Anda, instal library ini secara langsung dengan perintah:
```bash
pip install git+[https://github.com/Ghifariezra/neosiak-automation-suite.git](https://github.com/Ghifariezra/neosiak-automation-suite.git)
```

**2. Siapkan Kredensial (.env)**
Anda tetap wajib membuat file .env di dalam root direktori proyek Anda sendiri agar bot dapat melakukan login.


**3. Panggil Bot di Kode Anda**
Impor modul bot ke dalam file Python buatan Anda (misalnya app_punya_teman.py), lalu inisiasi dan jalankan:
```python
from src.bots.absen_uas import AbsenUASBot

print("Menjalankan bot buatan Ezra...")
bot = AbsenUASBot()
bot.run()
```