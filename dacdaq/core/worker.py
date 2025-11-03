import time
from PyQt6.QtCore import QObject, pyqtSignal, QMutex, QMutexLocker
from dacdaq.outputs.csv_sink import CsvSink
from dacdaq.outputs.event_sink import EventSink # <-- 1. IMPORT
from dacdaq.processing.filters import MovingAverageFilter

class AcquisitionWorker(QObject):
    # ... (signals are unchanged)
    data_ready = pyqtSignal(float)
    processed_data_ready = pyqtSignal(float)
    finished = pyqtSignal()
    error = pyqtSignal(str) 

    def __init__(self, instrument_class, config):
        super().__init__()
        self.InstrumentClass = instrument_class
        self.config = config
        self.instrument = None
        self.data_sink = None
        self.event_sink = None # <-- 2. ADD EVENT SINK
        
        self._mutex = QMutex()
        self._is_running = True
        self._is_paused = False
        
        self.processor = MovingAverageFilter(window_size=10)

    def run_acquisition(self):
        try:
            # 1. Connect to instrument (unchanged)
            self.instrument = self.InstrumentClass()
            if not self.instrument.connect_instrument():
                # ... (error handling unchanged)
                self.error.emit(f"Failed to connect to {self.instrument.get_name()}")
                self.finished.emit()
                return

            # 2. Open data sink (unchanged)
            self.data_sink = CsvSink(self.config["output_file"], self.config)
            if not self.data_sink.open():
                # ... (error handling unchanged)
                self.error.emit(f"Failed to open output file: {self.config['output_file']}")
                self.finished.emit()
                return

            # --- 3. NEW: Open Event Sink ---
            self.event_sink = EventSink(self.config["output_file"], self.config)
            if not self.event_sink.open():
                self.error.emit(f"Failed to open event file.")
                self.finished.emit()
                return
            # --- END NEW ---

            # 4. Acquisition loop (unchanged)
            print("Acquisition thread started...")
            while True:
                with QMutexLocker(self._mutex):
                    if not self._is_running:
                        break
                    while self._is_paused:
                        self._mutex.unlock() 
                        time.sleep(0.1)
                        self._mutex.lock()
                        if not self._is_running:
                            break
                
                raw_voltage = self.instrument.read_voltage()
                filtered_voltage = self.processor.process(raw_voltage)
                
                self.data_sink.write(raw_voltage, filtered_voltage)
                
                self.data_ready.emit(raw_voltage)
                self.processed_data_ready.emit(filtered_voltage)
            
            print("Acquisition loop finished.")
            
        except Exception as e:
            self.error.emit(f"Error in acquisition thread: {e}")
            
        finally:
            if self.instrument:
                self.instrument.close()
            if self.data_sink:
                self.data_sink.close()
            if self.event_sink: # <-- 5. CLOSE EVENT SINK
                self.event_sink.close()
            self.finished.emit()

    def stop(self):
        # ... (unchanged)
        with QMutexLocker(self._mutex):
            self._is_running = False
            self._is_paused = False
        print("Requesting thread stop...")

    def pause(self):
        # ... (unchanged)
        with QMutexLocker(self._mutex):
            self._is_paused = True
        print("Requesting thread pause...")

    def resume(self):
        # ... (unchanged)
        with QMutexLocker(self._mutex):
            self._is_paused = False
        print("Requesting thread resume...")
        
    # --- 6. NEW PUBLIC METHOD ---
    def add_event_comment(self, comment):
        """
        Thread-safe method to write a comment to the event log.
        This is called from the main GUI thread.
        """
        if self.event_sink:
            # The event sink's write method is simple and fast,
            # so we can call it directly.
            # For a slow operation, you'd use a signal.
            self.event_sink.write_event(comment)