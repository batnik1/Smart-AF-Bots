import pygame
from Agent007 import Agent
from Grid import Grid
import AStar
from AStar import Search,Matrix
import colors
pygame.init()
import time
# n,m=input().split()   Take input from User
n = 5   # height
m = 5   # width

display_height = 120*m+160
display_width = 120*n+160
racks_height = 120*m+160
racks_width = 120*n+160

screen = pygame.display.set_mode((display_height, display_width))  # create screen
running = True

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


def make_rect(x, y):
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(x, y, 10, 10))


pygame.display.set_caption("Amazon Warehouse")


def make_line(x, y, color):
    if x:
        pygame.draw.line(screen, color, (x, 80), (x, racks_width-70))
    elif y:
        pygame.draw.line(screen, color, (80, y), (racks_height-70, y))


def waste3(x, y, dir):
    if x:
        add_edge((x, 80), (x, racks_width-70),dir)
    elif y:
        add_edge((80, y), (racks_height-70, y),dir)

counter = pygame.image.load("human.png")

start = numofrack[str((0,0,1,1))]
goal1 = numofrack[str((2,2,1,4))]
Agent1 = Agent(start, goal1)


#Applying A Star Here


# n - Height m - Cols
def build_racks(n, m):
    y = 100
    for ro in range(0, n):
        x = 100
        for cols in range(0, m):
            for i in range(x, x+100, 20):
                for j in range(y, y+100, 20):
                    make_rect(i, j)
            draw_rack_lines(x, y)
            x += 120
        y += 120

def waste1(n,m):
    y = 100
    for ro in range(0, n):
        x = 100
        for cols in range(0, m):
            marking_line(x, y)
            x += 120
        y += 120


def draw_line(n, m):
    x = 80
    for i in range(m+1):
        make_line(x, 0, colors.ORANGE)  # up
        make_line(x+10, 0, colors.ORANGE)  # down
        x += 120
    y = 80
    for i in range(n+1):
        make_line(0, y, colors.ORANGE)  # right
        make_line(0, y+10, colors.ORANGE)  # left
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


def draw_rack_lines(x,y):
    pygame.draw.line(screen,colors.ORANGE,(x+15,y-10),(x+15,y+100))     #up
    pygame.draw.line(screen,colors.ORANGE,(x+55,y-10),(x+55,y+100))     #up
    pygame.draw.line(screen,colors.ORANGE,(x+35,y-10),(x+35,y+100))     #down
    pygame.draw.line(screen,colors.ORANGE,(x+75,y-10),(x+75,y+100))     #down

    pygame.draw.line(screen,colors.ORANGE,(x-10,y+15),(x+100,y+15))      #right
    pygame.draw.line(screen,colors.ORANGE,(x-10,y+55),(x+100,y+55))      #right
    pygame.draw.line(screen,colors.ORANGE,(x-10,y+35),(x+100,y+35))      #left
    pygame.draw.line(screen,colors.ORANGE,(x-10,y+75),(x+100,y+75))      #left


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

cAgent=Search(start,goal1)
cAgent.AStarModif()
Path=cAgent.getPath()

i=0
while running:
    time.sleep(0.02)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            break
    screen.fill((0, 0, 0))
    screen.blit(counter, (racks_height+200, racks_height+200))
    build_racks(n, m)
    draw_line(n, m)
    if i+1<len(Path):
        i+=1
    if i<len(Path):
        Agent1.playerX=Path[i][0]
        Agent1.playerY=Path[i][1]
    pygame.draw.circle(screen, colors.LIGHTBLUE1,(Agent1.playerX, Agent1.playerY), 2)
    pygame.display.update()

#print(Matrix.grid[81][80])