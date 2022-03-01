"""
This file contains functions that assigns order for every type of Agent (Warehouse Agent, Truck Agent , Sorting Agent).
We check for free Agents in any type of order and then assign the bot which is nearest to the Rack which we want to fetch.
State Change of Agent to Motion happens here after the Order Assignment.

"""
from AgentHandler01 import *
orders=[]
Torders=[]
sorting_orders=[]
coloring=[]

def handle_orders():
    finished=[]
    for i in range(len(orders)):        # List of Pending Orders
        list_racks = orders[i][0]
        hCounter=orders[i][1]
        order_id=orders[i][2]
        finished_racks=[]
        for rack in list_racks:    
            if rack_available[rack]!=1: # Rack which we want to fetch is not at it's place and is carried by another agent
                continue
            
            rack_location=numofrack[rack]
            ind = get_Agent(rack_location)  # Get the Index of Agent to which we will assign this Order
            if ind == -1:                   # No Agent is free so we will check later for order assignment
                break
            rack_available[rack]=0
            
            agent=Agents[ind]
            agent.CurRack=rack
            logger.info('Order'+','+str(order_id)+','+'Warehouse'+','+str(ind)+','+'Bot is assigned to go to Rack.')
            agent.ind=ind
            agent.goals=[rack_location,[-7,-7],numofhcounter[str((int(hCounter/m), hCounter % m))],[-14,-14],rack_location,[-21,-21]]   # Goals of the Agent which includes all the sub goals and negative coordinates are just there for logging purposes.
            get_subgoals(agent)
            agent.Index=-1
            finished_racks.append(rack)

            agent.Wait = False
            agent.color = colors.LIGHTBLUE1
            agent.size = 3
            agent.order_id=order_id
            agent.items_carrying=list_racks[rack]
            agent.CurRack=rack
        
            if rack[7]=="0":
                coloring.append((numofrack[rack],10,agent))
            else:
                coloring.append((numofrack[rack],5,agent))
        
        for rack in finished_racks:             # Deleting the racks whose delivery has been done
            orders[i][0].pop(rack)
        if len(orders[i][0])==0:            # All racks associated to one order is finished, then order is complete.
            finished.append(orders[i])      

    for ind in finished:
        try:
            orders.remove(ind)
        except:
            print(finished,ind,len(orders),orders)
    finished.clear()


def handle_orders_SBIG():
    finished=[]
    for i in range(len(orders)):
        list_racks = orders[i][0]
        hCounter=orders[i][1]
        order_id=orders[i][2]
        rack=list(list_racks.keys())[0]
        rack_location=numofrack[rack]
        ind = get_Agent(rack_location)
        if ind == -1:
            continue
        agent=Agents[ind]
        agent.ind=ind
        agent.goals=[]
        for rack in list_racks:
            if rack[7]=="0":
                coloring.append((numofrack[rack],10,agent))
            else:
                coloring.append((numofrack[rack],5,agent))
            agent.goals+=[numofrack[rack]]+[[-2,-2]]
        agent.goals.pop()
        agent.goals.append([-7,-7])
        agent.goals+=[numofhcounter[str((int(hCounter/m), hCounter % m))],[-14,-14],rack_location,[-21,-21]]
        get_subgoals(agent)
        finished.append(orders[i])  
        agent.Index=-1
        agent.Wait = False
        agent.color = colors.LIGHTBLUE1
        agent.size = 3
        agent.order_id=order_id
        agent.items_carrying=list_racks
        agent.CurRack=rack

    
    for ind in finished:
        try:
            orders.remove(ind)
        except:
            print(finished,ind,len(orders),orders)
    finished.clear()    

# This function gives random items with random quantities to Truck Agents to send them to random racks.
def truck_orders():     
    items=[]
    for _ in range(len(Truck_Agents)):
        type=random.randint(0,type_of_items)
        quantity=random.randint(1,max_order_limit)
        shelf=str((random.randint(0, n-1), random.randint(0,m-1), random.randint(0, 4), random.randint(0, 4)))
        items.append([type,quantity,shelf])
    return items
    
# Utility Function - To generate Dummy Sorting Orders so they don't sit idle
def dummy_sorting(key,count):
    for i in range(1,count+1):
        sorting_orders.append('Dummy '+str(key)+'#'+str(i))

