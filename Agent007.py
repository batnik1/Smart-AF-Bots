import math
import pygame
class Agent():

    def __init__(self, Destination, Target):
        self.playerX = Destination[0]
        self.playerY = Destination[1]
        self.goalX = Target[0]
        self.goalY = Target[1]

  
    def move(self, Target):
        self.playerX=Target[0]
        self.playerY=Target[1]
        

  