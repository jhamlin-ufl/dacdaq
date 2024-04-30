import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = uic.loadUi("ui/dacdaq.ui")
    window.show()

    app.exec()
