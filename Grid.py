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
        for i in range(0, self.height, 20):
            for j in range(0, self.width):
                self.grid[i][j] = 1

        for i in range(0, self.width, 20):
            for j in range(0, self.height):
                self.grid[j][i] = 1

        for j in range(0,self.width):
            self.grid[self.height-1][j]=1

        for j in range(0,self.height):
            self.grid[j][self.width-1]=1
    
    def build_obstacles(self,blocked):
        allOne=[]
        for i in range(0, self.height,20):
            for j in range(0, self.width):
                allOne.append([i,j])            

        for i in range(0, self.width,20):
            for j in range(0, self.height):
                allOne.append([j,i])

        k=0
        count=0
        while k+3 <len(blocked):
            p = path.Path([blocked[k], blocked[k+1], blocked[k+2], blocked[k+3]])
            flags = p.contains_points(allOne)
            # print(flags)
            for i in range(len(flags)):
                if flags[i]==True:
                    count+=1      

            kite=-1
            for i in range(0, self.height,20):
                for j in range(0, self.width):
                    kite=kite+1
                    if flags[kite]==True:
                        self.grid[i][j]=2    

            for i in range(0, self.width,20):
                for j in range(0, self.height):
                    kite=kite+1
                    if flags[kite]==True:
                        self.grid[j][i]=2
            print(count)           
            k+=4
        # for i in range(0, self.height):
        #     for j in range(0, self.width):
        #         if self.grid[i][j]==1:
        #             print("#",end="")
        #         else:
        #             print(" ",end="")
        #     print(" ")        

        
        # for i in range(0, self.height):
        #     for j in range(0, self.width):
        #         print(self.grid[i][j],end=" ")
        #     print(" ")
                
    
