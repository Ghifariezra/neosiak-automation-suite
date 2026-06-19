import os
import time
from dotenv import load_dotenv
from bots.layanan_mahasiswa import LayananMahasiswaBot

load_dotenv()

# Ambil data dari file .env
NIM = os.getenv("NIM_OR_EMAIL") if os.getenv(
    "NIM_OR_EMAIL") else "45XXXXXXXX"
PASSWORD = os.getenv("PASSWORD") if os.getenv("PASSWORD") else "password_anda"
PILIHAN_JAWABAN = os.getenv("PILIHAN_JAWABAN") if os.getenv("PILIHAN_JAWABAN") else "Sangat Setuju"
TEKS_SARAN = os.getenv("TEKS_SARAN") if os.getenv(
    "TEKS_SARAN") else "Pelayanan perpustakaan dan akademik sudah sangat memuaskan."

def main():
    print("[INFO] Memulai LayananMahasiswaBot...")
    bot = LayananMahasiswaBot()
    time.sleep(2)

    print("[INFO] Melakukan login...")
    bot.login(NIM, PASSWORD)
    print("[INFO] Login berhasil.")
    time.sleep(2)

    print("[INFO] Navigasi ke halaman pengisian survei...")
    bot.go_to_fill_survey()
    time.sleep(2)  # Beri waktu agar halaman survei termuat sepenuhnya

    # Mengambil info stepper
    stepper_info = bot.get_stepper_info()
    total_stepper = stepper_info['total']

    print(f"[INFO] Total Stepper ditemukan: {total_stepper}")
    print("[INFO] Daftar Stepper:")
    for idx, text in enumerate(stepper_info['texts'], start=1):
        print(f"  {idx}. {text}")

    print("[INFO] Memulai proses pengisian otomatis...")

    # Memanggil fungsi looping untuk menjawab pertanyaan
    bot.answer_questions(
        total_stepper=total_stepper,
        pilihan=PILIHAN_JAWABAN,
        teks_saran=TEKS_SARAN
    )

    print("[INFO] Proses pengisian selesai.")
    time.sleep(5)  # Jeda untuk melihat hasil sebelum browser ditutup

    print("[INFO] Menutup browser...")
    bot.quit()


if __name__ == "__main__":
    main()