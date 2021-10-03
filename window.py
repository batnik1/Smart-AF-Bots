from window_OrderHandler import *

running = True
orders=[]
Torders=[]
sorting_orders=[]
loading_truck = 0
loading_truck_boxes = 10
key=0
coloring=[]
paused=False
order_freq=10
truck_freq=500
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
    
while running:
    if key%order_freq==0:
        new_orders=gen_a_order()    # new_orders= (racks,human_counter,order_id)    
        if new_orders!="Nothing":
            orders.append(new_orders)   # To mantain FCFS Order
    if key%truck_freq==0:
        new_items=truck_orders()
        Torders+=new_items

    init_screen()
    handle_orders(orders,coloring)
    handle_Torders(Torders)
    handle_events()
    handle_rack_agents(coloring,key)
    handle_conveyor_belt(sorting_orders)
    handle_sorting_agents(sorting_orders)
    key+=1
    for colo in range(len(coloring)):
         pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(coloring[colo][0][0]+coloring[colo][1],coloring[colo][0][1]-5, 10, 10))
    pygame.display.update()