import argparse
import numpy as np
import cv2
import pyautogui
parser=argparse.ArgumentParser()
parser.add_argument('n_Agents',type=int)
# parser.add_argument('Congestion',type=int)
args=parser.parse_args()
from window_OrderHandler import *

import sys,io,os
from os import path
if(path.exists('input.txt')):
#     sys.stdin = open('input.txt','r')
     sys.stdout = open('output.txt','a')
else:
     input = io.BytesIO(os.read(0,os.fstat(0).st_size)).readline

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


index=args.n_Agents
#index=4
init_agents(index)

# 
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
                #        add_items(5)
                    else:
                        paused=1
                        break



while running:
    #lobal flag_finisher
    if key%order_freq==0:
        new_orders=gen_a_order()    # new_orders= (racks,human_counter,order_id)    
        if new_orders!="Nothing":
            orders.append(new_orders)   # To mantain FCFS Order

    if key==0:
        new_items=truck_orders()
        Torders+=new_items

    init_screen() 
    handle_orders()
    handle_Torders()
    handle_events()
    finish=handle_rack_agents(coloring,key)

    # if finish>num_Agents[index]-4:
    # new_praylist=[]  
    # for i,j in Intersections:
    #     pygame.draw.circle(screen, (0,255,0), (i,j), 4)

    # if len(orders)==0 and finish==num_Agents[index]:
    #     str='Without Congestion Management'
    #     if congestion_flag:
    #         str='With Congestion Management'
    #     print(str,'For',num_Agents[index],'Agents Final Key Value is -',key)
    #     break
    # if key%300==0:
    #     dummy_sorting(key,10)
    handle_conveyor_belt(sorting_orders)
    handle_sorting_agents(sorting_orders)
    handle_truck_agents(key)
    # if key%50==0:
    #     handle_intersection()
    key+=1

    for colo in range(len(coloring)):
         pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(coloring[colo][0][0]+coloring[colo][1],coloring[colo][0][1]-5, 10, 10))
    
    


    pygame.display.update()
    pygame.image.save(screen,"./Pics/image"+str(key)+".jpg")
    # image = pyautogui.screenshot()
    # image = cv2.cvtColor(np.array(image),cv2.COLOR_RGB2BGR)
    # writing it to the disk using opencv
    # if not cv2.imwrite("./Pics/image"+str(key)+".png", image):
    #     raise Exception("Could not write image")
   # x=input()    