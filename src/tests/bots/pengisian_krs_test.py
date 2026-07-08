import unittest
from unittest.mock import patch, MagicMock
from bots.pengisian_krs import PengisianKRSBot


class TestPengisianKRSBot(unittest.TestCase):
    @patch('core.driver.SB')
    @patch('time.sleep')
    def test_run_executes_correct_sequence(self, mock_sleep, mock_sb):
        """Memastikan alur metode run() mengeksekusi login, buka sidebar, dan quit dengan benar."""
        bot = PengisianKRSBot()

        # Mocking fungsi-fungsi internal agar tidak benar-benar menjalankan browser saat testing alur
        bot.login = MagicMock()
        bot.open_sidebar = MagicMock()
        bot.quit = MagicMock()

        # Eksekusi alur
        bot.run()

        # 1. Verifikasi login dipanggil
        bot.login.assert_called_once()

        # 2. Verifikasi open_sidebar dipanggil dengan parameter yang tepat
        bot.open_sidebar.assert_called_once_with(go_to="Pengisian KRS")

        # 3. Verifikasi quit dipanggil untuk mematikan instance
        bot.quit.assert_called_once()

        # 4. Verifikasi sleep digunakan di antara pemanggilan
        self.assertGreater(mock_sleep.call_count, 0)


if __name__ == '__main__':
    unittest.main()
