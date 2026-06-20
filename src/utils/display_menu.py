import os
from core.base_menu import BaseMenu


class TerminalMenu(BaseMenu):
    """
    Ini adalah class nyata yang mewarisi kontrak dari BaseMenu.
    """

    def start(self, list_menu):
        self.display_menu()
        pilihan = self.handle_input(list_menu)
        return pilihan

    def display_menu(self):
        banner = r"""
 _   _  _____  ____  ____  ___      _    _  __
| \ | || ____|/ __ \/ ___||_ _|    / \  | |/ /
|  \| ||  _| / / _` \___ \ | |    / _ \ | ' / 
| |\  || |__| | (_| |___) || |   / ___ \| . \ 
|_| \_||_____\ \__,_|____/|___| /_/   \_\_|\_\
                            Automation Suite
                            by EzDev
        """
        print(banner)
        print("=== Main Menu ===")
        print("1. Start Bot")
        print("2. Exit")

    def display_tools(self):
        banner_tools = r"""
  _____ ___   ___  _     ____  
 |_   _/ _ \ / _ \| |   / ___| 
   | || | | | | | | |   \___ \ 
   | || |_| | |_| | |___ ___) |
   |_| \___/ \___/|_____|____/ 
        """
        print(banner_tools)
        print("=== Automation Tools ===")
        print("1. Layanan Mahasiswa Bot")
        print("2. Pengisian KRS Bot")
        print("3. Tool Lainnya")
        print("4. Back to Main Menu")

    def handle_input(self, list_menu):
        return input(f"Masukkan pilihan (1-{len(list_menu)}): ").strip()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
