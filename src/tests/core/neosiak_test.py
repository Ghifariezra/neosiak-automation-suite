import unittest
from unittest.mock import patch, MagicMock
from core.neosiak import NeosiakBot

class TestNeosiakBot(unittest.TestCase):
    @patch('core.driver.SB')
    def test_login_uses_environment_variables(self, mock_sb):
        """Memastikan login mengetikkan kredensial dengan benar menggunakan selector."""
        mock_sb_instance = MagicMock()
        mock_sb.return_value = mock_sb_instance
        mock_driver = MagicMock()
        mock_sb_instance.__enter__.return_value = mock_driver

        # Menyimulasikan environment variable tanpa menyentuh file .env asli
        with patch.dict('os.environ', {"NIM_OR_EMAIL": "test_user", "PASSWORD": "test_password"}):
            bot = NeosiakBot()
            bot.login()

        # Verifikasi input dan klik
        mock_driver.type.assert_any_call('input[name="username"]', "test_user")
        mock_driver.type.assert_any_call(
            'input[name="password"]', "test_password")
        mock_driver.click.assert_called_with('button[type="submit"]')

    @patch('core.driver.SB')
    @patch('time.sleep')
    def test_open_sidebar_ditutup_executes_js(self, mock_sleep, mock_sb):
        """Memastikan bot menyuntikkan JS (Toast & Overlay) ketika menu target ditutup."""
        # Setup Mock Driver
        mock_sb_instance = MagicMock()
        mock_sb.return_value = mock_sb_instance
        mock_driver = MagicMock()
        mock_sb_instance.__enter__.return_value = mock_driver

        # 1. Mock elemen sidebar
        mock_sidebar_element = MagicMock()
        mock_sidebar_element.text = "Pengisian KRS"
        mock_driver.find_elements.return_value = [mock_sidebar_element]

        # 2. Mock elemen informasi status (Single WebElement)
        mock_info_element = MagicMock()
        mock_info_element.text = "Informasi !!! Pengisian KRS Sudah Ditutup."
        mock_driver.find_element.return_value = mock_info_element

        # Inisialisasi bot & jalankan fungsi dengan parameter dinamis
        bot = NeosiakBot()
        bot.open_sidebar(go_to="Pengisian KRS")

        # Verifikasi bahwa menu diklik sesuai teks
        mock_driver.click_link_text.assert_called_with("Pengisian KRS")

        # Verifikasi bahwa execute_script dipanggil untuk memunculkan UI
        self.assertGreater(mock_driver.execute_script.call_count, 0)

        # Verifikasi bahwa sleep dipanggil untuk memberi waktu UI muncul
        self.assertGreater(mock_sleep.call_count, 0)

    @patch('core.driver.SB')
    @patch('time.sleep')
    def test_open_sidebar_terbuka_no_js(self, mock_sleep, mock_sb):
        """Memastikan bot tidak menyuntikkan JS jika menu target tidak ditutup."""
        # Setup Mock Driver
        mock_sb_instance = MagicMock()
        mock_sb.return_value = mock_sb_instance
        mock_driver = MagicMock()
        mock_sb_instance.__enter__.return_value = mock_driver

        # 1. Mock elemen sidebar
        mock_sidebar_element = MagicMock()
        mock_sidebar_element.text = "Pengisian KRS"
        mock_driver.find_elements.return_value = [mock_sidebar_element]

        # 2. Mock elemen informasi (Skenario Aktif / Tidak ada kata "Ditutup")
        mock_info_element = MagicMock()
        mock_info_element.text = "Silakan melakukan pengisian untuk semester ini."
        mock_driver.find_element.return_value = mock_info_element

        bot = NeosiakBot()
        bot.open_sidebar(go_to="Pengisian KRS")

        # Verifikasi bahwa menu tetap diklik
        mock_driver.click_link_text.assert_called_with("Pengisian KRS")

        # Verifikasi execute_script TIDAK dipanggil karena status bukan "Ditutup"
        mock_driver.execute_script.assert_not_called()


if __name__ == '__main__':
    unittest.main()
