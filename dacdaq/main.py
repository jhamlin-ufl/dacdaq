import sys
import pyqtgraph as pg
import numpy as np
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget

if __name__ == "__main__":
    x = np.random.random(10)
    y = np.random.random(10)

    app = QApplication(sys.argv)

    window = uic.loadUi("ui/dacdaq.ui")

    plotWidget = pg.PlotWidget()

    # Set the title of the plot
    plotWidget.setWindowTitle("PyQtGraph Example")

    # Add a curve to the plot
    plotWidget.plot(x, y)

    # Show the plot
    plotWidget.show()

    window.show()

    app.exec()
