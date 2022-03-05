import argparse
from enum import Flag
from re import L
import numpy as np

from window_OrderHandler import *


pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 15)
PBar_Items = myfont.render('Progress Bar for Remaining Items', False, (255, 255, 255))
PBar_Orders=myfont.render('Progress Bar for Remaining Orders', False, (255, 255, 255))
Traffic_Flag=config['Traffic_Flag']
running = 1
key=0  
paused=0  
items_done=0
orders_done=0
order_freq=config['order_freq']
truck_freq=config['truck_freq']
sbig_flag=config['SBIG']

initHCtoConveyor()
def init_screen():
  #  pass
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

# https://<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>@github.com/<lordgavy01>/<Smart-AF-Bots>.git
"""
velocity,density
0.8849388764779784,0.04
0.8422870938888083,0.05
0.6598127291564279,0.1
0.7908560072151424,0.08
0.6316617300675831,0.12
0.491562152469726,0.15
0.8799984059669639,0.03
0.3999772068236708,0.2
0.4935203863876017,0.16
1.1849992315902942,0.01
0.18067947929292297,0.25
0.19653789061143037,0.3
0.35449773005951474,0.24
0.800190339844804,0.07
1.0702664571213356,0.02
0.962159466366327,0.06
0.8318022972901102,0.09
0.566065271223799,0.13
0.47711237571118814,0.17
0.78492482407427,0.11
0.3751944014274457,0.14
0.41059596785296576,0.18
0.39169760953750776,0.19
0.34688303277550997,0.21
"""








Total_orders=0
Running_Finisher=0
while running:
    if key%order_freq==0:
        new_orders=gen_a_order()    # new_orders= (racks,human_counter,order_id)    
     #   print(new_orders)
        if new_orders!="Nothing": 
            Total_orders+=1
            orders.append(new_orders)   # To mantain FCFS Order

    # if key%truck_freq==0:
    #     new_items=truck_orders()
    #     Torders+=new_items
    
    init_screen() 
    if sbig_flag:
        handle_orders_SBIG()
    else:
        handle_orders()
    
    handle_events()
    # if key==0:
    #     dummy_sorting(key,100)
    current_items,orders_completed_now,Running_Fin=handle_rack_agents(key,coloring)
    Running_Finisher+=Running_Fin
    if Traffic_Flag:
        update_intersection()
        for I in Intersections:
            r=Intersection_Gateway[I]

            try:
                r=r.index(1)
            except:
                pass
            # Red for 1, Green for 2, Yellow for 3, Blue for 4
            # if r==1:
            #     pygame.draw.circle(screen, colors.RED1, I,2)  #Up
            # elif r==2:
            #     pygame.draw.circle(screen, colors.GREEN1,I,2) #Down
            # elif r==3:
            #     pygame.draw.circle(screen, colors.YELLOW1,I,2)#Right
            # elif r==4:
            #     pygame.draw.circle(screen, colors.BLUE,I,2) #Left


    Final_Finisher=order_db.count_documents({})
   # Final_Finisher=100
    handle_conveyor_belt(sorting_orders)
    handle_sorting_agents(sorting_orders)
    # handle_truck_agents(key)
    key+=1

    pygame.draw.circle(screen,(255,0,0),numofdump["conveyor"],3)

    for colo in range(len(coloring)):
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(coloring[colo][0][0]+coloring[colo][1],coloring[colo][0][1]-5, 10, 10),1)
    
    items_done+=current_items
    screen.blit(PBar_Items,(racks_width+160,55))
    # Make a progress bar with a base rectangle as 100% and filled with items_done/total_items*100%
    pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(racks_width+50,60,100,10),1)
    pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(racks_width+50,60,100-items_done/total_items*100,10),0)
    pending_orders=Total_orders
    if pending_orders==0:
        pending_orders=1000
    orders_done+=orders_completed_now
    print(pending_orders,orders_done,Final_Finisher,Running_Finisher)
    pygame.draw.rect(screen, colors.INDIANRED1, pygame.Rect(racks_width+50,40,100,10),1)
    pygame.draw.rect(screen, colors.INDIANRED1, pygame.Rect(racks_width+50,40,orders_done/pending_orders*100,10),0)
   # print(pending_orders,orders_done)
    screen.blit(PBar_Orders,(racks_width+160,35))
   # print(Running_Finisher,Final_Finisher)
    pygame.display.update()
    if Running_Finisher==Final_Finisher:
        print(key)
        break
print("DONE",pending_orders,orders_done)
 #   pygame.image.save(screen,"./New/image"+str(key)+".jpg")
   