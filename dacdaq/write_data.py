#!/usr/bin/env python
"""
A demonstration of writing to a file using a file lock.
Writes out a sin wave.
"""

import numpy as np
import itertools
import fcntl
import time
import os
from pathlib import Path


def main():
    file_path = "./temporary_data_file.dat"
    if Path(file_path).exists():
        os.remove(file_path)

    with open(file_path, "a") as file:
        fcntl.flock(file.fileno(), fcntl.LOCK_EX)
        file.write("#time(s),x,y\n")
        fcntl.flock(file.fileno(), fcntl.LOCK_UN)

    mycount = itertools.count()

    t0 = time.time()

    while True:
        t = time.time() - t0
        x = 2 * np.pi * mycount.__next__() / 100
        y = np.sin(x)

        with open(file_path, "a") as file:
            fcntl.flock(file.fileno(), fcntl.LOCK_EX)
            file.write(f"{t},{x},{y}\n")
            fcntl.flock(file.fileno(), fcntl.LOCK_UN)

        time.sleep(0.1)


if __name__ == "__main__":
    main()
