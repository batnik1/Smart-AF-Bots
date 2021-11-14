import argparse
parser=argparse.ArgumentParser()
parser.add_argument('n_Agents',type=int)
#parser.add_argument('Congestion',type=int)
args=parser.parse_args()
from window_OrderHandler import *

from window_AgentHandler import Number_of_Agents

Number_of_Agents = args.n_Agents
import sys,io,os
from os import path
from collections import Counter,defaultdict
if(path.exists('input.txt')):
     sys.stdin = open('input.txt','r')
     sys.stdout = open('output.txt','a')
else:
     input = io.BytesIO(os.read(0,os.fstat(0).st_size)).readline

clock = pygame.time.Clock()
running = 1
key=0
paused=0
order_freq=1
truck_freq=2000
initHCtoConveyor()
def init_screen():
    screen.fill((0, 0, 0))
    build_racks(n, m)
    draw_line(n, m)
    build_counter()
    build_station_zone()
    build_station_lines()
    build_counter_lines()
    conveyor()
    build_charging_lines()
    build_charging_zone()
    make_sorting_area()
init_agents()
def handle_events():
    global paused,running
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = 0
            quit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                if paused:
                    paused=0
                else:
                    paused=1
                    break
    while paused:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = 0
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    if paused:
                        paused=0
                    else:
                        paused=1
                        break


while running:
    #lobal flag_finisher
    if key%order_freq==0:
        new_orders=gen_a_order()    # new_orders= (racks,human_counter,order_id)    
        if new_orders!="Nothing":
            orders.append(new_orders)   # To mantain FCFS Order

    if key%truck_freq==0:
        new_items=truck_orders()
        Torders+=new_items

    init_screen()
    # make circles where new_praylist points are
    
    #new_praylist=[]  
    # for i,j in Intersections:
    #     if 1 in Matrix.grid[i][j] and 4 in Matrix.grid[i][j]:
    #         new_praylist.append((i,j))
    #     elif 4 in Matrix.grid[i][j]:
    #         pygame.draw.circle(screen, (255,0,0), (i,j), 5)

    # for i in range(len(new_praylist)):
    #     pygame.draw.circle(screen, (0, 0, 255), (new_praylist[i][0], new_praylist[i][1]),1)        
    handle_orders()
    handle_Torders()
    handle_events()
    finish=handle_rack_agents(coloring,key)
    # print(key)
    # print(finish,key)
    if len(orders)==0 and finish==Number_of_Agents:
        print('Final Key Value is ',key)
        break
    
    # if key%300==0:
    #     dummy_sorting(key,10)
    handle_conveyor_belt(sorting_orders)
    handle_sorting_agents(sorting_orders)
    # handle_truck_agents(key)
    # if key%50==0:
    #     handle_intersection()
    key+=1
    for colo in range(len(coloring)):
         pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(coloring[colo][0][0]+coloring[colo][1],coloring[colo][0][1]-5, 10, 10))
    
    pygame.display.update()
    