from abc import ABC, abstractmethod

class BaseMenu(ABC):
    """
    Ini adalah Abstract Class. 
    Kita mewariskan 'ABC' agar class ini menjadi abstrak.
    """

    @abstractmethod
    def start(self):
        """
        Fungsi abstrak. Isinya dibiarkan kosong (pass).
        Semua class yang mewarisi BaseMenu WAJIB membuat ulang fungsi ini.
        """
        pass

    @abstractmethod
    def display_menu(self):
        """
        Fungsi abstrak. Isinya dibiarkan kosong (pass).
        Semua class yang mewarisi BaseMenu WAJIB membuat ulang fungsi ini.
        """
        pass
    
    @abstractmethod
    def display_tools(self):
        """
        Fungsi abstrak. Isinya dibiarkan kosong (pass).
        Semua class yang mewarisi BaseMenu WAJIB membuat ulang fungsi ini.
        """
        pass

    @abstractmethod
    def handle_input(self):
        """Aturan kedua: wajib punya fungsi untuk menangani input."""
        pass
    
    @abstractmethod
    def clear_screen(self):
        """Aturan ketiga: wajib punya fungsi untuk membersihkan layar terminal."""
        pass