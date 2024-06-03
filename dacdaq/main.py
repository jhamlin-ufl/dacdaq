from PyQt6 import QtWidgets, uic
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import numpy as np
import sys


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Load the UI Page
        uic.loadUi("./ui/mainwindow.ui", self)

        x = np.random.random(10)
        y = np.random.random(10)
        self.mainPlot.plot(x, y)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
