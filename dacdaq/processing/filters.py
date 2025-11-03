import numpy as np

class MovingAverageFilter:
    """
    A simple moving average filter.
    """
    def __init__(self, window_size=5):
        self.window_size = int(window_size)
        if self.window_size < 1:
            self.window_size = 1
        # Create a buffer for the window
        self.buffer = np.zeros(self.window_size)
        self.pointer = 0 # To track where in the buffer we are
    
    def process(self, new_value):
        """
        Adds a new value to the filter and returns the new average.
        """
        # Add the new value to the buffer
        self.buffer[self.pointer] = new_value
        
        # Increment the pointer, wrapping around if necessary
        self.pointer = (self.pointer + 1) % self.window_size
        
        # Calculate and return the mean of the buffer
        return np.mean(self.buffer)