# Very Similar to handle_orders() function, this time we are setting the goals for Truck Bots
def handle_Torders():
    Tfinished=[]
    for i in range(len(Torders)):
        type = Torders[i][0]
        quantity=Torders[i][1]
        rack=Torders[i][2]    
        if rack_available[rack]!=1:
            continue
        rack_location=numofrack[rack]
        ind = get_TAgent()
        if ind == -1:
            break
        rack_available[rack]=0
        agent=All_Agents[ind]
        # logger.info('Truck Bot '+str(ind)+" is assigned to deliever item type "+str(type)+" whose quant is "+str(quantity))
        logger.info('New Items'+','+'-'+','+'Truck Bot'+','+str(ind)+','+'Bot is assigned to deliever new items.')
        agent.ind=ind
        Tfinished.append(Torders[i])

        agent.goals=[rack_location,[-7,-7],agent.position,[-14,-14]]
        agent.nearestgoals=[]
        agent.goalindex=0
        for xx in range(len(agent.goals)):
            if agent.goals[xx][0]<0:
                agent.nearestgoals.append(agent.goals[xx])
                continue
            togoal=agent.goals[xx]
            nearestIntersec=nearest_intersection(togoal,rev=True) 

            agent.nearestgoals.append(nearestIntersec)
            
        agent.direction="motion"
        agent.Index=-1
        
        agent.Wait = False
        agent.color = colors.PINK1
        agent.size = 3
        agent.items_carrying=(type,quantity)
        agent.CurRack=rack
        # print(agent.direction,agent.ind)
        # x=input()
    for ind in Tfinished:
        Torders.remove(ind)


def handle_sorting_agents(sorting_orders):
    finished_sorder=[]
    for sorder in sorting_orders:
        ind = get_SAgent(numofdump["conveyor"])
        pygame.draw.circle(screen, colors.RED2, (int(numofdump["conveyor"][0]), int(numofdump["conveyor"][1])), 3)
        if ind == -1:
            break
        agent=All_Agents[ind]
        # logger.info("Sorting Bot is moving order with Order ID: "+str(sorder)+" to it's dumping point")
        logger.info('Sorting Order'+','+str(sorder)+','+'Sorting Bot'+','+str(ind)+','+"Bot is moving order to it's dumping point.")
        agent.ind=ind
        #sorting_bots.insert_one({"_id":ind,"Order_ID":order_id})
        if  sorder[0:3]=='Dum':
            address=(random.randint(0,2*sorting_n-3),random.randint(0,2*sorting_m-3))
        else:
            address=tuple(order_history.find_one({"_id":sorder})["address"])
        finished_sorder.append(sorder)
        agent.goals=[numofdump["conveyor"],[-7,-7],numofdump[str(address)],[-14,-14]]
        agent.nearestgoals=[]
        agent.goalindex=0
        for xx in range(len(agent.goals)):
                if agent.goals[xx][0]<0:
                    agent.nearestgoals.append(agent.goals[xx])
                    continue
                togoal=agent.goals[xx]
                nearestIntersec=nearest_intersection(togoal,rev=True) 
                agent.nearestgoals.append(nearestIntersec)
        agent.direction="motion"
        agent.Index=-1
        agent.Wait = False
        agent.size = 3
        agent.order_id=sorder       
    
    for ind in finished_sorder:
        sorting_orders.remove(ind)
    finished_sorder.clear()
    

def handle_conveyor_belt(sorting_orders):
    removing_conveyor=[]
    for i in range(len(Conveyor_Agents)):
        conveyor_agent=Conveyor_Agents[i]
        if conveyor_agent.position==(racks_width,(80+racks_height//2)//2+20):
            # logger.info("Conveyor Belt Moved Order with ID :"+str(conveyor_agent.order_id)+" to the Sorting Area")
            logger.info('Conveyor Belt'+','+str(conveyor_agent.order_id)+','+'Conveyor Belt'+','+'-'+','+'Shifted Order to the Sorting Area.')
        conveyor_agent.Index-=1
        if conveyor_agent.Index>=0:
            conveyor_agent.position = (conveyor_agent.path[conveyor_agent.Index][0], conveyor_agent.path[conveyor_agent.Index][1])
        if conveyor_agent.Index==-1:
            sorting_orders.append(conveyor_agent.order_id)          
            conveyor_agent.path=[]
            removing_conveyor.append(Conveyor_Agents[i])
            # conveyor_agent.color=colors.PALEGREEN
        pygame.draw.circle(screen, conveyor_agent.color, conveyor_agent.position,4)
    
    for ind in removing_conveyor:
        Conveyor_Agents.remove(ind)
    removing_conveyor.clear()