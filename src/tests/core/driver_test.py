import unittest
from unittest.mock import patch, MagicMock
from core.driver import Driver


class TestDriver(unittest.TestCase):
    def setUp(self):
        """Reset instance Singleton."""
        Driver._instances = {}

    @patch('core.driver.SB')
    def test_driver_initialization(self, mock_sb_class):
        """Memastikan Driver diinisialisasi dengan parameter yang benar."""
        mock_sb_instance = MagicMock()
        mock_sb_class.return_value = mock_sb_instance
        mock_sb_instance.__enter__.return_value = "mocked_driver_object"

        driver_obj = Driver()

        mock_sb_class.assert_called_once_with(
            uc=True,
            locale="id-ID",
            maximize=True
        )
        self.assertEqual(driver_obj.get_driver(), "mocked_driver_object")

    @patch('core.driver.SB')
    def test_driver_open_and_quit(self, mock_sb_class):
        """Memastikan metode open dan quit memanggil fungsi SeleniumBase yang tepat."""
        mock_sb_instance = MagicMock()
        mock_sb_class.return_value = mock_sb_instance
        mock_driver_methods = MagicMock()
        mock_sb_instance.__enter__.return_value = mock_driver_methods

        driver_obj = Driver()
        test_url = "https://neosiak.univpancasila.ac.id"
        driver_obj.open(test_url)

        mock_driver_methods.open.assert_called_once_with(test_url)

        driver_obj.quit()
        mock_sb_instance.__exit__.assert_called_once_with(None, None, None)


if __name__ == '__main__':
    unittest.main()
