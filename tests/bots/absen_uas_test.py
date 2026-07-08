import unittest
from unittest.mock import patch, MagicMock
from src.bots.absen_uas import AbsenUASBot


class TestAbsenUASBot(unittest.TestCase):

    @patch('src.core.driver.SB')
    def test_find_course_no_table(self, mock_sb):
        """Memastikan bot merespons dengan benar saat tabel tidak ditemukan."""
        bot = AbsenUASBot()
        # Simulasikan is_element_present mengembalikan False (tabel tidak ada)
        bot.driver.is_element_present.return_value = False

        result = bot.find_course("Sistem Informasi Geografis")
        self.assertIsNone(result)

    @patch('src.core.driver.SB')
    def test_find_course_no_input(self, mock_sb):
        """Memastikan bot merespons None jika tidak ada input mata kuliah."""
        bot = AbsenUASBot()
        # Simulasikan tabel ditemukan
        bot.driver.is_element_present.return_value = True

        result = bot.find_course("")
        self.assertIsNone(result)

    @patch('src.core.driver.SB')
    @patch('time.sleep')
    def test_find_course_success(self, mock_sleep, mock_sb):
        """Memastikan bot berhasil menemukan mata kuliah dan melakukan klik unduh."""
        bot = AbsenUASBot()

        # Simulasikan semua elemen yang dicek is_element_present selalu True
        bot.driver.is_element_present.return_value = True

        # Simulasikan tabel memiliki 1 baris
        bot.driver.find_elements.return_value = ['dummy_row_1']

        # Setup mock untuk elemen yang direturn oleh find_element
        mock_course_element = MagicMock()
        mock_course_element.text = "Sistem Informasi Geografis"

        mock_time_element = MagicMock()
        mock_time_element.text = "11:00"

        mock_link_element = MagicMock()
        mock_link_element.get_attribute.return_value = "https://neosiak.mock/download"

        # Fungsi side_effect untuk mengembalikan elemen yang sesuai berdasarkan selector-nya
        def mock_find_element_side_effect(selector):
            if "td:nth-child(3)" in selector:
                return mock_course_element
            elif "td:nth-child(8)" in selector:
                return mock_time_element
            elif "a" in selector:
                return mock_link_element
            return MagicMock()

        bot.driver.find_element.side_effect = mock_find_element_side_effect

        # Eksekusi fungsi
        result = bot.find_course("Sistem Informasi Geografis")

        # Verifikasi
        self.assertIsNotNone(result)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["course"], "Sistem Informasi Geografis")
        self.assertEqual(result["start_time"], "11:00")

        # Pastikan trik JS hapus atribut target, klik, dan go_back dieksekusi
        bot.driver.execute_script.assert_called()
        bot.driver.click.assert_called()
        bot.driver.go_back.assert_called()

    @patch('src.core.driver.SB')
    @patch('time.sleep')
    def test_find_course_failed_not_open(self, mock_sleep, mock_sb):
        """Memastikan bot menangani status file yang belum bisa diunduh (misal: 'Belum dibuka')."""
        bot = AbsenUASBot()

        # Simulasikan tabel ada, TAPI link <a> tidak ada (artinya badge text)
        def mock_is_element_present_side_effect(selector):
            if " a" in selector:
                return False  # Link download tidak ada
            return True  # Tabel dan kolom lainnya ada

        bot.driver.is_element_present.side_effect = mock_is_element_present_side_effect
        bot.driver.find_elements.return_value = ['dummy_row_1']

        mock_course_element = MagicMock()
        mock_course_element.text = "Data Mining"

        mock_time_element = MagicMock()
        mock_time_element.text = "13:30"

        mock_badge_element = MagicMock()
        mock_badge_element.text = "Belum dibuka"

        def mock_find_element_side_effect(selector):
            if "td:nth-child(3)" in selector:
                return mock_course_element
            elif "td:nth-child(8)" in selector:
                return mock_time_element
            elif "td:nth-child(10)" in selector:
                return mock_badge_element
            return MagicMock()

        bot.driver.find_element.side_effect = mock_find_element_side_effect

        # Eksekusi
        result = bot.find_course("Data Mining")

        # Verifikasi
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["reason"], "Belum dibuka")

    @patch('src.core.driver.SB')
    @patch('time.sleep')
    @patch.object(AbsenUASBot, 'login')
    @patch.object(AbsenUASBot, 'open_sidebar')
    @patch.object(AbsenUASBot, 'find_course')
    @patch.object(AbsenUASBot, 'quit')
    def test_run_success_flow(self, mock_quit, mock_find, mock_sidebar, mock_login, mock_sleep, mock_sb):
        """Memastikan alur metode run berjalan dengan benar saat form diisi."""
        bot = AbsenUASBot()

        # Simulasikan execute_script
        # Panggilan pertama adalah injeksi HTML (mereturn None)
        # Panggilan kedua adalah polling (mereturn nilai input pengguna)
        bot.driver.execute_script.side_effect = [None, "Kecerdasan Buatan"]

        mock_find.return_value = {"status": "success"}

        # Eksekusi
        bot.run()

        # Verifikasi pemanggilan metode internal sesuai urutan
        mock_login.assert_called_once()
        mock_sidebar.assert_called_once_with(go_to="Unduh Soal UAS")
        mock_find.assert_called_once_with(course_name="Kecerdasan Buatan")
        mock_quit.assert_called_once()

    @patch('src.core.driver.SB')
    @patch('time.sleep')
    @patch.object(AbsenUASBot, 'login')
    @patch.object(AbsenUASBot, 'open_sidebar')
    @patch.object(AbsenUASBot, 'find_course')
    @patch.object(AbsenUASBot, 'quit')
    def test_run_empty_input_cancels_operation(self, mock_quit, mock_find, mock_sidebar, mock_login, mock_sleep, mock_sb):
        """Memastikan bot membatalkan operasi jika input form kosong/di-cancel."""
        bot = AbsenUASBot()

        # Simulasikan pengguna submit tapi form kosong ""
        bot.driver.execute_script.side_effect = [None, ""]

        bot.run()

        # find_course TIDAK BOLEH dipanggil jika string kosong
        mock_find.assert_not_called()
        mock_quit.assert_called_once()


if __name__ == '__main__':
    unittest.main()
