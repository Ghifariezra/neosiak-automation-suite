from src.bots import AbsenUASBot, LayananMahasiswaBot, PengisianKRSBot
from src.utils import TerminalMenu

def main():
    daftar_menu = [1, 2]
    daftar_alat = [1, 2, 3]

    menu = TerminalMenu()

    # Looping Utama (Main Menu)
    while True:
        menu.clear_screen()
        pilihan = menu.start(daftar_menu)

        # Validasi apakah input berupa angka
        if not pilihan.isdigit():
            print("[INFO] Masukan tidak valid! Harap masukkan angka.")
            input("\n[Tekan Enter untuk mencoba lagi...]")
            continue

        pilihan = int(pilihan)

        if pilihan == 1:
            # Looping Sub-Menu (Tools)
            while True:
                menu.clear_screen()
                menu.display_tools()

                pilihan_alat = menu.handle_input(daftar_alat)

                if not pilihan_alat.isdigit():
                    print("[INFO] Masukan tidak valid! Harap masukkan angka.")
                    input("\n[Tekan Enter untuk mencoba lagi...]")
                    continue

                pilihan_alat = int(pilihan_alat)

                if pilihan_alat == 1:
                    menu.clear_screen()
                    print("[INFO] Memulai LayananMahasiswaBot...\n")
                    bot = LayananMahasiswaBot()
                    bot.run()
                    # Menahan layar agar hasil eksekusi bot bisa dibaca
                    input(
                        "\n[Bot Selesai. Tekan Enter untuk kembali ke menu alat...]")

                elif pilihan_alat == 2:
                    menu.clear_screen()
                    print("[INFO] Memulai PengisianKRSBot...\n")
                    bot = PengisianKRSBot()
                    bot.run()

                    input("\n[Selesai. Tekan Enter untuk kembali...]")
                
                elif pilihan_alat == 3:
                    menu.clear_screen()
                    print("[INFO] Memulai AbsenUASBot...\n")
                    bot = AbsenUASBot()
                    bot.run()
                    
                    input("\n[Selesai. Tekan Enter untuk kembali...]")
                
                elif pilihan_alat == 4:
                    print("\n[INFO] Tool lain belum tersedia.")
                    input("[Tekan Enter untuk kembali...]")

                elif pilihan_alat == 5:
                    # Keluar dari sub-menu dan kembali ke menu utama
                    break

                else:
                    print(
                        "\n[INFO] Pilihan tidak valid. Silakan pilih alat yang tersedia.")
                    input("[Tekan Enter untuk mencoba lagi...]")

        elif pilihan == 2:
            menu.clear_screen()
            print("[INFO] Keluar dari program. Sampai jumpa!")
            break  # Menghentikan looping utama, program selesai

        else:
            print("\n[INFO] Pilihan tidak valid. Silakan pilih menu yang tersedia.")
            input("[Tekan Enter untuk mencoba lagi...]")


if __name__ == "__main__":
    main()
