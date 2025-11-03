import csv
import datetime

class CsvSink:
    """
    Handles writing acquired data to a CSV file.
    NOW saves both raw and processed data.
    """
    def __init__(self, filepath, config_details):
        self.filepath = filepath
        self.config_details = config_details
        self.file_handle = None
        self.writer = None

    def open(self):
        """Opens the file and writes the full header."""
        try:
            self.file_handle = open(self.filepath, 'w', newline='')
            self.writer = csv.writer(self.file_handle)
            
            # Write comments
            for line in self.config_details.get("comments", "").split('\n'):
                self.writer.writerow([f"# {line}"])
            
            # Write metadata
            writer = self.writer
            writer.writerow([f"# Instrument: {self.config_details.get('instrument_name', 'Unknown')}"])
            writer.writerow([f"# Start Time: {datetime.datetime.now().isoformat()}"])
            writer.writerow([""]) # Spacer
            
            # --- MODIFIED ---
            # Write new data header
            writer.writerow(["Timestamp", "Voltage_Raw (V)", "Voltage_Filtered (V)"])
            # --- END MODIFIED ---

            self.file_handle.flush()
            print(f"Opened data sink: {self.filepath}")
            return True
        except Exception as e:
            print(f"Error opening CsvSink: {e}")
            return False

    # --- MODIFIED ---
    def write(self, raw_data, filtered_data):
        """Writes a single row of data."""
        if self.writer:
            timestamp = datetime.datetime.now().isoformat()
            self.writer.writerow([timestamp, raw_data, filtered_data])
            self.file_handle.flush() # Ensure data is written
    # --- END MODIFIED ---

    def close(self):
        """Closes the file handle."""
        if self.file_handle:
            print(f"Closing data sink: {self.filepath}")
            self.file_handle.close()
            self.file_handle = None
            self.writer = None