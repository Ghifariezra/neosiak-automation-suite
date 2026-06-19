from core.driver import Driver

class NeosiakBot(Driver):
    """Bot dasar untuk mengotomatisasi interaksi dengan portal Neosiak."""

    __url = "https://neosiak.univpancasila.ac.id"

    def __init__(self):
        super().__init__()
        self.open(self.__url)

    def login(self):
        """Metode untuk login ke portal Neosiak."""
        nim_or_email = self._os.getenv("NIM_OR_EMAIL") if self._os.getenv(
            "NIM_OR_EMAIL") else "45XXXXXXXX"
        password = self._os.getenv("PASSWORD") if self._os.getenv(
            "PASSWORD") else "password_anda"

        self.driver.type('input[name="username"]', nim_or_email)
        self.driver.type('input[name="password"]', password)
        self.driver.click('button[type="submit"]')