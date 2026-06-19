from core.neosiak import NeosiakBot

class LayananMahasiswaBot(NeosiakBot):
    """Bot untuk mengakses layanan mahasiswa."""

    def __init__(self):
        super().__init__()

    # Go To Fill Survey Page
    def go_to_fill_survey(self):
        """Navigasi ke halaman pengisian survei."""

        # Opsi 1: Menggunakan CSS Selector berdasarkan atribut href (Direkomendasikan)
        self.driver.click(
            'a[href="https://neosiak.univpancasila.ac.id/pertanyaan-laymhs"]')

        # Opsi 2: Menggunakan teks yang muncul di layarnya langsung
        # self.driver.click_link("Mengisi Survey Layanan Mahasiswa")

        return self

    # Get Stepper Info
    def get_stepper_info(self):
        """Mengambil teks dan total stepper dari halaman survei."""

        # 1. Cari semua elemen yang menampung teks judul stepper
        # Berdasarkan HTML kamu, teksnya ada di dalam <h3 class="stepper-title">
        stepper_elements = self.driver.find_elements('.stepper-title')

        # 2. Ekstrak teks dari masing-masing elemen menggunakan list comprehension
        # .strip() digunakan untuk membersihkan spasi berlebih atau karakter \n
        stepper_texts = [element.text.strip() for element in stepper_elements]

        # 3. Hitung total stepper berdasarkan jumlah teks yang berhasil diambil
        total_stepper = len(stepper_texts)

        # 4. Kembalikan datanya dalam bentuk Dictionary agar mudah diakses
        return {
            "total": total_stepper,
            "texts": stepper_texts
        }

    # Question and Answer
    def answer_questions(self, total_stepper, pilihan="Sangat Setuju", teks_saran="Layanan sudah sangat baik, terima kasih."):
        """
        Logika untuk menjawab semua pertanyaan survei di semua stepper menggunakan Native JS.
        :param total_stepper: Jumlah stepper/halaman yang harus di-looping
        :param pilihan: Teks jawaban yang ingin dipilih (default: "Sangat Setuju")
        :param teks_saran: Teks yang diisi jika textarea berstatus required
        """

        for i in range(total_stepper):
            print(f"[INFO] =========================================")
            print(f"[INFO] Menjawab pertanyaan pada Stepper {i+1}...")

            # Beri jeda 2 detik setiap pindah stepper agar DOM halaman web benar-benar siap
            self._time.sleep(2)

            # =================================================================
            # 1. BLOK JS UNTUK RADIO BUTTON (PILIHAN GANDA)
            # =================================================================
            script_radio = f"""
                var labels = document.querySelectorAll('label.btn-outline');
                var diklik = 0;
                
                for (var j = 0; j < labels.length; j++) {{
                    if (labels[j].innerText.includes('{pilihan}')) {{
                        labels[j].scrollIntoView({{block: 'center'}});
                        labels[j].click();
                        diklik++;
                    }}
                }}
            """
            try:
                self.driver.execute_script(script_radio)
                print(
                    f"[INFO] Perintah klik untuk opsi '{pilihan}' berhasil dijalankan.")
            except Exception as e:
                print(
                    f"[ERROR] Terjadi kesalahan eksekusi JS (Radio Button): {e}")

            # Jeda kecil sebelum mengecek textarea
            self._time.sleep(1)

            # =================================================================
            # 2. BLOK JS UNTUK TEXTAREA (SARAN / MASUKAN)
            # =================================================================
            script_textarea = f"""
                var textareas = document.querySelectorAll('textarea');
                
                for (var k = 0; k < textareas.length; k++) {{
                    var ta = textareas[k];
                    
                    // offsetParent !== null memastikan kita hanya mengisi textarea yang 
                    // sedang TAMPIL di stepper saat ini (bukan yang disembunyikan di stepper lain)
                    if (ta.offsetParent !== null) {{
                        ta.scrollIntoView({{block: 'center'}});
                        
                        // Cek apakah textarea ini wajib diisi (required)
                        var isReq = ta.hasAttribute('required') || ta.required;
                        
                        if (isReq) {{
                            ta.value = '{teks_saran}';
                        }} else {{
                            ta.value = '-';
                        }}
                        
                        // Memicu event input dan change agar framework web (seperti React/Bootstrap) 
                        // menyadari bahwa ada teks yang diinputkan secara programatik
                        ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    }}
                }}
            """
            try:
                self.driver.execute_script(script_textarea)
                print(
                    f"[INFO] Pengecekan dan pengisian Textarea (jika ada) berhasil dijalankan.")
            except Exception as e:
                print(f"[ERROR] Terjadi kesalahan eksekusi JS (Textarea): {e}")

            # =================================================================
            # 3. BLOK JS UNTUK PINDAH STEPPER / SUBMIT
            # =================================================================
            if i < total_stepper - 1:
                print(f"[INFO] Berpindah ke Stepper {i+2}...")
                try:
                    script_next = """
                        var nextBtn = document.querySelector('button[data-kt-stepper-action="next"]');
                        if (nextBtn) { nextBtn.click(); }
                    """
                    self.driver.execute_script(script_next)

                    # Wajib diberi jeda agar animasi slide stepper ke halaman berikutnya selesai
                    self._time.sleep(1.5)
                except Exception as e:
                    print(f"[ERROR] Gagal menekan tombol selanjutnya: {e}")
            else:
                print("[INFO] =========================================")
                print(
                    f"[INFO] Mencapai stepper terakhir ({total_stepper}). Seluruh pertanyaan telah dijawab!")
                print("[INFO] Siap untuk submit!")

                # UNCOMMENT KODE DI BAWAH JIKA INGIN BOT LANGSUNG MENEKAN TOMBOL SUBMIT OTOMATIS
                script_submit = """
                   var submitBtn = document.querySelector('button[data-kt-stepper-action="submit"]');
                   if (submitBtn) { submitBtn.click(); }
                """
                self.driver.execute_script(script_submit)

        return self

    def run(self):
        self._time.sleep(2)

        self.login()
        self._time.sleep(2)

        self.go_to_fill_survey()
        self._time.sleep(2)

        stepper_info = self.get_stepper_info()
        total_stepper = stepper_info['total']

        print(f"[INFO] Total Stepper ditemukan: {total_stepper}")
        print("[INFO] Daftar Stepper:")
        for idx, text in enumerate(stepper_info['texts'], start=1):
            print(f"  {idx}. {text}")

        print("[INFO] Memulai proses pengisian otomatis...")
        pilihan = self._os.getenv("PILIHAN_JAWABAN") if self._os.getenv(
            "PILIHAN_JAWABAN") else "Sangat Setuju"
        teks_saran = self._os.getenv("TEKS_SARAN") if self._os.getenv(
            "TEKS_SARAN") else "Pelayanan sudah sangat baik, terima kasih."

        self.answer_questions(
            total_stepper=total_stepper,
            pilihan=pilihan,
            teks_saran=teks_saran
        )

        print("[INFO] Proses pengisian selesai.")
        # Jeda untuk melihat hasil sebelum browser ditutup
        self._time.sleep(5)

        print("[INFO] Menutup browser...")
        self.quit()
