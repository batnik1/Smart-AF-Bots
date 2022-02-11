from cProfile import run
import pygame
import numpy as np
from collections import deque


class Vehicle:
    def __init__(self):  
        self.l = 4
        self.s0 = 10
        self.T = 0.5
        self.v_max = 7
        self.a_max = 3.44
        self.b_max = 4.61

        self.path = []
        self.current_road_index = 0

        self.x = 0
        self.v = self.v_max
        self.a = 0
        self.stopped = False

    def init_properties(self):
        self.sqrt_ab = 2*np.sqrt(self.a_max*self.b_max)
        self._v_max = self.v_max

    def update(self, lead, dt):
        # Update position and velocity
        if self.v + self.a*dt < 0:
            self.x -= 1/2*self.v*self.v/self.a
            self.v = 0
        else:
            self.v += self.a*dt
            self.x += self.v*dt + self.a*dt*dt/2
        
        # Update acceleration
        alpha = 0
        if lead:
            delta_x = lead.x - self.x - lead.l
            delta_v = self.v - lead.v

            alpha = (self.s0 + max(0, self.T*self.v + delta_v*self.v/self.sqrt_ab)) / delta_x

        self.a = self.a_max * (1-(self.v/self.v_max)**4 - alpha**2)

        if self.stopped: 
            self.a = -self.b_max*self.v/self.v_max
        
        
    def stop(self):
        self.stopped = True

    def unstop(self):
        self.stopped = False

    def slow(self, v):
        self.v_max = v

    def unslow(self):
        self.v_max = self._v_max



# start pygame with white screen
pygame.init()
screen=pygame.display.set_mode((800,600))

# Create 2 vehicle
V1 =[Vehicle(), Vehicle()]
# for i in range(15):
#     V1.append()
z=0
V1[0].x=z
z-=1
V1[1].x=z
z-=1
n=0
V3=[Vehicle(), Vehicle()]
V3[0].x=n
n-=1
V3[1].x=n
n-=1
xpp=Vehicle()
xpp.x=400
ypp=Vehicle()
ypp.x=300
V2=[]
V4=[]
Intersection=(400,300)
running=True
booking=False
key=0
while running:
    #print(booking)
    key+=1
    # if key%5000==0:
    #     booking=4-booking
    
    if key%100==0 and key<10000:
        V1=[Vehicle()]+V1
        V1[0].x=z
        z-=1
        V3=[Vehicle()]+V3
        V3[0].x=n
        n-=1

    screen.fill((255,255,255))
    # create two prependicular lines passing through the center of the screen
    pygame.draw.line(screen,(255,0,0),(400,0),(400,600),2)
    pygame.draw.line(screen,(0,255,0),(0,300),(800,300),2)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    for v in V1:
        pygame.draw.circle(screen, (255,0,0), (int(v.x), int(300)), 5)
    for v in V2:
        pygame.draw.circle(screen, (255,0,0), (int(v.x), int(300)), 5)
    
    p=[]
    for i in range(len(V1)):
        # update
        try1=V1[i].x
        if i+1 < len(V1):
            V1[i].update(V1[i+1], 1/60)
        else:
            if booking==3:
                V1[i].update(xpp, 1/60)
            elif 400-V1[i].x<50:
                booking=1
                V1[i].update(None, 1/60)
            else:
                V1[i].update(None, 1/60)
        if V1[i].x >= Intersection[0]:
            V2.append(V1[i])
            p.append(i)
            booking=False
        try2=V1[i].x
        if try1>try2:
            print("WTF this is wrong on many levels",try1,try2)
  
    for i in range(len(V2)):
            # if V2[i].x >= 700:
            #    V2[i].stop()
        # update
        if i+1 < len(V2):
            V2[i].update(V2[i+1], 1/60)
        else:
            V2[i].update(None, 1/60)
    
    if p:
        for i in p:
            V1.pop(i)
        p=[]

    for v in V3:
        pygame.draw.circle(screen, (255,0,0), (int(400), int(v.x)), 5)
    for v in V4:
        pygame.draw.circle(screen, (255,0,0), (int(400), int(v.x)), 5)
    
    p=[]
    for i in range(len(V3)):
        # update
        if i+1 < len(V3):
            V3[i].update(V3[i+1], 1/60)
        else:
            if booking==1:
                V3[i].update(ypp, 1/60)
            elif 300-V3[i].x<50:
                booking=3
                V3[i].update(None, 1/60)
            else:
                V3[i].update(None, 1/60)
        if V3[i].x>=Intersection[1]:
            V4.append(V3[i])
            p.append(i)
            booking=False

   # print(booking)
    for i in range(len(V4)):
        # if V4[i].x <= 100:
        #    V4[i].stop()
        # update
        if i+1 < len(V4):
            V4[i].update(V4[i+1], 1/60)
        else:
            V4[i].update(None, 1/60)
    
    if p:
        for i in p:
            V3.pop(i)
        p=[]
            
 
    pygame.display.flip()