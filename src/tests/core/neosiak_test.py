import unittest
from unittest.mock import patch, MagicMock
from core.neosiak import NeosiakBot
from core.driver import Driver


class TestNeosiakBot(unittest.TestCase):
    def setUp(self):
        """Reset instance Singleton."""
        Driver._instances = {}

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


if __name__ == '__main__':
    unittest.main()
