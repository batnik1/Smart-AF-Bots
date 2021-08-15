import pygame
from final_run import *
pygame.init()
import random
screen = pygame.display.set_mode((display_height, display_width))  # create screen


agent_color=colors.LIGHTBLUE1

def make_rect(x, y):
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(x, y, 10, 10))


def make_line(x, y, color):
    if x:
        pygame.draw.line(screen, color, (x, 80), (x, racks_width-70))
    elif y:
        pygame.draw.line(screen, color, (80, y), (racks_height-70, y))

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



def draw_rack_lines(x,y):
    pygame.draw.line(screen,colors.ORANGE,(x+15,y-10),(x+15,y+100))     #up
    pygame.draw.line(screen,colors.ORANGE,(x+55,y-10),(x+55,y+100))     #up
    pygame.draw.line(screen,colors.ORANGE,(x+35,y-10),(x+35,y+100))     #down
    pygame.draw.line(screen,colors.ORANGE,(x+75,y-10),(x+75,y+100))     #down

    pygame.draw.line(screen,colors.ORANGE,(x-10,y+15),(x+100,y+15))      #right
    pygame.draw.line(screen,colors.ORANGE,(x-10,y+55),(x+100,y+55))      #right
    pygame.draw.line(screen,colors.ORANGE,(x-10,y+35),(x+100,y+35))      #left
    pygame.draw.line(screen,colors.ORANGE,(x-10,y+75),(x+100,y+75))      #left

def build_counter():
    # pygame.draw.rect(screen, colors.VIOLETRED3, pygame.Rect(100, 10, 60, 60))
    x=100
    for i in range(m):
        pygame.draw.rect(screen, colors.PURPLE1, pygame.Rect(x, 20, 60, 50))
        x+=120
    x=100
    for i in range(m):
        pygame.draw.rect(screen, colors.PURPLE1, pygame.Rect(x, 120*(n+1)-20, 60, 50))
        x+=120

def build_counter_lines():
    x=90
    for i in range(m):
        pygame.draw.line(screen, colors.ORANGE, (x, 10), (x, 80))
        pygame.draw.line(screen, colors.ORANGE, (x+80, 10), (x+80, 80))
        pygame.draw.line(screen, colors.ORANGE, (x, 10), (x+80,10))
        x+=120
    x=90
    for i in range(m):
        pygame.draw.line(screen, colors.ORANGE, (x, 120*(n+1)-30), (x, 40+120*(n+1)))
        pygame.draw.line(screen, colors.ORANGE, (x+80, 120*(n+1)-30), (x+80, 40+120*(n+1)))
        pygame.draw.line(screen, colors.ORANGE, (x, 40+120*(n+1)), (x+80,40+120*(n+1)))
        x+=120

running = True
i=0
flag_location=[] #0 ->source 1->at counter
Index=[]
Path=[]
voo=[]
agent_counter=[]
color_agent=[]
all_agents=[]
position=[]
size_agent=[]
for i in range(20):
    all_agents.append(i)
    Index.append(0)
    flag_location.append(0)
    path=0
    Path.append(path)
    v1=random.randint(0,n-1)
    v2=random.randint(0,m-1)
    v3=random.randint(0,4)
    v4=random.randint(0,4)
    voo.append((v1,v2,v3,v4))
    which_counter=random.randint(0,2*m-1)
    agent_counter.append(which_counter)
    color_agent.append(colors.RED1)
    position.append([0,0])
    size_agent.append(4)
    

while running:
    time.sleep(0.02)
    for agent in range(20):
        if Index[agent]==0:
            if flag_location[agent]==1:
                #time.sleep(2)
                v1=random.randint(0,n-1)
                v2=random.randint(0,m-1)
                v3=random.randint(0,4)
                v4=random.randint(0,4)
                voo[agent]=(v1,v2,v3,v4)
                print(agent," agent path now from human counter ",agent_counter[agent],"to rack (",v1,v2,v3,v4,")")
                Path[agent]= Counter[agent_counter[agent]].getBFSPath(numofrack[str((v1,v2,v3,v4))])
                Path[agent].reverse()
                Index[agent]=len(Path[agent])
                color_agent[agent]=colors.LIGHTBLUE1
                size_agent[agent]=2
                flag_location[agent]=0
            else:
                #time.sleep(2)
                agent_counter[agent]=random.randint(0,2*m-1)
                print(agent," agent path now from rack (",voo[agent][0],voo[agent][1],voo[agent][2],voo[agent][3],") to human counter ",agent_counter[agent])
                Path[agent]= Reverse_Counter[agent_counter[agent]].getBFSPath(numofrack[str((voo[agent][0],voo[agent][1],voo[agent][2],voo[agent][3]))])
                Index[agent]=len(Path[agent])
                color_agent[agent]=colors.RED1
                size_agent[agent]=4
                flag_location[agent]=1
            
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            break
    screen.fill((0, 0, 0))
    build_racks(n, m)
    draw_line(n, m)
    build_counter()
    build_counter_lines()
    for agent in range(20):
        if Index[agent]+1>0:
            Index[agent]-=1
        if Index[agent]>=0:
            position[agent]=(Path[agent][Index[agent]][0],Path[agent][Index[agent]][1])
        pygame.draw.circle(screen, color_agent[agent],position[agent], size_agent[agent])
        #print(position[i]," for agent ", i)
    pygame.display.update()
   