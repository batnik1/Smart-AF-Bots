import argparse
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
Total_orders=0
Running_Finisher=0
while running:
    if key%order_freq==0:
        new_orders=gen_a_order()    # new_orders= (racks,human_counter,order_id)    
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
            if r==1:
                pygame.draw.circle(screen, colors.RED1, I,2)  #Up
            elif r==2:
                pygame.draw.circle(screen, colors.GREEN1,I,2) #Down
            elif r==3:
                pygame.draw.circle(screen, colors.YELLOW1,I,2)#Right
            elif r==4:
                pygame.draw.circle(screen, colors.BLUE,I,2) #Left


    if key==0:
        # dummy_sorting(key,100)
        Final_Finisher=212
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
    pygame.draw.rect(screen, colors.INDIANRED1, pygame.Rect(racks_width+50,40,100,10),1)
    pygame.draw.rect(screen, colors.INDIANRED1, pygame.Rect(racks_width+50,40,orders_done/pending_orders*100,10),0)
    print(pending_orders,orders_done)
    screen.blit(PBar_Orders,(racks_width+160,35))

    pygame.display.update()
    if Running_Finisher==Final_Finisher:
        print(Running_Finisher)
        break
print("DONE",pending_orders,orders_done)
 #   pygame.image.save(screen,"./New/image"+str(key)+".jpg")
   