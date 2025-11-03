import pyvisa
from .base import BaseInstrument

# NOTE: You may need to install a "backend" for pyvisa, e.g.:
# pip install pyvisa-py (for serial/USB) or NI-VISA (for GPIB)

class Keithley2000(BaseInstrument):
    """
    A real instrument class for a Keithley 2000 series voltmeter.
    It communicates using SCPI commands over VISA.
    
    Change the VISA_ADDRESS to match your instrument's connection.
    Find it using the 'NI MAX' tool or similar.
    """
    # Example: 'GPIB0::16::INSTR' or 'ASRL/dev/ttyUSB0::INSTR'
    VISA_ADDRESS = "GPIB0::16::INSTR" 

    def __init__(self):
        super().__init__()
        self.rm = None
        self.instrument = None
    
    def get_name(self):
        return "Keithley 2000 (VISA)"

    def connect_instrument(self):
        """Tries to connect to the instrument at the specified VISA address."""
        print(f"Connecting to {self.get_name()} at {self.VISA_ADDRESS}...")
        try:
            self.rm = pyvisa.ResourceManager()
            self.instrument = self.rm.open_resource(self.VISA_ADDRESS)
            self.instrument.timeout = 5000 # 5 second timeout
            
            # Reset and configure the instrument
            self.instrument.write("*RST") # Reset
            self.instrument.write(":SENSE:FUNCTION 'VOLT:DC'") # Set to DC Voltage
            self.instrument.write(":SENSE:VOLTAGE:DC:RANGE:AUTO ON") # Autoranging
            
            # Ask for its ID and print it
            identity = self.instrument.query("*IDN?")
            print(f"Successfully connected. ID: {identity.strip()}")
            return True
            
        except Exception as e:
            print(f"ERROR connecting to Keithley: {e}")
            return False

    def read_voltage(self):
        """
        Asks the instrument to take one reading.
        This is a "blocking" call, which is why it's in a thread.
        """
        try:
            # :READ? is a common SCPI command to trigger and return one reading
            voltage_str = self.instrument.query(":READ?")
            return float(voltage_str)
        except Exception as e:
            print(f"Error reading voltage: {e}")
            # Return a "Not a Number" to signal an error
            return float('nan') 

    def close(self):
        """Closes the VISA connection."""
        if self.instrument:
            self.instrument.close()
        if self.rm:
            self.rm.close()
        print(f"Disconnected from {self.get_name()}.")