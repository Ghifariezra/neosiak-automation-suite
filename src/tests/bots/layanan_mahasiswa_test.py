import unittest
from unittest.mock import patch, MagicMock
from bots.layanan_mahasiswa import LayananMahasiswaBot

class TestLayananMahasiswaBot(unittest.TestCase):
    @patch('core.driver.SB')
    # Memblokir time.sleep agar tes berjalan tanpa henti (instan)
    @patch('time.sleep')
    def test_answer_questions_executes_scripts(self, mock_sleep, mock_sb):
        """Memastikan eksekusi injeksi JS berjalan sempurna melintasi semua stepper."""
        mock_sb_instance = MagicMock()
        mock_sb.return_value = mock_sb_instance
        mock_driver = MagicMock()
        mock_sb_instance.__enter__.return_value = mock_driver

        bot = LayananMahasiswaBot()

        # Eksekusi fungsi dengan 2 halaman stepper
        bot.answer_questions(total_stepper=2, pilihan="Setuju")

        # Verifikasi bahwa driver mengeksekusi JavaScript
        self.assertGreater(bot.driver.execute_script.call_count, 0)

        # Verifikasi bahwa time.sleep dipanggil untuk memberi jeda antar stepper
        self.assertGreater(mock_sleep.call_count, 0)

    @patch('core.driver.SB')
    def test_go_to_fill_survey_clicks_correct_link(self, mock_sb):
        """Memastikan navigasi form survei menekan elemen a href yang tepat."""
        mock_sb_instance = MagicMock()
        mock_sb.return_value = mock_sb_instance
        mock_driver = MagicMock()
        mock_sb_instance.__enter__.return_value = mock_driver

        bot = LayananMahasiswaBot()
        bot.go_to_fill_survey()

        mock_driver.click.assert_called_with(
            'a[href="https://neosiak.univpancasila.ac.id/pertanyaan-laymhs"]'
        )


if __name__ == '__main__':
    unittest.main()
