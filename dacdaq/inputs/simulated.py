import time
import numpy as np
from .base import BaseInstrument

class SimulatedInstrument(BaseInstrument):
    """
    Our simulated instrument, now adhering to the BaseInstrument interface.
    """
    def __init__(self):
        super().__init__()
        self.baseline = 10.0
    
    def get_name(self):
        return "Simulated Instrument (Random)"

    def connect_instrument(self):
        print("Simulated Instrument Connected.")
        return True # Always succeeds

    def read_voltage(self):
        """Simulates a 50ms hardware read time."""
        time.sleep(0.05) 
        noise = np.random.normal(0.0, 0.2)
        drift = np.sin(np.pi * np.random.random()) * 0.1
        self.baseline += drift
        return self.baseline + noise

    def close(self):
        print("Simulated Instrument Disconnected.")