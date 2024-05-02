import sys
import pyqtgraph as pg
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from mainwindow import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

'''
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
'''
