# Main window
- plots the data in real time
- suitable graph controls
- allows comments
- allows pausing/resuming
- allows stopping
- configure an event loop.  Some kind of scriptable thing?

# Source configuration
- Dialog that allows different instruments to be configured and selected.
- Intialize instrument
  - Could select file that holds configuration
  - File could be just a command string to send to instrument

# When starting a new measurement:
- Configure sources or chose an old configuration
- Ask for comments:
  - Details of measurement
  - Who is present

# What to try to do at first?
- Main goal is to build an "instrument" that generates random numbers
- Allow this data to be plotted and recorded
- Dialog that asks:
  - Use an existing configuration?
  - Build a new configuration?
    - List of available instruments
    - Pick and add to list.
    - allow giving a nickname and setting other options
