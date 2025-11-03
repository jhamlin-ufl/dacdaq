import numpy as np
import pyqtgraph as pg
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QCheckBox, QDoubleSpinBox
)
from PyQt6.QtCore import QThread, Qt
from dacdaq.core.worker import AcquisitionWorker

class DacDaqWindow(QMainWindow):
    """
    The main application window.
    Now with manual Y-axis graph controls.
    """
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.setWindowTitle(f"DacDAQ - Logging to: {config['output_file']}")
        self.setGeometry(100, 100, 800, 750) 

        # Buffers
        self.raw_data_buffer = np.zeros(500)
        self.filtered_data_buffer = np.zeros(500)
        
        # --- Plot Widget ---
        pg.setConfigOption("background", "w")
        pg.setConfigOption("foreground", "k")
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.addLegend()
        self.plot_widget.setLabel("left", "Voltage (V)")
        self.plot_widget.setLabel("bottom", "Time (samples)")
        self.plot_widget.showGrid(x=True, y=True, alpha=0.5)
        
        self.raw_plot_curve = self.plot_widget.plot(
            pen=pg.mkPen('k', width=1, style=Qt.PenStyle.DotLine), 
            name="Raw Data"
        )
        self.filtered_plot_curve = self.plot_widget.plot(
            pen=pg.mkPen('r', width=2), 
            name="Filtered Data"
        )

        self.acquisition_thread = None
        self.acquisition_worker = None

        # --- Main Layout ---
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.addWidget(self.plot_widget)

        self.status_label = QLabel(f"Instrument: {config['instrument_name']}")
        main_layout.addWidget(self.status_label)
        
        # --- Event Log Layout ---
        event_layout = QHBoxLayout()
        event_layout.addWidget(QLabel("Add Event:"))
        self.event_entry_box = QLineEdit()
        self.event_entry_box.setPlaceholderText("Type a comment and press Enter...")
        self.event_entry_box.returnPressed.connect(self.log_event)
        event_layout.addWidget(self.event_entry_box)
        self.add_event_button = QPushButton("Add Event")
        self.add_event_button.clicked.connect(self.log_event)
        event_layout.addWidget(self.add_event_button)
        main_layout.addLayout(event_layout)
        
        # --- Graph Controls Layout ---
        graph_controls_layout = QHBoxLayout()
        
        self.autorange_check = QCheckBox("Auto-Range Y-Axis")
        self.autorange_check.setChecked(True)
        self.autorange_check.stateChanged.connect(self.toggle_autorange)
        graph_controls_layout.addWidget(self.autorange_check)
        
        graph_controls_layout.addStretch()
        
        graph_controls_layout.addWidget(QLabel("Y-Min:"))
        self.ymin_spin = QDoubleSpinBox()
        self.ymin_spin.setRange(-10000, 10000)
        self.ymin_spin.setValue(0)
        self.ymin_spin.setDecimals(3)
        self.ymin_spin.editingFinished.connect(self.apply_manual_range)
        graph_controls_layout.addWidget(self.ymin_spin)
        
        graph_controls_layout.addWidget(QLabel("Y-Max:"))
        self.ymax_spin = QDoubleSpinBox()
        self.ymax_spin.setRange(-10000, 10000)
        self.ymax_spin.setValue(20)
        self.ymax_spin.setDecimals(3)
        self.ymax_spin.editingFinished.connect(self.apply_manual_range)
        graph_controls_layout.addWidget(self.ymax_spin)
        
        self.toggle_autorange() 
        main_layout.addLayout(graph_controls_layout)
        
        # --- Button Layout ---
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start Acquisition")
        self.start_button.clicked.connect(self.start_acquisition)
        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.toggle_pause)
        self.pause_button.setEnabled(False) 
        self.stop_button = QPushButton("Stop Acquisition")
        self.stop_button.clicked.connect(self.stop_acquisition) # <-- This line caused the error
        self.stop_button.setEnabled(False)
        self.clear_button = QPushButton("Clear Plot")
        self.clear_button.clicked.connect(self.clear_plot)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addStretch() 
        button_layout.addWidget(self.clear_button)
        main_layout.addLayout(button_layout)
        
        self.start_acquisition()

    def start_acquisition(self):
        # ... (Thread creation is the same) ...
        self.acquisition_thread = QThread()
        self.acquisition_worker = AcquisitionWorker(
            self.config["instrument_class"], 
            self.config
        )
        self.acquisition_worker.moveToThread(self.acquisition_thread)
        self.acquisition_thread.started.connect(self.acquisition_worker.run_acquisition)
        self.acquisition_worker.data_ready.connect(self.update_raw_plot)
        self.acquisition_worker.processed_data_ready.connect(self.update_filtered_plot)
        self.acquisition_worker.finished.connect(self.on_acquisition_finished)
        self.acquisition_worker.error.connect(self.on_acquisition_error)

        self.acquisition_thread.start()
        
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.pause_button.setEnabled(True)
        self.pause_button.setText("Pause")
        self.status_label.setText("Acquisition running...")
        
        self.event_entry_box.setEnabled(True)
        self.add_event_button.setEnabled(True)
        
        self.autorange_check.setChecked(True)
        
    # --- THIS METHOD WAS MISSING ---
    def stop_acquisition(self):
        if self.acquisition_worker:
            self.acquisition_worker.stop()
        
        self.stop_button.setEnabled(False)
        self.pause_button.setEnabled(False)
    # --- END ---

    def on_acquisition_finished(self):
        if self.acquisition_thread:
            self.acquisition_thread.quit()
            self.acquisition_thread.wait()
        
        self.acquisition_thread = None
        self.acquisition_worker = None
        
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.pause_button.setEnabled(False)
        self.pause_button.setText("Pause")
        self.status_label.setText("Acquisition Stopped. Ready to start again.")
        
        self.event_entry_box.setEnabled(False)
        self.add_event_button.setEnabled(False)
        
    def on_acquisition_error(self, err_msg):
        self.status_label.setText(f"ERROR: {err_msg}")
        self.on_acquisition_finished() 

    def update_raw_plot(self, voltage):
        self.raw_data_buffer = np.roll(self.raw_data_buffer, -1)
        self.raw_data_buffer[-1] = voltage
        self.raw_plot_curve.setData(self.raw_data_buffer)

    def update_filtered_plot(self, voltage):
        self.filtered_data_buffer = np.roll(self.filtered_data_buffer, -1)
        self.filtered_data_buffer[-1] = voltage
        self.filtered_plot_curve.setData(self.filtered_data_buffer)

    def closeEvent(self, event):
        self.stop_acquisition()
        if self.acquisition_thread:
            self.acquisition_thread.wait()
        event.accept()

    def toggle_pause(self):
        if not self.acquisition_worker:
            return

        if self.pause_button.text() == "Pause":
            self.acquisition_worker.pause()
            self.pause_button.setText("Resume")
            self.status_label.setText("Acquisition paused...")
        else:
            self.acquisition_worker.resume()
            self.pause_button.setText("Pause")
            self.status_label.setText("Acquisition running...")

    def clear_plot(self):
        print("Clearing plot buffers.")
        self.raw_data_buffer.fill(0)
        self.filtered_data_buffer.fill(0)
        self.raw_plot_curve.setData(self.raw_data_buffer)
        self.filtered_plot_curve.setData(self.filtered_data_buffer)

    def log_event(self):
        comment = self.event_entry_box.text()
        if not comment or not self.acquisition_worker:
            return 
            
        self.acquisition_worker.add_event_comment(comment)
        
        self.event_entry_box.clear()
        self.status_label.setText(f"Logged event: {comment}")

    def toggle_autorange(self):
        is_checked = self.autorange_check.isChecked()
        self.plot_widget.enableAutoRange(y=is_checked)
        
        self.ymin_spin.setEnabled(not is_checked)
        self.ymax_spin.setEnabled(not is_checked)
        
        if not is_checked:
            self.apply_manual_range()
            
    def apply_manual_range(self):
        if not self.autorange_check.isChecked():
            ymin = self.ymin_spin.value()
            ymax = self.ymax_spin.value()
            self.plot_widget.setYRange(ymin, ymax)