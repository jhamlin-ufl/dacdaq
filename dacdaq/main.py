from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QTimer
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import numpy as np
import sys


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Load the UI Page
        uic.loadUi("./ui/mainwindow.ui", self)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_label)
        self.timer.start(1)  # Update every 1000 milliseconds (1 second)

    def update_label(self):
        x = np.random.random(10)
        y = np.random.random(10)
        self.mainPlot.clear()
        self.mainPlot.plot(x, y)  # Setup timer


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
