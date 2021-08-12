import pygame
from Agent007 import Agent
pygame.init()
# n,m=input().split()   Take input from User
n=10   # height
m=10    # width

display_height= 1000
display_width= 1000
racks_height= 60*m+80
racks_width= 60*n+80

screen = pygame.display.set_mode((display_height, display_width))  # create screen
running = True

def make_rect(x,y):
    pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x, y, 5, 5))


pygame.display.set_caption("Amazon Warehouse")

def make_line(x,y,color):
    if x:
        pygame.draw.line(screen,color,(x,40),(x,racks_width-35))
    elif y:
        pygame.draw.line(screen,color,(40,y),(racks_height-35,y))

counter = pygame.image.load("human.png")

start=[100,100]
goal1=[200,200]
Agent1=Agent(start,goal1)


# n - Height m - Cols
def build_racks(n,m): 
    y=50
    for ro in range(0,n):
        x=50
        for cols in range(0,m):
            for i in range(x,x+50,10):
                for j in range(y,y+50,10):
                    make_rect(i,j)
            draw_rack_lines(x,y)
            x+=60
        y+=60    

def draw_line(n,m):
    x=40
    for i in range(m+1):
        make_line(x,0,(251,255,5))
        make_line(x+5,0,(0,255,255))
        x+=60
    y=40
    for i in range(n+1):
        make_line(0,y,(251,255,5))
        make_line(0,y+5,(0,255,255))
        y+=60

def draw_rack_lines(x,y):
    pygame.draw.line(screen,(251,255,5),(x+7.5,y-5),(x+7.5,y+50))
    pygame.draw.line(screen,(251,255,5),(x+27.5,y-5),(x+27.5,y+50))
    pygame.draw.line(screen,(0,255,255),(x+17.5,y-5),(x+17.5,y+50))
    pygame.draw.line(screen,(0,255,255),(x+37.5,y-5),(x+37.5,y+50))

    pygame.draw.line(screen,(251,255,5),(x-5,y+7.5),(x+50,y+7.5))
    pygame.draw.line(screen,(251,255,5),(x-5,y+27.5),(x+50,y+27.5))
    pygame.draw.line(screen,(0,255,255),(x-5,y+17.5),(x+50,y+17.5))
    pygame.draw.line(screen,(0,255,255),(x-5,y+37.5),(x+50,y+37.5))


a=[[20,42],[100,100],[240,300]]
j=0
i=0
while running:
    events=pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            break
    screen.fill((0, 0, 0))
    screen.blit(counter,(racks_height+200,racks_height+200))
    build_racks(n,m)
    draw_line(n,m)
    j=(j+1)%100
    Agent1.move([goal1[0],goal1[1]+j])
    pygame.draw.circle(screen,(255,0,0),(Agent1.playerX,Agent1.playerY), 4)
    pygame.display.update()
