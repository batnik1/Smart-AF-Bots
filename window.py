import AStar
from Agent007 import Agent
import random
import pygame
from final_run import *
from Orders import *
import collections
pygame.init()
screen = pygame.display.set_mode(
    (display_height, display_width))  # create screen
import time


def ManhattanDistance(start, end):
    return abs(start[0]-end[0])+abs(start[1]-end[1])


agent_color = colors.LIGHTBLUE1


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


def draw_rack_lines(x, y):
    pygame.draw.line(screen, colors.ORANGE, (x+15, y-10), (x+15, y+100))  # up
    pygame.draw.line(screen, colors.ORANGE, (x+55, y-10), (x+55, y+100))  # up
    pygame.draw.line(screen, colors.ORANGE,
                     (x+35, y-10), (x+35, y+100))  # down
    pygame.draw.line(screen, colors.ORANGE,
                     (x+75, y-10), (x+75, y+100))  # down

    pygame.draw.line(screen, colors.ORANGE, (x-10, y+15),
                     (x+100, y+15))  # right
    pygame.draw.line(screen, colors.ORANGE, (x-10, y+55),
                     (x+100, y+55))  # right
    pygame.draw.line(screen, colors.ORANGE,
                     (x-10, y+35), (x+100, y+35))  # left
    pygame.draw.line(screen, colors.ORANGE,
                     (x-10, y+75), (x+100, y+75))  # left


def build_counter():
    # pygame.draw.rect(screen, colors.VIOLETRED3, pygame.Rect(100, 10, 60, 60))
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
    x = 90
    for i in range(m):
        pygame.draw.line(screen, colors.ORANGE, (x, 10), (x, 80))
        pygame.draw.line(screen, colors.ORANGE, (x+80, 10), (x+80, 80))
        pygame.draw.line(screen, colors.ORANGE, (x, 10), (x+80, 10))
        x += 120
    x = 90
    for i in range(m):
        pygame.draw.line(screen, colors.ORANGE,
                         (x, 120*(n+1)-30), (x, 40+120*(n+1)))
        pygame.draw.line(screen, colors.ORANGE,
                         (x+80, 120*(n+1)-30), (x+80, 40+120*(n+1)))
        pygame.draw.line(screen, colors.ORANGE,
                         (x, 40+120*(n+1)), (x+80, 40+120*(n+1)))
        x += 120


