import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

class Plotter():
    def __init__(self, driver, fps, circuit, speeds):
        self.driver = driver
        self.time = 1 / fps
        self.circuit = circuit
        self.speeds = np.array(speeds)

    def plot(self):
                
