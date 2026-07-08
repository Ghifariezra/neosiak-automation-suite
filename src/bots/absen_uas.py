from core.neosiak import NeosiakBot

class AbsenUASBot(NeosiakBot):
    """Bot untuk mengotomatisasi absen UAS di portal Neosiak."""

    def __init__(self):
        super().__init__()

    def find_course(self, course_name=None):
        """Metode untuk mencari kursus dengan nama tertentu, mengambil waktu, dan mengunduh file."""
        # Check table
        parent_table_selector = '#kt_app_content_container > div.table-responsive'
        self.driver.wait_for_element(parent_table_selector)

        check_child_selector = f'{parent_table_selector} > table'
        if not self.driver.is_element_present(check_child_selector):
            print(f"[INFO] Tidak ada tabel kursus yang ditemukan.")
            return None

        if not course_name:
            print("[INFO] Nama kursus tidak diberikan.")
            return None

        # Ambil jumlah baris (tr) di dalam tbody untuk batas looping
        rows = self.driver.find_elements(f'{check_child_selector} tbody tr')
        total_rows = len(rows)
        # print(f"[DEBUG] Total baris mata kuliah yang terdeteksi: {total_rows}")

        # Looping murni menggunakan string CSS Selector (jauh lebih aman di SeleniumBase)
        for i in range(1, total_rows + 1):
            # Buat selector spesifik untuk tiap kolom di baris ke-i (nth-child mulai dari 1)
            course_col = f'{check_child_selector} tbody tr:nth-child({i}) td:nth-child(3)'
            time_col = f'{check_child_selector} tbody tr:nth-child({i}) td:nth-child(8)'
            file_col = f'{check_child_selector} tbody tr:nth-child({i}) td:nth-child(10)'

            # Lewati jika kolom matakuliah tidak ditemukan (mencegah error tabel berantakan)
            if not self.driver.is_element_present(course_col):
                continue

            current_course = self.driver.find_element(course_col).text.strip()
            # print(f"[DEBUG] Mengecek Baris {i}: {current_course}")

            # Cek apakah nama kursus yang dicari ada di baris ini
            if course_name.lower() in current_course.lower():
                print(f"[INFO] Ditemukan kursus: {current_course}")

                # Get start time
                start_time = self.driver.find_element(time_col).text.strip()
                print(f"[INFO] Jam Mulai: {start_time}")

                # Cek apakah tag <a> (link download) ada di dalam kolom file
                link_selector = f'{file_col} a'

                if self.driver.is_element_present(link_selector):
                    # Kalau tag 'a' ada, ambil href dan elemennya
                    download_link = self.driver.find_element(link_selector)
                    file_url = download_link.get_attribute('href')
                    print(f"[INFO] File tersedia. Target URL: {file_url}")

                    # 1. Trik JS: Hapus atribut target="_blank" MENGGUNAKAN SELECTOR
                    # Alih-alih melempar arguments[0], kita pakai document.querySelector bawaan JS
                    self.driver.execute_script(
                        f"document.querySelector('{link_selector}').removeAttribute('target');"
                    )

                    print("[INFO] Membuka PDF di tab yang sama...")
                    # 2. Klik link-nya
                    self.driver.click(link_selector)

                    # 3. Beri waktu beberapa detik agar file PDF selesai di-load oleh browser
                    self._time.sleep(4)

                    print("[INFO] Kembali ke halaman utama Neosiak...")
                    # 4. Klik tombol "Back" pada browser untuk kembali ke tabel
                    self.driver.go_back()

                    return {
                        "status": "success",
                        "course": current_course,
                        "start_time": start_time
                    }
                    
                else:
                    # Kalau tidak ada tag 'a', berarti cuma teks/badge ("Belum dibuka")
                    badge_text = self.driver.find_element(
                        file_col).text.strip()
                    print(
                        f"[WARNING] Tidak dapat mengunduh file. Status saat ini: {badge_text}")

                    return {
                        "status": "failed",
                        "course": current_course,
                        "start_time": start_time,
                        "reason": badge_text
                    }

        print(f"[INFO] Kursus '{course_name}' tidak ditemukan di tabel.")
        return None

    def run(self):
        """Contoh alur eksekusi bot"""
        self._time.sleep(2)
        self.login()

        self._time.sleep(2)
        self.open_sidebar(go_to="Unduh Soal UAS")

        self._time.sleep(2)

        print("[INFO] Memunculkan form input di browser...")

        # 1. Inject HTML & JS untuk membuat Modal Form
        js_inject_form = """
            // Reset variabel global window.botCourseName
            window.botCourseName = null;

            // Buat Background Overlay (Efek Gelap + Blur)
            let overlay = document.createElement('div');
            overlay.id = 'bot-overlay-form';
            overlay.style.position = 'fixed';
            overlay.style.top = '0';
            overlay.style.left = '0';
            overlay.style.width = '100vw';
            overlay.style.height = '100vh';
            overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.6)'; 
            overlay.style.backdropFilter = 'blur(5px)';
            overlay.style.zIndex = '999998';
            overlay.style.display = 'flex';
            overlay.style.alignItems = 'center';
            overlay.style.justifyContent = 'center';

            // Buat Kotak Form
            let formBox = document.createElement('div');
            formBox.style.backgroundColor = '#ffffff';
            formBox.style.padding = '30px';
            formBox.style.borderRadius = '12px';
            formBox.style.boxShadow = '0 10px 25px rgba(0,0,0,0.2)';
            formBox.style.width = '400px';
            formBox.style.fontFamily = 'system-ui, -apple-system, sans-serif';

            // Judul
            let title = document.createElement('h3');
            title.innerText = '🤖 Bot Pencari UAS';
            title.style.marginTop = '0';
            title.style.marginBottom = '10px';
            title.style.color = '#181C32'; // Warna teks gelap khas Neosiak

            // Label
            let label = document.createElement('p');
            label.innerText = 'Masukkan nama mata kuliah yang ingin diunduh:';
            label.style.color = '#7E8299';
            label.style.fontSize = '14px';
            label.style.marginBottom = '20px';

            // Input Field
            let input = document.createElement('input');
            input.type = 'text';
            input.placeholder = 'Cth: Sistem Informasi Geografis';
            input.style.width = '100%';
            input.style.padding = '12px';
            input.style.marginBottom = '20px';
            input.style.border = '1px solid #E4E6EF';
            input.style.borderRadius = '6px';
            input.style.fontSize = '15px';
            input.style.boxSizing = 'border-box';
            input.style.outline = 'none';

            // Tombol Submit
            let btn = document.createElement('button');
            btn.innerText = 'Cari & Unduh';
            btn.style.width = '100%';
            btn.style.padding = '12px';
            btn.style.backgroundColor = '#009EF7'; // Warna biru primary Neosiak
            btn.style.color = '#ffffff';
            btn.style.border = 'none';
            btn.style.borderRadius = '6px';
            btn.style.cursor = 'pointer';
            btn.style.fontSize = '15px';
            btn.style.fontWeight = 'bold';

            // Hover effect untuk tombol
            btn.onmouseover = () => btn.style.backgroundColor = '#008be0';
            btn.onmouseout = () => btn.style.backgroundColor = '#009EF7';

            // Logika ketika tombol diklik
            btn.onclick = function() {
                // Simpan nilai ke variabel global browser
                window.botCourseName = input.value;
                // Hapus form dari layar
                overlay.remove(); 
            };

            // Susun elemen
            formBox.appendChild(title);
            formBox.appendChild(label);
            formBox.appendChild(input);
            formBox.appendChild(btn);
            overlay.appendChild(formBox);
            document.body.appendChild(overlay);

            // Fokuskan cursor otomatis ke dalam input
            input.focus();
        """

        self.driver.execute_script(js_inject_form)

        # 2. Polling (Menunggu pengguna mengisi dan menekan tombol)
        course_name = None
        print("[INFO] Menunggu pengguna mengisi form di layar browser...")

        while True:
            # Ambil nilai dari variabel global JS 'window.botCourseName'
            result_from_ui = self.driver.execute_script(
                "return window.botCourseName;")

            # Jika nilainya bukan None, berarti tombol sudah diklik
            if result_from_ui is not None:
                course_name = result_from_ui.strip()
                break

            # Tunggu setengah detik sebelum mengecek lagi (mencegah CPU overwork)
            self._time.sleep(0.5)

        # 3. Eksekusi pencarian
        if not course_name:
            print("[INFO] Input kosong, membatalkan pencarian.")
            self.quit()
            return

        print(f"[INFO] Memproses pencarian untuk: {course_name}")
        result = self.find_course(course_name=course_name)

        if result and result.get("status") == "success":
            print("[INFO] Operasi unduh file berhasil dilakukan.")
        else:
            print("[INFO] Operasi unduh file tertunda atau gagal.")

        self._time.sleep(2)
        self.quit()
