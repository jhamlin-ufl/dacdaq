from PyQt6.QtCore import QObject

class BaseInstrument(QObject):
    """
    An abstract base class for all instruments.
    It inherits from QObject so it can be moved to a thread.
    """
    def __init__(self):
        super().__init__()
    
    def connect_instrument(self):
        """Connect to the hardware. Returns True on success."""
        raise NotImplementedError
        
    def read_voltage(self):
        """Read a single value from the instrument."""
        raise NotImplementedError

    def close(self):
        """Disconnect from the hardware."""
        raise NotImplementedError

    def get_name(self):
        """Return a human-readable name for the instrument."""
        return "Base Instrument"