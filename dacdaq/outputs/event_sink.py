import csv
import datetime

class EventSink:
    """
    Handles writing timestamped user events (comments) to a .events.csv file.
    """
    def __init__(self, filepath, config_details):
        # We'll automatically append '.events' to the main log file name
        base_filepath = filepath.rsplit('.', 1)[0]
        self.filepath = f"{base_filepath}.events.csv"
        self.config_details = config_details
        self.file_handle = None
        self.writer = None

    def open(self):
        """Opens the event file and writes the header."""
        try:
            self.file_handle = open(self.filepath, 'w', newline='')
            self.writer = csv.writer(self.file_handle)
            
            # Write comments from config
            for line in self.config_details.get("comments", "").split('\n'):
                self.writer.writerow([f"# {line}"])
            
            # Write metadata
            writer = self.writer
            writer.writerow([f"# Instrument: {self.config_details.get('instrument_name', 'Unknown')}"])
            writer.writerow([f"# Start Time: {datetime.datetime.now().isoformat()}"])
            writer.writerow([""]) # Spacer
            
            # Write data header
            writer.writerow(["Timestamp", "Event_Comment"])
            self.file_handle.flush()
            print(f"Opened event sink: {self.filepath}")
            return True
        except Exception as e:
            print(f"Error opening EventSink: {e}")
            return False

    def write_event(self, comment):
        """Writes a new timestamped event to the file."""
        if self.writer:
            timestamp = datetime.datetime.now().isoformat()
            # Sanitize comment to remove newlines
            clean_comment = comment.replace('\n', ' ').replace('\r', ' ')
            self.writer.writerow([timestamp, clean_comment])
            self.file_handle.flush()
            print(f"Logged event: {clean_comment}")

    def close(self):
        """Closes the file handle."""
        if self.file_handle:
            print(f"Closing event sink: {self.filepath}")
            self.file_handle.close()
            self.file_handle = None
            self.writer = None