import pygame
from Agent007 import Agent
from Grid import Grid
import AStar
from AStar import Search,Matrix
import colors

import time
# n,m=input().split()   Take input from User
m = 4 # width
n = 4  # height     (n,m)>=3
sorting_m=6
sorting_n=4

print("reached map_simul")


display_width = 120*m+800
display_height = 120*n+300
racks_height = 120*n+160
racks_width = 120*m+160

rack_available={}
def rack_available_fn():
    for i in range(n):
        for j in range(m):
            for k in range(5):
                for l in range(5):
                    rack_available[str((i,j,k,l))]=1

rack_available_fn()
#print(rack_availaible[str((3,1,1,1))])


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
#print(numofrack[str((0,0,1,1))])
#y=100
numofdump={}
def numofdumping():
    x=racks_width+20
    for i in range(2*sorting_m):
        y=80
        for j in range(2*sorting_n):
            numofdump[str((j,i))]=(x-10,y+10)
            y+=30
        x+=30

numofdumping()
numofdump["conveyor"]=(racks_width,(80+racks_height//2)//2+20)


numofhcounter={}
def num_hcounter(n,m):
    for i in range(2):
        for j in range(m):
            numofhcounter[str((i,j))]=(90+120*j+i*(80), i*(120*(n+1)-40)+45)
num_hcounter(n,m)
pygame.display.set_caption("Warehouse Simulation V1.0")

def waste3(x, y, dir):
    if x:
        add_edge((x, 80), (x, racks_height-70),dir)
    elif y:
        add_edge((80, y), (racks_width-70, y),dir)


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

def marking_queue_line(n,m):
    x=90
    for i in range(m):
        add_edge((x, 10), (x, 80),direction["down"])
        add_edge((x+80,10),(x+80,80),direction["up"])
        add_edge((x, 10), (x+80,10),direction["left"])
        x+=120
    x=90
    for i in range(m):
        add_edge((x, 120*(n+1)-30), (x, 40+120*(n+1)),direction["down"])
        add_edge((x+80, 120*(n+1)-30), (x+80, 40+120*(n+1)),direction["up"])
        add_edge((x, 40+120*(n+1)), (x+80,40+120*(n+1)),direction["right"])
        x+=120

def marking_station_line(n,m):
    add_edge((80, 80), (30, 80),direction["left"])
    add_edge((80, (n//2+n%2)*100), ((30, (n//2+n%2)*100)),direction["right"])
    add_edge((30, (n//2+n%2)*100), ((30, 80)),direction["down"])
    pass


def waste_conveyor_belt():
    add_edge((130, 0), (racks_width, 0),direction["right"])
    add_edge((130, racks_height+10), (racks_width, racks_height+10),direction["right"])
    add_edge((racks_width, 0),(racks_width,(80+racks_height//2)//2+20),direction["down"])
    add_edge((racks_width,(80+racks_height//2)//2+20), (racks_width, racks_height+10),direction["up"])
    x=130
    for _ in range(m):
        add_edge((x,1),(x,15),direction["up"])
        add_edge((x, racks_height-5), (x,racks_height+9),direction["down"])
        x+=120

def waste_charging():
    
    for i in range((n//2+n % 2)*100+20,racks_height-90,10):
        add_edge((30,i),(80,i),direction["right"])

    add_edge((30, (n//2+n % 2)*100+10), (80, (n//2+n % 2)*100+10),direction["left"])
    add_edge((30, racks_height-90), (80, racks_height-90),direction["right"])
    add_edge((30, (n//2+n % 2)*100+10), (30, racks_height-90),direction["down"])

    
def waste_sorting_area():
    sorting_w=sorting_m*60+20
    sorting_h=sorting_n*60+20
    add_edge((racks_width,80),(sorting_w+racks_width,80),direction["left"])
    add_edge((racks_width,sorting_h+80),(sorting_w+racks_width,sorting_h+80),direction["right"])
    add_edge((racks_width,80),(racks_width,sorting_h+80),direction["down"])
    add_edge((sorting_w+racks_width,80),(sorting_w+racks_width,sorting_h+80),direction["up"])


    add_edge((racks_width-25,(80+racks_height//2)//2-25),(racks_width,(80+racks_height//2)//2-25),direction["left"]) #left queue
    add_edge((racks_width-25,int((80+racks_height//2)//2+20)),(racks_width,int((80+racks_height//2)//2+20)),direction["right"]) #right queue
    add_edge((racks_width-25,int((80+racks_height//2)//2-25)),(racks_width-25,int((80+racks_height//2)/2+20)),direction["down"]) #down queue
    #pygame.draw.line(screen,colors.BLUE,(racks_width,(80+racks_height//2)/2-25),(racks_width-25,(80+racks_height//2)/2-25),width=2)    # Left
    #pygame.draw.line(screen,colors.BLUE,(racks_width-25,(80+racks_height//2)/2+20),(racks_width,(80+racks_height//2)/2+20),width=2)    # Right
    #pygame.draw.line(screen,colors.BLUE,(racks_width-25,(80+racks_height//2)/2-25),(racks_width-25,(80+racks_height//2)/2+20),width=2)             #Down

    # (n+1)*15+n*10=sorting_n*100+15
    # (m+1)*15+m*10=sorting_m*100+15
    x=racks_width+20


    x=racks_width+10
    y=80
    for _ in range(sorting_m+1):
        add_edge((x, 80),(x,sorting_h+80),direction["up"])
        x+=60
    x=racks_width+40
    for _ in range(sorting_m):
        add_edge((x, 80),(x,sorting_h+80),direction["down"])
        x+=60
    for _ in range(sorting_n+1):
        add_edge((racks_width, y+10),(racks_width+sorting_w,y+10),direction["right"])
        y+=60
    y=110
    for _ in range(sorting_n):
        add_edge((racks_width, y+10),(racks_width+sorting_w,y+10),direction["left"])
        y+=30

waste1(n, m)
waste2(n,m)
marking_queue_line(n,m)
waste_conveyor_belt()
waste_sorting_area()
waste_charging()