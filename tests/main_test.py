import unittest
from unittest.mock import patch, MagicMock
from main import main

class TestMainLogic(unittest.TestCase):

    # Kita mencegat class TerminalMenu agar tidak mencetak apa-apa ke layar
    @patch('main.TerminalMenu')
    @patch('builtins.print')
    def test_main_exit_path(self, mock_print, mock_menu_class):
        """Memastikan fungsi main bisa keluar dengan aman saat user memilih opsi 2."""

        # 1. Setup objek tiruan
        mock_menu_instance = MagicMock()
        mock_menu_class.return_value = mock_menu_instance

        # 2. Paksa menu.start() seolah-olah user langsung mengetik "2" (Exit)
        mock_menu_instance.start.return_value = "2"

        # 3. Eksekusi fungsi main (akan langsung kena 'break' dan selesai)
        main()

        # 4. Verifikasi bahwa pesannya benar-benar dicetak
        mock_print.assert_any_call("[INFO] Keluar dari program. Sampai jumpa!")


if __name__ == '__main__':
    unittest.main()
