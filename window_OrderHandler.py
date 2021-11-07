from window_AgentHandler import *
orders=[]
Torders=[]
sorting_orders=[]
coloring=[]
def handle_orders():
    finished=[]
    for i in range(len(orders)):
        list_racks = orders[i][0]
        hCounter=orders[i][1]
        order_id=orders[i][2]
        count=0
        finished_racks=[]
        for rack in list_racks:    
            if rack_available[rack]!=1:
                continue

            rack_location=numofrack[rack]
            ind = get_Agent(rack_location)
            if ind == -1:
                break
            rack_available[rack]=0
            agent=Agents[ind]
            logger.info('Bot '+str(ind)+" is assigned to go to Rack "+str(rack))
            
            agent.ind=ind
            agent.goals=[rack_location,[-7,-7],numofhcounter[str((int(hCounter/m), hCounter % m))],[-14,-14],rack_location,[-21,-21]]
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
            finished_racks.append(rack)
            #TODO : Speed up this

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

def truck_orders():
    items=[]
    for _ in range(len(Truck_Agents)):
        type=random.randint(0,type_of_items)
        quantity=random.randint(1,3)
        shelf=str((random.randint(0, m-1), random.randint(0,n-1), random.randint(0, 4), random.randint(0, 4)))
        items.append([type,quantity,shelf])
    return items

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
        logger.info('Truck Bot '+str(ind)+" is assigned to deliever item type "+str(type)+" whose quant is "+str(quantity))
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


