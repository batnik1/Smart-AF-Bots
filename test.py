import AStar
from Agent007 import Agent
import random
import pygame
from final_run import *
from Orders import *
import collections
pygame.init()
screen = pygame.display.set_mode(
    (display_width, display_height))  # create screen
import time
import operator

dir = [(-1, -1), (0, -1), (0, 1), (1, 0), (-1, 0)]      # (-1,-1) is just pushed to make it 1 based indexing


def ManhattanDistance(start, end):
    return abs(start[0]-end[0])+abs(start[1]-end[1])

agent_color = colors.LIGHTBLUE1


HCtoConveyor={}
def initHCtoConveyor():
    x=130
    for i in range(2*m):
        if i==m:
            x=130
        if i<m:
            HCtoConveyor[i]=(x,15)
        else:
            HCtoConveyor[i]=(x, racks_height-5)    
        x+=120
        

def make_sorting_area():
    sorting_w=sorting_m*60+20
    sorting_h=sorting_n*60+20
    pygame.draw.rect(screen,colors.BLUE,pygame.Rect(racks_width,80,sorting_w,sorting_h),3)
    pygame.draw.line(screen,colors.BLUE,(racks_width,(80+racks_height//2)/2-25),(racks_width-25,(80+racks_height//2)/2-25),width=2)    # Left
    pygame.draw.line(screen,colors.BLUE,(racks_width-25,(80+racks_height//2)/2+20),(racks_width,(80+racks_height//2)/2+20),width=2)    # Right
    pygame.draw.line(screen,colors.BLUE,(racks_width-25,(80+racks_height//2)/2-25),(racks_width-25,(80+racks_height//2)/2+20),width=2)             #Down

    # (n+1)*15+n*10=sorting_n*100+15
    # (m+1)*15+m*10=sorting_m*100+15
    x=racks_width+20

    for _ in range(int(2*sorting_m)):
       y=100
       for _ in range(int(2*sorting_n)):
           make_rect(x, y,colors.PURPLE3)
           y+=30
       x+=30  
    x=racks_width+10
    y=80
    for i in range(2*sorting_m+1):
        pygame.draw.line(screen, colors.BLUE, (x, 80),(x,sorting_h+80),2)
        x+=30
    for i in range(2*sorting_n+1):
        pygame.draw.line(screen, colors.BLUE, (racks_width, y+10),(racks_width+sorting_w,y+10),2)
        y+=30
    # for _ in range(0,n//2):
    #     x = racks_width+10
    #     for _ in range(0,m//2):
    #         for i in range(x, x+100, 20):
    #             for j in range(y, y+100, 20):
    #                 make_rect(i, j)
    #         x += 120
    #     y += 120
         

def conveyor():
    pygame.draw.line(screen, colors.GREEN, (130, 0), (racks_width, 0))
    pygame.draw.line(screen, colors.GREEN, (130, racks_height+10), (racks_width, racks_height+10),width=2)
    x=130
    for i in range(m):
        pygame.draw.line(screen, colors.GREEN, (x, 0), (x, 15),width=10)
        pygame.draw.line(screen, colors.GREEN, (x, racks_height+10), (x,racks_height-5 ),width=10)
        x+=120
    
    pygame.draw.line(screen, colors.GREEN, (racks_width, 0), (racks_width, racks_height+10),width=2)
    
    


def make_rect(x, y,color=(255,0,0)):
    pygame.draw.rect(screen,color, pygame.Rect(x, y, 10, 10))


def make_line(x, y, color):
    if x:
        pygame.draw.line(screen, color, (x, 80), (x, racks_height-70))
    elif y:
        pygame.draw.line(screen, color, (80, y), (racks_width-70, y))

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


def draw_rack_lines(x, y,color=colors.ORANGE):
    pygame.draw.line(screen, color, (x+15, y-10), (x+15, y+100))  # up
    pygame.draw.line(screen, color, (x+55, y-10), (x+55, y+100))  # up
    pygame.draw.line(screen, color,
                     (x+35, y-10), (x+35, y+100))  # down
    pygame.draw.line(screen, color,
                     (x+75, y-10), (x+75, y+100))  # down

    pygame.draw.line(screen, color, (x-10, y+15),
                     (x+100, y+15))  # right
    pygame.draw.line(screen, color, (x-10, y+55),
                     (x+100, y+55))  # right
    pygame.draw.line(screen, color,
                     (x-10, y+35), (x+100, y+35))  # left
    pygame.draw.line(screen, color,
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


charging_state={}
charging_loc={}
charging_state_list=[]
def build_charge_dict():
    counting=-1
    for i in range((n//2+n % 2)*100+20,racks_height-90,10):
        counting+=1
        charging_state_list.append(counting)
        charging_state[counting]=0
        charging_loc[counting]=(55,i)
      #  pygame.draw.line(screen, colors.ORANGE, (30, i), (80, i))   
build_charge_dict()
def build_charging_zone():
    for i in range((n//2+n % 2)*100+20,racks_height-90,10):
        pygame.draw.line(screen, colors.ORANGE, (30, i), (80, i))    


def build_charging_lines():
    pygame.draw.line(screen, colors.ORANGE, (80, (n//2+n % 2)*100+10), (30, (n//2+n % 2)*100+10))
    pygame.draw.line(screen, colors.ORANGE, (80, racks_height-90), ((30, racks_height-90)))
    pygame.draw.line(screen, colors.ORANGE, (30, (n//2+n % 2)*100+10), (30, racks_height-90))

def get_charging():
    for i in range(len(charging_state_list)):
        if charging_state[i]==0:
            charging_state[i]=1
            return i,charging_loc[i]
    return -1,-1
              
        
running = True

Number_of_Agents = 100
Number_of_SAgents= 50
Agents = []
Conveyor_Agents=[]
Sorting_Agents=[]
for i in range(Number_of_Agents):
    nAgent=Agent(0,n,m)
    nAgent.position=numofrack[nAgent.CurRack]
    Agents.append(nAgent)
for i in range(Number_of_SAgents):
    nAgent=Agent(2,n,m)
    sorting_random=(random.randint(0,2*sorting_n-1),random.randint(0,2*sorting_m-1))
    nAgent.position=numofdump[str(sorting_random)]
    Sorting_Agents.append(nAgent)
    
    


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
        d=ManhattanDistance(rack_pos, agent.position)
        if agent.Wait == True and mindis>d and 10*agent.charge>=d:
            mindis=d

    for i in range(len(Agents)):
        if Agents[i].Wait==True:
            if mindis==ManhattanDistance(rack_pos, Agents[i].position) and 10*Agents[i].charge>=d:
                return i
    return -1

def get_SAgent(rack_pos):
    mindis=99999999999999999
    for agent in Sorting_Agents:
        if agent.Wait == True and mindis>ManhattanDistance(rack_pos, agent.position):
            mindis=ManhattanDistance(rack_pos, agent.position)

    for i in range(len(Sorting_Agents)):
        if Sorting_Agents[i].Wait==True:
            if mindis==ManhattanDistance(rack_pos, Sorting_Agents[i].position):
                return i
    return -1


orders=[]
sorting_orders=[]
loading_truck = 0
loading_truck_boxes = 10
key=0
coloring=[]
paused=False

initHCtoConveyor()






while running:
    #time.sleep(0.02)
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
    
    if key%10==0:
        new_orders=gen_a_order()    # new_orders= (racks,human_counter,order_id)    
        if new_orders!="Nothing":
            orders.append(new_orders)   # To mantain FCFS Order
    
    finished=[]
    for i in range(len(orders)):
        list_racks = orders[i][0]
        hCounter=orders[i][1]
        order_id=orders[i][2]
        count=0
        finished_racks=[]
        for rack in list_racks:    
            if rack_available[rack]!=1:
                # print('Skipped (not aval)',rack)
                continue

            rack_location=numofrack[rack]
            ind = get_Agent(rack_location)
           # print(ind)
            if ind == -1:
                break
            rack_available[rack]=0
            agent=Agents[ind]
            # logger.info('Bot '+str(ind)+" is assigned to go to Rack "+str(rack))
            agent.ind=ind
            # bot_db.insert_one({"_id":ind,"Order_ID":order_id,"Rack":rack,"Items":list_racks[rack],"target":[hCounter]})
            nAgent = Search(agent.position,rack_location)
            # nAgent = Search(agent.position,charging_loc[4])
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

    # for i in range(2*sorting_m):
    #     for j in range(2*sorting_n):
    #         pygame.draw.circle(screen, colors.WHITE, numofdump[str((j,i))],6)


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
    conveyor()
    build_charging_lines()
    build_charging_zone()
    make_sorting_area()
    
    for agent in Agents:
        if agent.cStation!=-1 and agent.position==charging_loc[agent.cStation] and agent.charge==100:
            charging_state[agent.cStation]=0
            agent.cStation=-1
            agent.color = colors.LIGHTBLUE1
           # agent.Wait = True
            agent.size = 4
            agent.needcharge=False
            nAgent = Search(agent.position,numofrack[agent.CurRack])
            nAgent.BFS()
            agent.Path = nAgent.getPath()
            agent.Path.reverse()
            agent.Index = len(agent.Path)
            print(agent.Index,"lo")
        if agent.Index==2:                      # Coloring Racks 
            remove=[]
            for colo in range(len(coloring)):
                if coloring[colo][0]==agent.CurRack:
                    remove.append(coloring[colo])
            for i in remove:
                coloring.remove(i)
        agent.Index -= 1
        if agent.Index >= 0:
            if  agent.Index%20==0:
                agent.charge-=1
                
            if agent.Path[agent.Index]==[-7,-7]:
                agent.Index -= 1
                # logger.info('Bot '+str(agent.ind)+': Reached the Desired Rack')
            elif agent.Path[agent.Index]==[-14,-14]:
                # logger.info('Bot '+str(agent.ind)+': Reached the Human Counter with items '+str(agent.items_carrying))
                doc=order_db.find_one({"_id":agent.order_id})
                quantity=doc["ordered_quantity"]
                progress=doc["order_progress"]
                human_ct=doc["human_counter"]
                total_items_carrying=0
                for items in agent.items_carrying:
                    total_items_carrying+=items[1]
                if total_items_carrying+progress==quantity:
                    # logger.info("Order "+str(doc['_id'])+" is finished")
                    # delivered.insert_one({"_id":doc["_id"],"dumping_rack":sorting_random,"dumped":False})
                    conveyor_agent= Agent(1,n,m)
                    conveyor_agent.position=HCtoConveyor[human_ct]
                    conveyor_agent.order_id=agent.order_id
                    if human_ct<m:
                        conveyor_agent.Path=HCtoSorting[str((0,human_ct))].copy()
                    else:
                        conveyor_agent.Path=HCtoSorting[str((1,human_ct-m))].copy()
                    # conveyor_agent.Path+=Sorting_Counter[0].getBFSPath(numofdump[str(sorting_random)])
                    conveyor_agent.Path.reverse()
                    conveyor_agent.Index=len(conveyor_agent.Path)
                    Conveyor_Agents.append(conveyor_agent)

                order_db.update_one({"_id":agent.order_id},{"$inc":{"order_progress":total_items_carrying}})
                agent.Index -= 1
            elif agent.Path[agent.Index]==[-21,-21]:
                # logger.info('Bot '+str(agent.ind)+': Kept the Rack back which I was carrying')
                agent.Index -= 1
            else: 
                agent.position = (agent.Path[agent.Index][0], agent.Path[agent.Index][1])
        if agent.Index <= -1:
            if agent.needcharge==False:
                agent.Path = []
                rack_available[agent.CurRack]=1
                agent.Wait = True
                agent.color = colors.YELLOW1
            else:
                agent.size = 2
                agent.color = colors.GREEN
                if key%10==0:
                    agent.charge+=1

            if agent.charge<20 and agent.needcharge == False:
                charge_ind,charge_box=get_charging()
                if charge_box==-1:
                    continue
                agent.cStation=charge_ind
                agent.needcharge=True
                nAgent = Search(agent.position,charge_box)
                nAgent.BFS()
                agent.Path = nAgent.getPath()
                agent.Path.reverse()
                agent.Index = len(agent.Path)
                agent.Wait = False
                agent.size=2
                # TODO: Send it to charging station
            remove=[]
            for colo in range(len(coloring)):
                if coloring[colo][2]==agent:
                    remove.append(coloring[colo])
            for i in remove:
                coloring.remove(i)
        pygame.draw.circle(screen, agent.color, agent.position, agent.size)
    
    removing_conveyor=[]
    for i in range(len(Conveyor_Agents)):
        conveyor_agent=Conveyor_Agents[i]
        # if conveyor_agent.position==(racks_width,(80+racks_height//2)//2+20):
            # logger.info("Conveyor Belt Moved Order with ID :"+str(conveyor_agent.order_id)+" to the Sorting Area")
        conveyor_agent.Index-=1
        if conveyor_agent.Index>=0:
            conveyor_agent.position = (conveyor_agent.Path[conveyor_agent.Index][0], conveyor_agent.Path[conveyor_agent.Index][1])
        if conveyor_agent.Index==-1:
            sorting_orders.append(conveyor_agent.order_id)          
            conveyor_agent.Path=[]
            removing_conveyor.append(i)
            conveyor_agent.color=colors.PALEGREEN
        pygame.draw.circle(screen, conveyor_agent.color, conveyor_agent.position,4)
    for ind in removing_conveyor:
        Conveyor_Agents.remove(Conveyor_Agents[ind])
    removing_conveyor.clear()
        
    finished_sorder=[]
    for sorder in sorting_orders:
        ind = get_SAgent(numofdump["conveyor"])
        if ind == -1:
            break
        agent=Sorting_Agents[ind]
        # logger.info("Sorting Bot is moving order with Order ID: "+str(sorder)+" to it's dumping point")
        agent.ind=ind
        #sorting_bots.insert_one({"_id":ind,"Order_ID":order_id})
        address=tuple(order_history.find_one({"_id":sorder})["address"])
        finished_sorder.append(sorder)
        b = Reverse_Sorting_Counter[0].getBFSPath(agent.position)     # From that Rack to Counter
        c = Sorting_Counter[0].getBFSPath(numofdump[str(address)])
        b.reverse()

        agent.Path =b+c
        agent.Path.reverse()
        agent.Index = len(agent.Path)
        agent.Wait = False
        agent.color = colors.RED1
        agent.size = 4
        agent.order_id=sorder       
              
    for ind in finished_sorder:
        sorting_orders.remove(ind)
    finished_sorder.clear()
    for sagent in Sorting_Agents:
        sagent.Index-=1
        if sagent.Index>=0:
            sagent.position = (sagent.Path[sagent.Index][0], sagent.Path[sagent.Index][1])
        if sagent.Index==-1:  
            # logger.info("Sorting Bot dumped the order with Order ID: "+str(sagent.order_id)+" to it's dumping point")
            sagent.Wait=True       
            sagent.Path=[]
            sagent.color=colors.PALEGREEN
        pygame.draw.circle(screen, sagent.color, sagent.position,4)
    key+=1
    for colo in range(len(coloring)):
         pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(coloring[colo][0][0]+coloring[colo][1],coloring[colo][0][1]-5, 10, 10))

    pygame.display.update()


    """
    1. Charging State vapis 1 bhi krni h
    2. jb robot kuj charge hojaye tb charging station se nikalke kai aur bhejna h    
    """