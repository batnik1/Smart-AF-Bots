from matplotlib import pyplot as plt
import numpy as np
from matplotlib import path
# grid class for making our roadmap
class Grid():

    def __init__(self, width, height):
        self.width = width
        self.height = height
        rows, cols = (height, width)
        self.grid = [[[0] for i in range(cols)] for j in range(rows)]
