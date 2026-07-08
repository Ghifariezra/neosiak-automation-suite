from src.core import NeosiakBot

class PengisianKRSBot(NeosiakBot):
    """Bot untuk mengotomatisasi pengisian KRS di portal Neosiak."""
    
    def __init__(self):
        super().__init__()

    def run(self):
        """Contoh alur eksekusi bot"""
        self._time.sleep(2)
        self.login()
        
        self._time.sleep(2)
        self.open_sidebar(go_to="Pengisian KRS")
        
        self._time.sleep(2)
        self.quit()