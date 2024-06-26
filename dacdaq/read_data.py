#!/usr/bin/env python
"""
A demonstration of plotting a file that is being
concurrently updated.
"""

import fcntl
from pathlib import Path
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer
import pyqtgraph as pg
import pandas as pd


def read_file_with_lock(file_path):
    with open(file_path, "r") as file:
        # Acquire a shared lock on the file (read lock)
        fcntl.flock(file.fileno(), fcntl.LOCK_SH)

        try:
            # Read the file content
            df = pd.read_csv(file)
        finally:
            # Release the lock
            fcntl.flock(file.fileno(), fcntl.LOCK_UN)

    return df


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a plot widget
        self.plot_widget = pg.PlotWidget()

        # Set the central widget of the window
        self.setCentralWidget(self.plot_widget)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(100)

        self.update_plot()

    def update_plot(self):
        df = read_file_with_lock("./temporary_data_file.dat")
        self.plot_widget.plot(df.x, df.y)


def make_plot():
    app = QApplication(sys.argv)

    # Create an instance of the main window
    window = MainWindow()
    window.show()

    # Start the Qt event loop
    sys.exit(app.exec())


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
