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
            agent.nearestgoals=[]
            agent.goalindex=0
            for xx in range(len(agent.goals)):
                if agent.goals[xx][0]<0:
                    agent.nearestgoals.append(agent.goals[xx])
                    continue
                togoal=agent.goals[xx]
                nearestIntersec=nearest_intersection(togoal,rev=True)       # Converting Sub Goals from Workspace Domain to Ambient Graph Domain

                agent.nearestgoals.append(nearestIntersec)
             
            agent.direction="motion"
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
        agent=Truck_Agents[ind]
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
        agent.size = 5
        agent.items_carrying=(type,quantity)
        agent.CurRack=rack

    for ind in Tfinished:
        Torders.remove(ind)


