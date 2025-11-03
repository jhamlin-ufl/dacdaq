<div align="center">

<h1>⚡️ DacDAQ ⚡️</h1>

<p><b>A robust, high-performance, and scalable Python system for real-time data acquisition, processing, and visualization.</b></p>

<p>Built to replace legacy lab software, DacDAQ offers a modern, maintainable, and version-controllable solution for scientific research.</p>

<p>
  <a href="https://github.com/GodlyDonuts/dacdaq/actions">
    <img alt="Build Status" src="https://img.shields.io/github/actions/workflow/status/GodlyDonuts/dacdaq/ci.yml?branch=main&style=for-the-badge">
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge">
  </a>
  <a href="https://github.com/GodlyDonuts/dacdaq/releases">
    <img alt="Latest Release" src="https://img.shields.io/github/v/release/GodlyDonuts/dacdaq?style=for-the-badge">
  </a>
  <a href="https://github.com/GodlyDonuts/dacdaq/issues">
    <img alt="Open Issues" src="https://img.shields.io/github/issues/GodlyDonuts/dacdaq?style=for-the-badge">
  </a>
</p>

</div>

-----

## ✨ Features

DacDAQ is a complete toolkit for interfacing with lab hardware, built on a modern Python stack (`PyQt6`, `pyqtgraph`, and `Poetry`).

  - ⚡ **Non-Blocking, Threaded Architecture:** The core acquisition loop runs in a dedicated `QThread`, ensuring the GUI remains perfectly responsive, even with slow instruments.
  - 🧩 **Modular Instrument Plugins:** Easily add new hardware by creating a simple `BaseInstrument` plugin. Comes with a `SimulatedInstrument` for testing and a `Keithley2000` class for real-world use.
  - 💾 **Save & Load Configurations:** Don't re-enter settings. Save your entire setup (instrument choice, output file, comments) to a JSON file and load it instantly.
  - 📈 **High-Performance Real-Time Plotting:** Uses `pyqtgraph` to plot multiple data streams live.
  - 🔬 **Live Data Processing:** Apply real-time filters (like the built-in `MovingAverageFilter`) and plot both raw and processed data simultaneously.
  - ⏯️ **Full Run Control:** **Start**, **Stop**, **Pause**, and **Resume** your acquisition at any time.
  - 📝 **Live Event Logging:** Add timestamped comments (e.g., "Increased pressure to 10 GPa") during a run *without* stopping acquisition. Events are saved to a separate `.events.csv` file.
  - 📊 **Flexible Graph Controls:** Toggle Y-axis auto-ranging and manually set Y-min/max limits to focus on your data.
  - 📂 **Dual-File Data Sinks:** Automatically saves all data to two files: a `.csv` for raw and filtered data, and a `.events.csv` for your comments.

-----

## 🚀 Getting Started

Get your local copy up and running in a few simple steps.

### Prerequisites

  - `Python 3.10+`
  - `Poetry` (for package management)
  - A backend for `pyvisa` (if using real hardware), e.g., `NI-VISA`

### Installation & Running

```bash
# 1. Clone the repository
git clone https://github.com/jhamlin-ufl/dacdaq.git
cd dacdaq

# 2. Install dependencies with Poetry
# This creates a virtual environment and installs all packages
poetry install

# 3. Run the application
poetry run python run_app.py
```

### How to Use

1.  The **Configure** dialog will appear.
2.  Click **"Load Config..."** to load a previous setup, or...
3.  Select your instrument (e.g., "Keithley 2000").
4.  Click **"Browse..."** to choose an output CSV file.
5.  Add pre-run comments.
6.  Click **"Save Config..."** to save this setup for next time.
7.  Click **"OK"** to start the main application.

-----

## 🌲 Project Structure

The project is organized into a modular package, making it easy to extend.

```
dacdaq/
├── dacdaq/
│   ├── __init__.py
│   ├── core/
│   │   └── worker.py         # The main AcquisitionWorker (runs on a QThread)
│   ├── inputs/
│   │   ├── base.py           # BaseInstrument class
│   │   ├── simulated.py      # Simulated (random data) instrument
│   │   └── keithley2000.py   # Real Keithley 2000 instrument
│   ├── outputs/
│   │   ├── csv_sink.py       # Saves data (raw, filtered) to .csv
│   │   └── event_sink.py     # Saves user comments to .events.csv
│   ├── processing/
│   │   └── filters.py        # Contains MovingAverageFilter
│   └── ui/
│       ├── config_dialog.py  # The startup configuration window
│       └── main_window.py    # The main plot/control window
├── .gitignore
├── LICENSE
├── README.md         # You are here!
├── poetry.lock       # Defines exact dependency versions
├── pyproject.toml    # Defines all project dependencies
└── run_app.py        # The main entry point to run the program
```

-----

## 📜 License

Distributed under the **MIT License**. See `LICENSE` file for more information.

-----

## ✉️ Contact

@GodlyDonuts

**Project Link:** [https://github.com/GodlyDonuts/dacdaq](https://github.com/GodlyDonuts/dacdaq)
