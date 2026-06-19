import unittest
from unittest.mock import patch, MagicMock
from core.driver import Driver

# 1. Harus membuat class yang mewarisi unittest.TestCase
class TestDriver(unittest.TestCase):

    # 2. Pengganti @pytest.fixture(autouse=True)
    def setUp(self):
        """Metode bawaan unittest yang otomatis dijalankan SEBELUM setiap test dimulai."""
        Driver._instances = {}

    @patch('core.driver.SB')  # Mencegat class SB dari seleniumbase
    def test_driver_initialization(self, mock_sb_class):
        """Memastikan Driver diinisialisasi dengan parameter yang benar."""

        # Konfigurasi objek tiruan (Mock) untuk Context Manager (__enter__)
        mock_sb_instance = MagicMock()
        mock_sb_class.return_value = mock_sb_instance
        mock_sb_instance.__enter__.return_value = "mocked_driver_object"

        # Eksekusi
        driver_obj = Driver()

        # Verifikasi parameter yang dikirim ke SB()
        mock_sb_class.assert_called_once_with(
            uc=True,
            locale="id-ID",
            maximize=True
        )

        # 3. Verifikasi metode get_driver menggunakan metode bawaan TestCase
        self.assertEqual(driver_obj.get_driver(), "mocked_driver_object")

    @patch('core.driver.SB')
    def test_driver_open_and_quit(self, mock_sb_class):
        """Memastikan metode open dan quit memanggil fungsi SeleniumBase yang tepat."""

        # Setup Mock
        mock_sb_instance = MagicMock()
        mock_sb_class.return_value = mock_sb_instance

        # Mock untuk objek yang dikembalikan oleh __enter__
        mock_driver_methods = MagicMock()
        mock_sb_instance.__enter__.return_value = mock_driver_methods

        driver_obj = Driver()

        # Tes metode open()
        test_url = "https://neosiak.univpancasila.ac.id"
        driver_obj.open(test_url)
        mock_driver_methods.open.assert_called_once_with(test_url)

        # Tes metode quit()
        driver_obj.quit()
        mock_sb_instance.__exit__.assert_called_once_with(None, None, None)


# 4. Harus ada blok ini agar file bisa dijalankan sendiri
if __name__ == '__main__':
    unittest.main()
