#!/usr/bin/env python
"""
A demonstration of plotting a file that is being
concurrently updated.
"""

import pyqtgraph as pg
from PyQt6 import QtWidgets
import fcntl
import time
import os
from pathlib import Path


def make_plot():
    class MainWindow(QtWidgets.QMainWindow):
        def __init__(self):
            super().__init__()

            # Temperature vs time plot
            self.plot_graph = pg.PlotWidget()
            self.setCentralWidget(self.plot_graph)
            minutes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 30]
            self.plot_graph.plot(minutes, temperature)

    app = QtWidgets.QApplication([])
    main = MainWindow()
    main.show()
    app.exec()


def main():
    file_path = "./temporary_data_file.dat"
    if not Path(file_path).exists():
        print("File does not exist!")
        return 0
    else:
        make_plot()
        return 1


if __name__ == "__main__":
    main()
