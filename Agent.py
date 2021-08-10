import math
import pygame
class Agent():

    def __init__(self, Destination, Target, Agent_Image, Target_Image):
        self.playerX = Destination[0]
        self.playerY = Destination[1]
        self.goalX = Target[0]
        self.goalY = Target[1]
        self.wait=0
        self.player_image = pygame.image.load(Agent_Image)
        self.target_image = pygame.image.load(Target_Image)
        self.transformed_image = pygame.image.load(Agent_Image)
        self.angle = 90

    def rotate(self, angle):
        self.angle = (self.angle + angle + 360) % 360
        self.transformed_image = pygame.transform.rotate(self.player_image, (self.angle - 90))

    def rotateto(self, angle):
        running = True
        clockwise = True
        if self.angle==angle:
            return
        if (self.angle > angle):
            if (self.angle - angle < 360 - self.angle + angle):
                clockwise = True
            else:
                clockwise = False
        elif (self.angle < angle):
            if (angle - self.angle < 360 - angle + self.angle):
                clockwise = False
            else:
                clockwise = True

        if (clockwise):
            self.rotate(-2)
        else:
            self.rotate(2)

    def change(self, length):
        self.playerX += length * math.cos(math.radians(self.angle))
        self.playerY += (-1)*length * math.sin(math.radians(self.angle))

    def move(self, angle, length):
        self.rotate(angle)
        self.change(length)

    def small_movement(self, Destination, Target, angle):
        self.move(angle,abs(Destination[0]-Target[0])+abs(Destination[1]-Target[1]))

    def big_movement(self, Destination, Target):
        posX1 = Destination[0]
        posY1 = Destination[1]
        posX2 = Target[0]
        posY2 = Target[1]
        if posX1 == posX2:
            if posY1 < posY2:
                self.rotateto(270)
                if self.angle==270:
                    self.playerX=Target[0]
                    self.playerY=Target[1]
                    self.wait=0
                    #self.small_movement(Destination, Target, 0)
                else:
                    self.wait=1
            else:
                self.rotateto(90)
                if self.angle==90:
                    self.playerX=Target[0]
                    self.playerY=Target[1]
                    self.wait=0
                    #self.small_movement(Destination, Target, 0)
                else:
                    self.wait=1
        elif posY1 == posY2:
            if posX1 > posX2:
                self.rotateto(180)
                if self.angle==180:
                    self.playerX=Target[0]
                    self.playerY=Target[1]
                    self.wait=0
                    #self.small_movement(Destination, Target, 0)
                else:
                    self.wait=1
            else:
                self.rotateto(0)
                if self.angle==0:
                    self.playerX=Target[0]
                    self.playerY=Target[1]
                    self.wait=0
                    #self.small_movement(Destination, Target, 0)
                else:
                    self.wait=1
    def collision(self):
        pass
