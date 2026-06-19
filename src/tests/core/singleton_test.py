import unittest
from core.singleton import SingletonMeta

class DummyClass(metaclass=SingletonMeta):
    def __init__(self):
        self.state = "active"

# 1. Harus membuat class yang mewarisi unittest.TestCase
class TestSingleton(unittest.TestCase):
    def test_singleton_creates_only_one_instance(self):
        obj1 = DummyClass()
        obj2 = DummyClass()

        # 2. Tidak bisa pakai assert bawaan, harus pakai method khusus dari TestCase
        self.assertIs(obj1, obj2)


# 3. Harus ada blok ini agar file bisa dijalankan sendiri
if __name__ == '__main__':
    unittest.main()