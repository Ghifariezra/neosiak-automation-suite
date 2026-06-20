from core.driver import Driver

class NeosiakBot(Driver):
    """Bot dasar untuk mengotomatisasi interaksi dengan portal Neosiak."""

    __url = "https://neosiak.univpancasila.ac.id"

    def __init__(self):
        super().__init__()
        self.open(self.__url)

    def login(self):
        """Metode untuk login ke portal Neosiak."""
        nim_or_email = self._os.getenv("NIM_OR_EMAIL") if self._os.getenv(
            "NIM_OR_EMAIL") else "45XXXXXXXX"
        password = self._os.getenv("PASSWORD") if self._os.getenv(
            "PASSWORD") else "password_anda"

        self.driver.type('input[name="username"]', nim_or_email)
        self.driver.type('input[name="password"]', password)
        self.driver.click('button[type="submit"]')
        
        return None
    
    def open_sidebar(self, go_to):
        """Metode untuk membuka menu pengisian KRS."""

        # Gabungkan CSS Selector langsung dari parent hingga ke elemen target (menu-title)
        selector = '#kt_app_sidebar_secondary_menu div[data-kt-menu-trigger="click"] .menu-link .menu-title'

        # find_elements() akan mengembalikan list of Selenium WebElements
        menu_elements = self.driver.find_elements(selector)

        for element in menu_elements:
            # Karena iterasi ini mengembalikan objek WebElement native, Anda bisa langsung panggil .text
            get_text = element.text.strip()
            if get_text:  # Filter opsional jika ada elemen kosong
                print(f"[DEBUG] Found sidebar link: {get_text}")
                if get_text == go_to:
                    self.driver.click_link_text(get_text)
                    self._time.sleep(2)  # Tunggu halaman KRS terbuka

                    get_info = self.driver.find_element(
                        '#kt_app_content_container > div > div > div:nth-child(2) > h4').text.strip()

                    if "Ditutup" in get_info:
                        pesan = "Pengisian KRS saat ini ditutup. Tidak dapat melanjutkan."
                        print(f"[INFO] {pesan}")

                        self.driver.execute_script(f"""
                            // 1. Buat Background Overlay (Efek Gelap + Blur)
                            let overlay = document.createElement('div');
                            overlay.style.position = 'fixed';
                            overlay.style.top = '0';
                            overlay.style.left = '0';
                            overlay.style.width = '100vw';
                            overlay.style.height = '100vh';
                            overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.4)'; 
                            overlay.style.backdropFilter = 'blur(6px)'; // Efek blur
                            overlay.style.zIndex = '99998'; // Berada persis di bawah toast
                            document.body.appendChild(overlay);

                            // 2. Buat Elemen Toast di Tengah Layar
                            let toast = document.createElement('div');
                            toast.innerText = '🤖 BOT INFO:\\n{pesan}';
                            toast.style.position = 'fixed';
                            toast.style.top = '50%';
                            toast.style.left = '50%';
                            toast.style.transform = 'translate(-50%, -50%)'; // Trik memposisikan tepat di tengah
                            toast.style.backgroundColor = '#f44336';
                            toast.style.color = 'white';
                            toast.style.padding = '24px 40px';
                            toast.style.borderRadius = '12px';
                            toast.style.zIndex = '99999'; // Berada di atas overlay
                            toast.style.boxShadow = '0 20px 25px -5px rgba(0, 0, 0, 0.2)';
                            toast.style.fontFamily = 'system-ui, -apple-system, sans-serif';
                            toast.style.fontSize = '18px';
                            toast.style.fontWeight = 'bold';
                            toast.style.textAlign = 'center';
                            toast.style.lineHeight = '1.6';
                            document.body.appendChild(toast);
                            
                            // 3. Menghilangkan toast dan overlay otomatis setelah 4 detik
                            setTimeout(() => {{
                                toast.remove();
                                overlay.remove();
                            }}, 4000);
                        """)

                        self._time.sleep(4)
                        return

                    break

        return None
