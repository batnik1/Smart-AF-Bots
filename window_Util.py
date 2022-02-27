import AStar
from Agent007 import Agent
import pygame
from Orders import *
from Path_planner import *
import collections
# file just for drawing and showing to screen different utilities
pygame.init()
screen = pygame.display.set_mode((display_width, display_height))  # create screen
# pygame.event.set_allowed([pygame.QUIT, #pygame.K_SPACE])

dir = [(-1, -1), (0, -1), (0, 1), (1, 0), (-1, 0)]      # (-1,-1) is just pushed to make it 1 based indexing


def ManhattanDistance(start, end):
    return abs(start[0]-end[0])+abs(start[1]-end[1])

agent_color = colors.LIGHTBLUE1

# Paths from Human Counter to sorting area
HCtoConveyor={}
def initHCtoConveyor():
    x=130
    for i in range(2*m):
        if i==m:
            x=130
        if i<m:
            HCtoConveyor[i]=(x,15)
        else:
            HCtoConveyor[i]=(x, racks_height-5)    
        x+=120
        
def compare(item1, item2):
    if item1[0] < item2[0]:
        return -1
    elif item1[0] > item2[0]:
        return 1
    else:
        return 0

# Making the sorting area
def make_sorting_area():
    sorting_w=sorting_m*60+20
    sorting_h=sorting_n*60+20
   # pygame.draw.rect(screen,colors.BLUE,pygame.Rect(racks_width,80,sorting_w,sorting_h),3)
    pygame.draw.line(screen,colors.BLUE,(racks_width+10,(80+racks_height//2)/2-20),(racks_width-40,(80+racks_height//2)/2-20),width=2)    # Left
    pygame.draw.line(screen,colors.BLUE,(racks_width-40,(80+racks_height//2)/2+70),(racks_width+10,(80+racks_height//2)/2+70),width=2)    # Right
    pygame.draw.line(screen,colors.BLUE,(racks_width-40,(80+racks_height//2)/2-20),(racks_width-40,(80+racks_height//2)/2+70),width=2)    # Down
    x=racks_width+20

    for _ in range(int(2*sorting_m-1)):
       y=100
       for _ in range(int(2*sorting_n-1)):
           make_rect(x, y,colors.PURPLE3)
           y+=30
       x+=30  
    x=racks_width+10
    y=80
    for i in range(2*sorting_m):
        pygame.draw.line(screen, colors.BLUE, (x, 90),(x,sorting_h+40),2)
        x+=30
    for i in range(2*sorting_n):
        pygame.draw.line(screen, colors.BLUE, (racks_width+10, y+10),(racks_width+sorting_w-40,y+10),2)
        y+=30   

# Drawing the coveyor on screen
def conveyor():
    pygame.draw.line(screen, colors.GREEN, (130, 0), (racks_width, 0))
    pygame.draw.line(screen, colors.GREEN, (130, racks_height+10), (racks_width, racks_height+10),width=2)
    x=130
    for i in range(m):
        pygame.draw.line(screen, colors.GREEN, (x, 0), (x, 15),width=10)
        pygame.draw.line(screen, colors.GREEN, (x, racks_height+10), (x,racks_height-5 ),width=10)
        x+=120
    
    pygame.draw.line(screen, colors.GREEN, (racks_width, 0), (racks_width, racks_height+10),width=2)
    
    

# Functions to draw different things on screen
def make_rect(x, y,color=(255,0,0)):
    pygame.draw.rect(screen,color, pygame.Rect(x, y, 10, 10))


def make_line(x, y, color):
    if x:
        pygame.draw.line(screen, color, (x, 80), (x, racks_height-70))
    elif y:
        pygame.draw.line(screen, color, (80, y), (racks_width-70, y))


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


def draw_rack_lines(x, y,color=colors.ORANGE):
   # return
    pygame.draw.line(screen, color, (x+15, y-10), (x+15, y+100))  # up
    pygame.draw.line(screen, color, (x+55, y-10), (x+55, y+100))  # up
    pygame.draw.line(screen, color,
                     (x+35, y-10), (x+35, y+100))  # down
    pygame.draw.line(screen, color,
                     (x+75, y-10), (x+75, y+100))  # down

    pygame.draw.line(screen, color, (x-10, y+15),
                     (x+100, y+15))  # right
    pygame.draw.line(screen, color, (x-10, y+55),
                     (x+100, y+55))  # right
    pygame.draw.line(screen, color,
                     (x-10, y+35), (x+100, y+35))  # left
    pygame.draw.line(screen, color,
                     (x-10, y+75), (x+100, y+75))  # left


def build_counter():
  #  return
    pygame.draw.rect(screen, colors.VIOLETRED3, pygame.Rect(100, 10, 60, 60))
    x = 100
    for i in range(m):
        pygame.draw.rect(screen, colors.PURPLE1, pygame.Rect(x, 20, 60, 50))
        x += 120
    x = 100
    for i in range(m):
        pygame.draw.rect(screen, colors.PURPLE1,
                         pygame.Rect(x, 120*(n+1)-20, 60, 50))
        x += 120


def build_counter_lines():
    #return 
    x = 90
    for i in range(m):
        pygame.draw.line(screen, colors.ORANGE, (x, 10), (x, 80))
        pygame.draw.line(screen, colors.ORANGE, (x+80, 10), (x+80, 80))
        pygame.draw.line(screen, colors.ORANGE, (x, 10), (x+80, 10))
        x += 120
    x = 90
    for _ in range(m):
        pygame.draw.line(screen, colors.ORANGE,
                         (x, 120*(n+1)-30), (x, 40+120*(n+1)))
        pygame.draw.line(screen, colors.ORANGE,
                         (x+80, 120*(n+1)-30), (x+80, 40+120*(n+1)))
        pygame.draw.line(screen, colors.ORANGE,
                         (x, 40+120*(n+1)), (x+80, 40+120*(n+1)))
        x += 120


def build_station_lines():
  #  return
    pygame.draw.line(screen, colors.ORANGE, (80, 80), (30, 80))
    pygame.draw.line(screen, colors.ORANGE, (80, (n//2+n%2)*100), ((30, (n//2+n % 2)*100)))
    pygame.draw.line(screen, colors.ORANGE, (30, (n//2+n%2)*100), ((30, 80)))

    for y in range(80+10,(n//2+n % 2)*100,10):
        pygame.draw.line(screen, colors.ORANGE, (30, y), (80,y))


def build_station_zone():
    # (x,y,x+l,y+b)
   # return
    pygame.draw.rect(screen, colors.PURPLE2,pygame.Rect(30, 80, 50, (n//2+n % 2)*100-80))


charging_state={}
charging_loc={}
charging_state_list=[]


# Drawing chargin Stations
def build_charge_dict():
    counting=-1
    for i in range((n//2+n % 2)*100+20,racks_height-90,10):
        counting+=1
        charging_state_list.append(counting)
        charging_state[counting]=0
        charging_loc[counting]=(55,i)
        pygame.draw.line(screen, colors.ORANGE, (30, i), (80, i))   
build_charge_dict()
def build_charging_zone():
    for i in range((n//2+n % 2)*100+20,racks_height-90,10):
        pygame.draw.line(screen, colors.ORANGE, (30, i), (80, i))    


def build_charging_lines():
    pygame.draw.line(screen, colors.ORANGE, (80, (n//2+n % 2)*100+10), (30, (n//2+n % 2)*100+10))
    pygame.draw.line(screen, colors.ORANGE, (80, racks_height-90), ((30, racks_height-90)))
    pygame.draw.line(screen, colors.ORANGE, (30, (n//2+n % 2)*100+10), (30, racks_height-90))

def get_charging():
    for i in range(len(charging_state_list)):
        if charging_state[i]==0:
            charging_state[i]=1
            return i,charging_loc[i]
    return -1,-1
