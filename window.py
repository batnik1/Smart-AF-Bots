import argparse
parser=argparse.ArgumentParser()
parser.add_argument('n_Agents',type=int)
# parser.add_argument('RandomIns',type=int)
args=parser.parse_args()
from window_OrderHandler import *

import sys,io,os
from os import path
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


# index=args.n_Agents

test_flag=args.n_Agents//10
index=args.n_Agents%10
# print(index,test_flag)
init_agents(0,test_flag,index)


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

    # if key==0:
    #     new_items=truck_orders()
    #     Torders+=new_items

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
    # print(finish,num_Agents[2])
    # if num_Agents[index]-finish<=2:
        # extras=[]
        # for i in list(Position_Booking):
        #     extras.append(i)
        # # for i in range(1500):
        # #     for j in range(1500):
        # #         if Position_Booking[(i,j)]==1:
        # #             extras.append((i,j))
        # print(len(extras))
        # for extra in extras:
        #     pygame.draw.circle(screen, (0, 0, 255), (extra[0],extra[1]),6)
        # # input() 
    # if flag:
    # extras=[]
    # for i in range(m):
    #     for j in range(n):
    #         for k in range(5):
    #             for l in range(5):
    #                 if rack_available[str((i,j,k,l))]!=1:
    #                     print(rack_available[str((i,j,k,l))])
    #                     extras.append(str((i,j,k,l)))
    # print(len(extras))
    # input()
    # for extra in extras:
    #     pygame.draw.circle(screen, (0, 0, 255), (numofrack[extra][0],numofrack[extra][1]),6)        
    # input()
        
    # print(input.txt')):
#      sys.stdin = open('input.txt','r')
#      sys.stdout = open('output.txt','a')
# else:
#      input = io.finish,num_Agents[index],len(orders))
    if len(orders)==0 and finish==num_Agents[0]:
        str1='Without Congestion Management'
        if congestion_flag:
            str1='With Congestion Management'
        str2='Normal Intersection Management'
        if test_flag:
            str2='Intersection Management with Randomization and epsilon '+str(num_epsilon[index])
        print(str1,str2,'For',num_Agents[0],'Agents Final Key Value is -',key)
        break
    
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