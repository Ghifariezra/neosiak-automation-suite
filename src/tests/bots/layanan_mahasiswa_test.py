import unittest
from unittest.mock import patch, MagicMock
from bots.layanan_mahasiswa import LayananMahasiswaBot
from core.driver import Driver

# 1. Bungkus dengan class yang mewarisi unittest.TestCase
class TestLayananMahasiswaBot(unittest.TestCase):

    # 2. Ganti @pytest.fixture dengan setUp
    def setUp(self):
        """Reset dictionary instance pada SingletonMeta sebelum setiap tes dijalankan."""
        Driver._instances = {}

    # Kita mem-patch SB dari core.driver, bukan mematikan __init__ nya
    @patch('core.driver.SB')
    # 3. Tambahkan 'self'
    def test_login_method_uses_correct_selectors(self, mock_sb):
        """Memastikan metode login mengetik di kolom yang benar dan menekan submit."""

        # Setup Mock agar SeleniumBase menghasilkan objek tiruan, bukan browser asli
        mock_sb_instance = MagicMock()
        mock_sb.return_value = mock_sb_instance
        mock_driver = MagicMock()
        mock_sb_instance.__enter__.return_value = mock_driver

        # Inisialisasi bot (Sekarang aman, karena self.driver akan berisi mock_driver)
        bot = LayananMahasiswaBot()

        # Eksekusi metode yang ingin dites
        bot.login("4524212200", "password123")

        # Verifikasi input pada mock_driver
        bot.driver.type.assert_any_call('input[name="username"]', "4524212200")
        bot.driver.type.assert_any_call(
            'input[name="password"]', "password123")

        # Verifikasi klik
        bot.driver.click.assert_called_with('button[type="submit"]')

    @patch('core.driver.SB')
    # Tambahkan 'self'
    def test_answer_questions_executes_scripts(self, mock_sb):
        """Memastikan logika looping JS dieksekusi berdasarkan total stepper."""

        # Setup Mock yang sama
        mock_sb_instance = MagicMock()
        mock_sb.return_value = mock_sb_instance
        mock_driver = MagicMock()
        mock_sb_instance.__enter__.return_value = mock_driver

        bot = LayananMahasiswaBot()

        # Tes menjalankan answer_questions untuk 3 stepper
        bot.answer_questions(total_stepper=3, pilihan="Setuju")

        # 4. Ganti 'assert >' dengan method bawaan TestCase: assertGreater
        self.assertGreater(bot.driver.execute_script.call_count, 0)


# 5. Blok eksekusi utama
if __name__ == '__main__':
    unittest.main()
