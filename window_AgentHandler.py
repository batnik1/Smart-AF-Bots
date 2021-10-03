from window_Util import *      

Number_of_Agents = 10
Number_of_SAgents= 10
Number_of_TAgents=len(truck_resting)
Agents = []
Conveyor_Agents=[]
Sorting_Agents=[]
Truck_Agents=[]
def init_agents():
    for _ in range(Number_of_Agents):
        nAgent=Agent(0,n,m)
        nAgent.position=numofrack[nAgent.CurRack]
        Agents.append(nAgent)
    for _ in range(Number_of_SAgents):
        nAgent=Agent(2,n,m)
        sorting_random=(random.randint(0,2*sorting_n-1),random.randint(0,2*sorting_m-1))
        nAgent.position=numofdump[str(sorting_random)]
        Sorting_Agents.append(nAgent)
    for i in range(Number_of_TAgents):
        nAgent=Agent(1,n,m)
        nAgent.truck_rest=i
        nAgent.position=truck_resting[i]
        Truck_Agents.append(nAgent)

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

def get_TAgent():
    for i in range(len(Truck_Agents)):
        if Truck_Agents[i].Wait==True:
            return i
    return -1

def handle_rack_agents(coloring,key):
    for agent in Agents:
        if agent.cStation!=-1 and agent.position==charging_loc[agent.cStation] and agent.charge==200:
            charging_state[agent.cStation]=0
            agent.cStation=-1
            agent.color = colors.LIGHTBLUE1
            agent.size = 4
            agent.needcharge=False
            nAgent = Search(agent.position,numofrack[agent.CurRack])
            nAgent.BFS()
            agent.Path = nAgent.getPath()
            agent.Path.reverse()
            agent.Index = len(agent.Path)
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
                logger.info('Bot '+str(agent.ind)+': Reached the Desired Rack')
            elif agent.Path[agent.Index]==[-14,-14]:
                logger.info('Bot '+str(agent.ind)+': Reached the Human Counter with items '+str(agent.items_carrying))
                doc=order_db.find_one({"_id":agent.order_id})
                quantity=doc["ordered_quantity"]
                progress=doc["order_progress"]
                human_ct=doc["human_counter"]
                total_items_carrying=0
                for items in agent.items_carrying:
                    total_items_carrying+=items[1]
                if total_items_carrying+progress==quantity:
                    logger.info("Order "+str(doc['_id'])+" is finished")
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
                logger.info('Bot '+str(agent.ind)+': Kept the Rack back which I was carrying')
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

def handle_conveyor_belt(sorting_orders):
    removing_conveyor=[]
    for i in range(len(Conveyor_Agents)):
        conveyor_agent=Conveyor_Agents[i]
        if conveyor_agent.position==(racks_width,(80+racks_height//2)//2+20):
            logger.info("Conveyor Belt Moved Order with ID :"+str(conveyor_agent.order_id)+" to the Sorting Area")
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

def handle_sorting_agents(sorting_orders):
    finished_sorder=[]
    for sorder in sorting_orders:
        ind = get_SAgent(numofdump["conveyor"])
        if ind == -1:
            break
        agent=Sorting_Agents[ind]
        logger.info("Sorting Bot is moving order with Order ID: "+str(sorder)+" to it's dumping point")
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
            logger.info("Sorting Bot dumped the order with Order ID: "+str(sagent.order_id)+" to it's dumping point")
            sagent.Wait=True       
            sagent.Path=[]
            sagent.color=colors.PALEGREEN
        pygame.draw.circle(screen, sagent.color, sagent.position,4)

def handle_truck_agents():
    for agent in Truck_Agents:
        agent.Index -= 1
        if agent.Index >= 0:        
            if agent.Path[agent.Index]==[-7,-7]:
                agent.Index -= 1
                add_item(agent.items_carrying[0],agent.items_carrying[1],agent.CurRack)
                logger.info('Truck Bot '+str(agent.ind)+': Reached the Desired Rack with item '+str(agent.items_carrying[0])+'with count '+str(agent.items_carrying[1]))
            else: 
                agent.position = (agent.Path[agent.Index][0], agent.Path[agent.Index][1])
        if agent.Index == -1:
                agent.Path = []
                rack_available[agent.CurRack]=1
                agent.Wait = True   
                agent.size=2
        pygame.draw.circle(screen, agent.color, agent.position, agent.size)