from window_OrderHandler import *
clock = pygame.time.Clock()
running = 1
key=0
paused=0
order_freq=10
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
    
  #  print(Position_Booking)
   # input("At the end of world")
    # for i,j in Intersections:
    #     # if Position_Booking[(i,j)]!=0:
    #     #     new_praylist.append((i,j))
    #         #pygame.draw.circle(screen, (0,0,255), (i,j), 5)
    #     if Intersection_Gateway[(i,j)][1]==1:
    #         if Intersection_Gateway[(i,j)]!=[0,1,0,0,0]:
    #             print("rigged")
    #        # print(Intersection_Gateway[(i,j)])
    #         pygame.draw.circle(screen, (255,255,255), (i,j), 10)
    #     elif Intersection_Gateway[(i,j)][4]==1:
    #    #     print(Intersection_Gateway[(i,j)])
    #         pygame.draw.circle(screen, (0,0,255), (i,j), 10)
        
    # for i,j in Intersections:
    #     if 1 in Matrix.grid[i][j] and 4 in Matrix.grid[i][j]:
    #         new_praylist.append((i,j))
    #     elif 4 in Matrix.grid[i][j]:
    #         pygame.draw.circle(screen, (255,0,0), (i,j), 5)

    # for i in range(len(new_praylist)):
    #     pygame.draw.circle(screen, (0, 0, 255), (new_praylist[i][0], new_praylist[i][1]),1)    
    # for i in range(len(spec)):
    #     pygame.draw.circle(screen, (255, 0,0), (spec[i][0], spec[i][1]),1)    
    handle_orders()
    handle_Torders()
    handle_events()
    handle_rack_agents(coloring,key)
    handle_conveyor_belt(sorting_orders)
    handle_sorting_agents(sorting_orders)
    #handle_truck_agents()
    # if key%50==0:
    #     handle_intersection()
    key+=1
   # print(Intersection_Gateway)
    # for i,j in list(Intersection_Gateway):
    #     if Intersection_Gateway[(i,j)]!=[0]*5:
    #         print(i,j,Intersection_Gateway[(i,j)])
    
    for colo in range(len(coloring)):
         pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(coloring[colo][0][0]+coloring[colo][1],coloring[colo][0][1]-5, 10, 10))
    
    pygame.display.update()
    