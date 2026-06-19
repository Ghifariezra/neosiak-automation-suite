import unittest
from unittest.mock import patch
from utils.display_menu import TerminalMenu


class TestTerminalMenu(unittest.TestCase):

    def setUp(self):
        """Inisialisasi objek TerminalMenu untuk digunakan di seluruh tes."""
        self.menu = TerminalMenu()

    @patch('builtins.print')
    def test_display_menu_prints_banner(self, mock_print):
        """Memastikan display_menu mencetak banner utama ke layar."""
        self.menu.display_menu()

        # Memastikan fungsi print bawaan Python dipanggil berkali-kali
        self.assertGreater(mock_print.call_count, 0)

    @patch('builtins.print')
    def test_display_tools_prints_banner(self, mock_print):
        """Memastikan display_tools mencetak banner sub-menu."""
        self.menu.display_tools()
        self.assertGreater(mock_print.call_count, 0)

    # Mencegat input keyboard dan memaksanya langsung mengembalikan string " 1 "
    @patch('builtins.input', return_value=" 1 ")
    def test_handle_input_cleans_whitespace(self, mock_input):
        """Memastikan handle_input meminta input dan membersihkan spasi (strip)."""
        list_menu = [1, 2]
        result = self.menu.handle_input(list_menu)

        # Memastikan spasi terhapus (menjadi "1" bukan " 1 ")
        self.assertEqual(result, "1")
        mock_input.assert_called_once()

    # Mencegat metode internal milik TerminalMenu itu sendiri
    @patch.object(TerminalMenu, 'display_menu')
    @patch.object(TerminalMenu, 'handle_input', return_value="2")
    def test_start_calls_methods_correctly(self, mock_handle_input, mock_display_menu):
        """Memastikan metode start menjalankan urutan display dan input dengan benar."""
        list_menu = [1, 2]
        result = self.menu.start(list_menu)

        mock_display_menu.assert_called_once()
        mock_handle_input.assert_called_once_with(list_menu)
        self.assertEqual(result, "2")

    @patch('os.system')
    @patch('os.name', 'nt')  # Memaksa deteksi OS menjadi Windows
    def test_clear_screen_windows(self, mock_system):
        """Memastikan clear_screen memanggil 'cls' di lingkungan Windows."""
        self.menu.clear_screen()
        mock_system.assert_called_once_with('cls')

    @patch('os.system')
    @patch('os.name', 'posix')  # Memaksa deteksi OS menjadi Linux/Mac
    def test_clear_screen_linux(self, mock_system):
        """Memastikan clear_screen memanggil 'clear' di lingkungan Mac/Linux."""
        self.menu.clear_screen()
        mock_system.assert_called_once_with('clear')


if __name__ == '__main__':
    unittest.main()
