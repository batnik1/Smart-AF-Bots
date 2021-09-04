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
import logging



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

Number_of_Agents = 2
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

    for i in range(len(Agents)):
        if Agents[i].Wait==True:
            if mindis==ManhattanDistance(rack_pos, Agents[i].position):
                return i
    return -1
    
def pause():
    paused=True
    while paused:
        pass

#Creating Log File
logging.basicConfig(filename="Warehouse.log",format='%(asctime)s %(message)s',filemode='w')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)
orders=[]
loading_truck = 0
loading_truck_boxes = 10
key=0
coloring=[]
paused=False
while running:
    time.sleep(0.02)
    # if loading_truck == 1:
    #     for agent in Number_of_Agents:
    #         if loading_truck_boxes == 0:
    #             loading_truck = 0
    #             break
    #         agent.Path = write_path(agent.position)
    #         agent.Wait = False
    #         agent.color = colors.LIGHTBLUE1
    #         agent.size = 4
    #         agent.Index = len(agent.Path)
    #         loading_truck_boxes -= 1
    if key%500==0:
        new_orders=gen_a_order()    # new_orders= (racks,human_counter,order_id)    
        if new_orders!="Nothing":
            orders.append(new_orders)   # To mantain FCFC Order
    
    iteratations=len(orders)
    finished=[]
    for i in range(len(orders)):
        iteratations-=1
        list_racks = orders[i][0]
        hCounter=orders[i][1]
        order_id=orders[i][2]
        count=0
        finished_racks=[]
        for rack in list_racks:    
            if rack_available[rack]!=1:
                continue

            rack_location=numofrack[rack]
            ind = get_Agent(rack_location)
            if ind == -1:
                break
            rack_available[rack]=1
            agent=Agents[ind]
            logger.info('Bot '+str(ind)+" is assigned to go to Rack "+str(rack))
            agent.ind=ind
            bot_db.insert_one({"_id":ind,"Order_ID":order_id,"Rack":rack,"Items":list_racks[rack],"target":[hCounter]})
            nAgent = Search(agent.position,rack_location)
            nAgent.BFS()
            
            count+=1
            finished_racks.append(rack)
            
            a = nAgent.getPath()                                 # Agent's Position to Desired Rack 
            b = Reverse_Counter[hCounter].getBFSPath(rack_location)     # From that Rack to Counter
            c = Counter[hCounter].getBFSPath(rack_location)
            b.reverse()

            agent.Path =a+[[-7,-7]]+b+[[-14,-14]]+c+[[-21,-21]]
            agent.Path.reverse()
            agent.Index = len(agent.Path)
            agent.Wait = False
            agent.color = colors.LIGHTBLUE1
            agent.size = 4
            agent.order_id=order_id
            agent.items_carrying=list_racks[rack]
            agent.CurRack=rack
            # print("delivering item type ", rack_pos[1][0]," of quantity ",rack_pos[1][1]," from ",rack_pos[0])
            # pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(rack_pos_location[0]+5,rack_pos_location[1]-5, 10, 10))
            if rack[7]=="0":
                coloring.append((numofrack[rack],10,agent))
            else:
                coloring.append((numofrack[rack],5,agent))
        for rack in finished_racks:
            orders[i][0].pop(rack)
        if len(orders[i][0])==0:
            finished.append(i)      
              
    
    for ind in finished:
        orders.remove(orders[ind])
    finished.clear()

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            quit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                if paused:
                    paused=False
                else:
                    paused=True
                    break
    
    while paused:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    if paused:
                        paused=False
                    else:
                        paused=True
                        break
    screen.fill((0, 0, 0))
    build_racks(n, m)
    draw_line(n, m)
    build_counter()
    build_station_zone()
    build_station_lines()
    build_counter_lines()
    for agent in Agents:
        if agent.Index==2:                      # Coloring Racks 
            remove=[]
            for colo in range(len(coloring)):
                if coloring[colo][0]==agent.CurRack:
                    remove.append(coloring[colo])
            for i in remove:
                coloring.remove(i)
        agent.Index -= 1
        if agent.Index >= 0:
            if agent.Path[agent.Index]==[-7,-7]:
                agent.Index -= 1
                logger.info('Bot '+str(agent.ind)+': Reached the Desired Rack')
            elif agent.Path[agent.Index]==[-14,-14]:
                logger.info('Bot '+str(agent.ind)+': Reached the Human Counter with items '+str(agent.items_carrying))
                doc=order_db.find_one({"_id":agent.order_id})
                quantity=doc["ordered_quantity"]
                progress=doc["order_progress"]
                total_items_carrying=0
                for items in agent.items_carrying:
                    total_items_carrying+=items[1]
                order_db.update_one({"_id":agent.order_id},{"$inc":{"order_progress":total_items_carrying}})
                agent.Index -= 1
            elif agent.Path[agent.Index]==[-21,-21]:
                logger.info('Bot '+str(agent.ind)+': Back at my Rack Now')
                agent.Index -= 1
            else: 
                agent.position = (agent.Path[agent.Index][0], agent.Path[agent.Index][1])
        if agent.Index == -1:
            agent.Path = []
            rack_available[agent.CurRack]=0
            bot_db.delete_one({"_id":agent.ind})
            agent.Wait = True
            agent.color = colors.YELLOW1
            agent.size = 2
            remove=[]
            for colo in range(len(coloring)):
                if coloring[colo][2]==agent:
                    remove.append(coloring[colo])
            for i in remove:
                coloring.remove(i)
        pygame.draw.circle(screen, agent.color, agent.position, agent.size)
    key+=1
    for colo in range(len(coloring)):
         pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(coloring[colo][0][0]+coloring[colo][1],coloring[colo][0][1]-5, 10, 10))

    pygame.display.update()