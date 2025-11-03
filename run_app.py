import sys
from PyQt6.QtWidgets import QApplication, QDialog
from dacdaq.ui.config_dialog import ConfigDialog
from dacdaq.ui.main_window import DacDaqWindow

def main():
    """
    The main entry point for the DacDAQ application.
    """
    app = QApplication(sys.argv)
    
    # 1. Show config dialog first
    config_dialog = ConfigDialog()
    
    if config_dialog.exec() == QDialog.DialogCode.Accepted:
        config = config_dialog.get_config()
        
        # 2. If OK, get config and show main window
        window = DacDaqWindow(config)
        window.show()
        sys.exit(app.exec())
    else:
        # 3. If Cancel, exit the application
        print("Startup cancelled.")
        sys.exit(0)

if __name__ == "__main__":
    main()