import json # <-- 1. IMPORT JSON
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox,
    QDialogButtonBox, QFileDialog, QTextEdit, QPushButton, QHBoxLayout
)
from dacdaq.inputs.simulated import SimulatedInstrument
from dacdaq.inputs.keithley2000 import Keithley2000

AVAILABLE_INSTRUMENTS = {
    SimulatedInstrument().get_name(): SimulatedInstrument,
    Keithley2000().get_name(): Keithley2000,
}
# Create a reverse map for loading
INSTRUMENT_CLASS_TO_NAME = {v: k for k, v in AVAILABLE_INSTRUMENTS.items()}


class ConfigDialog(QDialog):
    """
    A dialog to configure the acquisition.
    Now supports saving and loading configurations.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configure New Acquisition")
        self.setMinimumWidth(400)
        
        self.config = {}

        layout = QVBoxLayout(self)
        
        # --- 2. NEW: Save/Load Buttons ---
        config_file_layout = QHBoxLayout()
        self.load_config_button = QPushButton("Load Config...")
        self.load_config_button.clicked.connect(self.load_configuration)
        
        self.save_config_button = QPushButton("Save Config...")
        self.save_config_button.clicked.connect(self.save_configuration)
        
        config_file_layout.addWidget(self.load_config_button)
        config_file_layout.addWidget(self.save_config_button)
        layout.addLayout(config_file_layout)
        # --- END NEW ---

        # --- Form Layout (unchanged) ---
        form_layout = QFormLayout()

        self.instrument_combo = QComboBox()
        self.instrument_combo.addItems(AVAILABLE_INSTRUMENTS.keys())
        form_layout.addRow("Instrument:", self.instrument_combo)

        self.file_path_edit = QLineEdit()
        self.file_path_edit.setReadOnly(True)
        self.browse_button = QPushButton("Browse...")
        self.browse_button.clicked.connect(self.select_output_file)
        
        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_path_edit)
        file_layout.addWidget(self.browse_button)
        form_layout.addRow("Output File (CSV):", file_layout)
        
        self.comments_edit = QTextEdit()
        self.comments_edit.setPlaceholderText("Enter details: setup, who is present, goals...")
        form_layout.addRow("Comments:", self.comments_edit)
        
        layout.addLayout(form_layout)
        
        # --- OK / Cancel Buttons (unchanged) ---
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        
        self.ok_button = self.button_box.button(QDialogButtonBox.StandardButton.Ok)
        self.ok_button.setEnabled(False) 
        
        layout.addWidget(self.button_box)

    def select_output_file(self):
        # ... (unchanged)
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Output File", "", "CSV Files (*.csv)")
        if file_name:
            self.file_path_edit.setText(file_name)
            self.ok_button.setEnabled(True)

    def accept(self):
        # ... (unchanged)
        instrument_name = self.instrument_combo.currentText()
        self.config = {
            "instrument_name": instrument_name,
            "instrument_class": AVAILABLE_INSTRUMENTS[instrument_name],
            "output_file": self.file_path_edit.text(),
            "comments": self.comments_edit.toPlainText()
        }
        super().accept()

    def get_config(self):
        # ... (unchanged)
        return self.config

    # --- 3. NEW: Save/Load Methods ---
    def load_configuration(self):
        """Loads configuration from a .json file."""
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Load Configuration", "", "JSON Files (*.json)"
        )
        if not file_name:
            return
            
        try:
            with open(file_name, 'r') as f:
                config_data = json.load(f)
            
            # Populate the dialog fields
            self.instrument_combo.setCurrentText(config_data.get("instrument_name", ""))
            self.file_path_edit.setText(config_data.get("output_file", ""))
            self.comments_edit.setPlainText(config_data.get("comments", ""))
            
            # Enable OK button if a file path was loaded
            if self.file_path_edit.text():
                self.ok_button.setEnabled(True)
                
            print(f"Configuration loaded from {file_name}")
            
        except Exception as e:
            print(f"Error loading configuration: {e}")
            # You could show a QMessageBox here
            
    def save_configuration(self):
        """Saves the current dialog settings to a .json file."""
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Configuration", "", "JSON Files (*.json)"
        )
        if not file_name:
            return

        # Create config data from current fields
        config_data = {
            "instrument_name": self.instrument_combo.currentText(),
            "output_file": self.file_path_edit.text(),
            "comments": self.comments_edit.toPlainText(),
        }
        
        try:
            with open(file_name, 'w') as f:
                json.dump(config_data, f, indent=4)
            print(f"Configuration saved to {file_name}")
        except Exception as e:
            print(f"Error saving configuration: {e}")
            # You could show a QMessageBox here