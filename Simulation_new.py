import random
import time
import math
import pygame
from Agent import Agent
from Grid import Grid
import trialastar
from Make_map import matrix,buffer
#import Make_map
pygame.init()

screen = pygame.display.set_mode((1600, 1600))  # create screen
running = True
### Title and Icon
pygame.display.set_caption("Waah Bete")

#Ou
target = pygame.image.load("dart.png")
Number_of_Agents=0
Agents=[]
Index=[]
Path=[]
def add_agent(source,dest):
    Agents.append(Agent(source,dest,"robot-vacuum-cleaner.png","dart.png"))
    Index.append(0)
    cAgent=trialastar.A_Star_Solver(source,dest)
    cAgent.Solve()
    #print(cAgent.cost)
    Path.append(cAgent.path)
    global Number_of_Agents
    Number_of_Agents+=1


add_agent([200,200],[800,800])
add_agent([400,400],[600,600])
add_agent([600,600],[400,400])
add_agent([800,800],[200,200])

# for i in range(0,matrix.height):
#     for j in range(0,matrix.width):
#         if matrix.grid[i][j]==2:
#             print(i,j)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break        
    screen.fill((255, 255, 255))
    
    for i in range(Number_of_Agents):
        screen.blit(Agents[i].transformed_image,(Agents[i].playerX,Agents[i].playerY))
        screen.blit(Agents[i].target_image,(Agents[i].goalX,Agents[i].goalY))
        if Index[i]+1<len(Path[i]):
            Agents[i].big_movement(Path[i][Index[i]],Path[i][Index[i]+1])
            if Agents[i].wait==0:
                Index[i]+=1
    
    i=0
    while i+3<len(buffer):
        #print(buffer[i],buffer[i+1],buffer[i+2],buffer[i+3])
        points = [buffer[i], buffer[i+1],buffer[i+2],buffer[i+3]]
        pygame.draw.polygon(screen, (255,0,0), points)
        i+=4

    #pygame.draw.rect(screen, (255,0,0), pygame.Rect(700, 210, 5, 690))
    #pygame.draw.rect(screen, (255,0,0), pygame.Rect(650, 199, 150, 5))
    #pygame.draw.rect(screen, (255,0,0), pygame.Rect(400, 175, 5, 200))
    pygame.display.update()