def build_station_lines():
    pygame.draw.line(screen, colors.ORANGE, (80, 80), (30, 80))
    pygame.draw.line(screen, colors.ORANGE, (80, (n//2+n %
                     2)*100), ((30, (n//2+n % 2)*100)))
    pygame.draw.line(screen, colors.ORANGE, (30, (n//2+n % 2)*100), ((30, 80)))


def build_station_zone():
    # (x,y,x+l,y+b)
    pygame.draw.rect(screen, colors.AQUAMARINE2,
                     pygame.Rect(30, 80, 50, (n//2+n % 2)*100-80))


running = True

Number_of_Agents = 10
Agents = []
for i in range(Number_of_Agents):
    nAgent=Agent(0,n,m)
    nAgent.position=numofrack[nAgent.CurRack]
    Agents.append(nAgent)
    


def write_path(agent_position):
    a = Reverse_Station[0].getBFSPath(agent_position)
    b = Station[0].getBFSPath(agent_position)
    b.reverse()
    a = a+b
    return a

#  from one rack to another + to the goal

def compare(item1, item2):
    if item1[0] < item2[0]:
        return -1
    elif item1[0] > item2[0]:
        return 1
    else:
        return 0

def get_Agent(rack_pos):
    mindis=99999999999999999
    for agent in Agents:
        if agent.Wait == True and mindis>ManhattanDistance(rack_pos, agent.position):
            mindis=ManhattanDistance(rack_pos, agent.position)

    for agent in Agents:
        if agent.Wait==True:
            if mindis==ManhattanDistance(rack_pos, agent.position):
                return agent

    return -1
    
orders=collections.deque()
loading_truck = 0
loading_truck_boxes = 10
key=0
coloring=[]
while running:
    time.sleep(0.02)
    #print(key)
    if loading_truck == 1:
        for agent in Number_of_Agents:
            if loading_truck_boxes == 0:
                loading_truck = 0
                break
            agent.Path = write_path(agent.position)
            agent.Wait = False
            agent.color = colors.LIGHTBLUE1
            agent.size = 4
            agent.Index = len(agent.Path)
            loading_truck_boxes -= 1
    if key%100==0:
        new_orders=random_order()
        while new_orders:
            orders.append(new_orders[0])
            new_orders.popleft()
            
    
    iteratations=len(orders)
    while iteratations>=1:
        iteratations-=1
        rack_pos = orders.popleft()
        if rack_availaible[rack_pos[0]]!=1:
            orders.append(rack_pos)
            continue
        rack_pos_location=numofrack[rack_pos[0]]
        agent = get_Agent(rack_pos_location)
        if agent == -1:
            orders.append(rack_pos)
            break
        
        start1=time.perf_counter()
        nAgent = Search(agent.position,rack_pos_location)
        nAgent.BFS()
        a = nAgent.getPath()
        start2=time.perf_counter()
        #print("outer one",start2-start1)
        nCounter = random.randint(0, 2*m-1)
        b = Reverse_Counter[nCounter].getBFSPath(rack_pos_location)
        c = Counter[nCounter].getBFSPath(rack_pos_location)
        b.reverse()
        agent.Path =a+b+c
        agent.Path.reverse()
        agent.Index = len(agent.Path)
        agent.Wait = False
        agent.color = colors.LIGHTBLUE1
        agent.size = 4
        print("delivering item type ", rack_pos[1][0]," of quantity ",rack_pos[1][1]," from ",rack_pos[0])
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(rack_pos_location[0]+5,rack_pos_location[1]-5, 10, 10))
        
        if rack_pos[0][7]=="0":
            coloring.append((rack_pos_location,10))
        else:
            coloring.append((rack_pos_location,5))
        #delivered.insert_one()
        
  
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            break
    screen.fill((0, 0, 0))
    build_racks(n, m)
    draw_line(n, m)
    build_counter()
    build_station_zone()
    build_station_lines()
    build_counter_lines()
    for agent in Agents:
        agent.Index -= 1
        if agent.Index >= 0:
            agent.position = (
                agent.Path[agent.Index][0], agent.Path[agent.Index][1])
        if agent.Index == -1:
            agent.Path = []
            agent.Wait = True
            agent.color = colors.YELLOW1
            agent.size = 2
        pygame.draw.circle(screen, agent.color, agent.position, agent.size)
    key+=1
    for colo in range(len(coloring)):
         pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(coloring[colo][0][0]+coloring[colo][1],coloring[colo][0][1]-5, 10, 10))

    pygame.display.update()

 # for agent in range(20):
    #     if waiting_state[agent]==0:
    #         if flag_location[agent]==1:
    #             collection.update_one({"_id":agent_counter[agent]},{"$inc":{"score": 1}})
    #             #time.sleep(2)
    #             v1=random.randint(0,n-1)
    #             v2=random.randint(0,m-1)
    #             v3=random.randint(0,4)
    #             v4=random.randint(0,4)
    #             voo[agent]=(v1,v2,v3,v4)
    #             print(agent," agent path now from human counter ",agent_counter[agent],"to rack (",v1,v2,v3,v4,")")
    #             Path[agent]= Counter[agent_counter[agent]].getBFSPath(numofrack[str((v1,v2,v3,v4))])
    #             Path[agent].reverse()
    #             Index[agent]=len(Path[agent])
    #             color_agent[agent]=colors.LIGHTBLUE1
    #             size_agent[agent]=2
    #             flag_location[agent]=0
    #         else:
    #             #time.sleep(2)
    #             agent_counter[agent]=random.randint(0,2*m-1)
    #             print(agent," agent path now from rack (",voo[agent][0],voo[agent][1],voo[agent][2],voo[agent][3],") to human counter ",agent_counter[agent])
    #             Path[agent]= Reverse_Counter[agent_counter[agent]].getBFSPath(numofrack[str((voo[agent][0],voo[agent][1],voo[agent][2],voo[agent][3]))])
    #             Index[agent]=len(Path[agent])
    #             color_agent[agent]=colors.RED1
    #             size_agent[agent]=4
    #             flag_location[agent]=1
