import pygame
from Agent007 import Agent
from Grid import Grid
import AStar
from AStar import Search,Matrix
import colors

import time
# n,m=input().split()   Take input from User
n = 5   # height
m = 5   # width

display_height = 120*m+160
display_width = 120*n+160
racks_height = 120*m+160
racks_width = 120*n+160

numofrack={}
def num_racks(n,m):
    for i in range(n):
        for j in range(m):
            for l in range(5):
                numofrack[str((i,j,0,l))]=(120*i+90,120*j+105+20*l)
                numofrack[str((i,j,1,l))]=(25+numofrack[str((i,j,0,0))][0],l*20+numofrack[str((i,j,0,0))][1])
                for k in range(2,5):
                    numofrack[str((i,j,k,l))]=((k-1)*20+numofrack[str((i,j,1,0))][0],numofrack[str((i,j,1,l))][1])

num_racks(n,m)
print(numofrack[str((0,0,1,1))])



pygame.display.set_caption("Amazon Warehouse")


def waste3(x, y, dir):
    if x:
        add_edge((x, 80), (x, racks_width-70),dir)
    elif y:
        add_edge((80, y), (racks_height-70, y),dir)




#Applying A Star Here



def waste1(n,m):
    y = 100
    for ro in range(0, n):
        x = 100
        for cols in range(0, m):
            marking_line(x, y)
            x += 120
        y += 120

def waste2(n, m):
    x = 80
    for i in range(m+1):
        waste3(x,0,direction["up"])
        waste3(x+10, 0, direction["down"])  # down
        x += 120
    y = 80
    for i in range(n+1):
        waste3(0, y, direction["right"])  # right
        waste3(0, y+10, direction["left"])  # left
        y += 120



direction = {}
direction["up"] = 1
direction["down"] = 2
direction["right"] = 3
direction["left"] = 4


#  Grid[x][y]=empty list ho

def add_edge(X, Y, dir):
    if X[0] == Y[0]:
        for i in range(X[1], Y[1]+1, 1):
            Matrix.grid[X[0]][i].append(dir)
    else:
        for i in range(X[0], Y[0]+1, 1):
            Matrix.grid[i][X[1]].append(dir)



def marking_line(x,y):
    add_edge((x+15,y-10),(x+15,y+100),direction["up"])
    add_edge((x+55,y-10),(x+55,y+100),direction["up"])
    add_edge((x+35,y-10),(x+35,y+100),direction["down"])
    add_edge((x+75,y-10),(x+75,y+100),direction["down"])
    add_edge((x-10,y+15),(x+100,y+15),direction["right"])
    add_edge((x-10,y+55),(x+100,y+55),direction["right"])
    add_edge((x-10,y+35),(x+100,y+35),direction["left"])
    add_edge((x-10,y+75),(x+100,y+75),direction["left"])


j = 0
flag = 0
waste1(n, m)
waste2(n,m)

# for i in range(n):
#     for j in range(
# sources