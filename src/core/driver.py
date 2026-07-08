import os
import time
from dotenv import load_dotenv
# Hapus import SingletonMeta
# from core.singleton import SingletonMeta
from seleniumbase import SB

load_dotenv()

# Hapus (metaclass=SingletonMeta) dari deklarasi class
class Driver:
    """Class untuk mengelola instance SeleniumBase (Tanpa Singleton)."""

    _os: os = os
    _time: time = time

    def __init__(self):
        # Inisialisasi Context Manager
        self._sb_manager = SB(
            uc=True,  # Gunakan undetected-chromedriver
            locale="id-ID",
            maximize=True
        )
        # Eksekusi __enter__() secara manual untuk mendapatkan objek instance
        # yang memiliki metode .open(), .type(), dll.
        self.driver = self._sb_manager.__enter__()

    def get_driver(self):
        """Mengembalikan instance driver."""
        return self.driver

    def open(self, url):
        """Membuka URL menggunakan driver."""
        self.driver.open(url)
        return self

    def quit(self):
        """Menutup semua driver."""
        # Menjalankan __exit__ untuk menutup browser dan membersihkan resource
        self._sb_manager.__exit__(None, None, None)
        return self
