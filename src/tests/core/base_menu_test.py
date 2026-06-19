import unittest
from core.base_menu import BaseMenu


class TestBaseMenu(unittest.TestCase):

    def test_cannot_instantiate_abstract_class(self):
        """Memastikan BaseMenu tidak bisa diinisiasi secara langsung."""
        # Jika kita memaksa membuat objek dari BaseMenu, Python harus mengeluarkan TypeError
        with self.assertRaises(TypeError):
            BaseMenu()

    def test_concrete_class_must_implement_all_methods(self):
        """Memastikan class turunan wajib mengimplementasikan semua abstract method."""

        # Membuat class tiruan yang mewarisi BaseMenu tapi "lupa" mengimplementasikan fungsinya
        class IncompleteMenu(BaseMenu):
            pass

        # Harus gagal dengan TypeError karena melanggar kontrak
        with self.assertRaises(TypeError):
            IncompleteMenu()


if __name__ == '__main__':
    unittest.main()
