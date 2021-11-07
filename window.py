from window_OrderHandler import *

running = 1
key=0
paused=0
order_freq=50
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
    
    # for i in range(len(new_praylist)):
    #     pygame.draw.circle(screen, (0, 255, 0), (new_praylist[i][0], new_praylist[i][1]), 2)    
    
    handle_orders()
    handle_Torders()
    handle_events()
    handle_rack_agents(coloring,key)
    handle_conveyor_belt(sorting_orders)
    handle_sorting_agents(sorting_orders)
    handle_truck_agents()
    key+=1
    for colo in range(len(coloring)):
         pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(coloring[colo][0][0]+coloring[colo][1],coloring[colo][0][1]-5, 10, 10))
    pygame.display.update()