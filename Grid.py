from matplotlib import pyplot as plt
import numpy as np
from matplotlib import path

class Grid():

    def __init__(self, width, height):
        self.width = width
        self.height = height
        rows, cols = (height, width)
        self.grid = [[0 for i in range(cols)] for j in range(rows)]

    def build_roads(self):
        pass




        # for i in range(0, self.height, 20):
        #     for j in range(0, self.width):
        #         self.grid[i][j] = 1

        # for i in range(0, self.width, 20):
        #     for j in range(0, self.height):
        #         self.grid[j][i] = 1

        # for j in range(0,self.width):
        #     self.grid[self.height-1][j]=1

        # for j in range(0,self.height):
        #     self.grid[j][self.width-1]=1
    