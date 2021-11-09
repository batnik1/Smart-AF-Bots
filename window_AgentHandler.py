from window_Util import *      

Number_of_Agents = 1
Number_of_SAgents= 5
Number_of_TAgents=len(truck_resting)
Agents = []
Conveyor_Agents=[]
Sorting_Agents=[]
Truck_Agents=[]
def init_agents():
    for _ in range(Number_of_Agents):
        nAgent=Agent(0,n,m)
        nAgent.CurRack=str((random.randint(0,m-1), random.randint(0,n-1), random.randint(0, 4), random.randint(0, 4)))
        nAgent.position=numofrack[nAgent.CurRack]
        Agents.append(nAgent)

    for _ in range(Number_of_SAgents):
        nAgent=Agent(2,n,m)
        nAgent.color=colors.PALEGREEN
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

def get_direction(a,b):
    x1,y1=a
    x2,y2=b
    if a==b:
        return "rest"
    if x1==x2:
        if y1<y2:
            return "down"
        else:
            return "up"
    elif y1==y2:
        if x1<x2:
            return "right"
        else:
            return "left"
    else:
        print("Dead Direction Kid")
    
def handle_rack_agents(coloring, key):
    
    for agent in Agents:
        #print(10*heat_value(agent.position,0,Agents,Truck_Agents,Sorting_Agents))
        if agent.waitingperiod>0:
            agent.waitingperiod-=1
        if agent.cStation!=-1 and agent.position==charging_loc[agent.cStation] and abs(agent.charge-200)<=1:
            charging_state[agent.cStation]=0
            agent.cStation=-1
            agent.color = colors.LIGHTBLUE1
            agent.size = 4
            agent.needcharge=False
            agent.goals=[numofrack[agent.CurRack],[-200,-200]]
            agent.nearestgoals=[]
            agent.goalindex=0
            agent.direction="motion"
            for xx in range(len(agent.goals)):
                if agent.goals[xx][0]<0:
                    agent.nearestgoals.append(agent.goals[xx])
                    continue
                togoal=agent.goals[xx]
                nearestIntersec=nearest_intersection(togoal,rev=True) 
                agent.nearestgoals.append(nearestIntersec)
            
        if agent.Index <= -1 and agent.direction=="rest":
            if agent.needcharge==True:
                agent.color = colors.GREEN
                agent.charge+=.1

            if agent.charge<20 and agent.needcharge == False:
                charge_ind,charge_box=get_charging()
                if charge_box==-1:
                    continue
                agent.color = colors.LIGHTBLUE1
                agent.cStation=charge_ind
                agent.needcharge=True
                agent.direction="motion"
                agent.goals=[charge_box,[-11,-11]]
                agent.nearestgoals=[]
                agent.goalindex=0
                for xx in range(len(agent.goals)):
                    if agent.goals[xx][0]<0:
                        agent.nearestgoals.append(agent.goals[xx])
                        continue
                    togoal=agent.goals[xx]
                    nearestIntersec=nearest_intersection(togoal,rev=True) 
                    agent.nearestgoals.append(nearestIntersec)

                agent.Wait = False

        if agent.changelane==1:
            agent.changelane=0
            agent.Path=[]
            agent.Index=-1

        if agent.Index>=0:
            agent.charge-=0.05
            agent.position = (agent.Path[agent.Index][0], agent.Path[agent.Index][1])
            agent.Index-=1
            if agent.waitingperiod==0 and Intersec_dic[(agent.position[0],agent.position[1])]==1:
                heating=heat_value(agent.position,0,Agents,Truck_Agents,Sorting_Agents)
                heating*=100
                if heating<12:
                    agent.color = colors.LIGHTBLUE1
                elif heating<20:
                    agent.color = colors.YELLOW1
                else:
                    agent.color = colors.RED1
                    agent.changelane=1
                    agent.waitingperiod=15
              
        elif agent.direction!="rest":
            
            if agent.position==agent.goals[agent.goalindex]:
                agent.goalindex+=1
                
            if agent.goalindex<len(agent.goals):
                if agent.goals[agent.goalindex]==[-7,-7]:
                    # logger.info('Bot '+str(agent.ind)+': Reached the Desired Rack')
                    logger.info('Order'+','+str(agent.order_id)+','+'Warehouse'+','+str(agent.ind)+','+'Bot Reached the Desired Rack.')
                    
                    agent.goalindex+=1
                    
                elif agent.goals[agent.goalindex]==[-14,-14]:
                    # logger.info('Bot'+','+str(agent.ind)+': Reached the Human Counter with items '+str(agent.items_carrying))
                    logger.info('Order'+','+str(agent.order_id)+','+'Warehouse'+','+str(agent.ind)+','+'Bot Reached the Human Counter with few items.')
                    doc=order_db.find_one({"_id":agent.order_id})
                    quantity=doc["ordered_quantity"]
                    progress=doc["order_progress"]
                    human_ct=doc["human_counter"]
                    total_items_carrying=0
                    for items in agent.items_carrying:
                        total_items_carrying+=items[1]
                    if total_items_carrying+progress==quantity:
                        # logger.info("Order "+str(doc['_id'])+" is finished")
                        logger.info('Finished Order'+','+str(agent.order_id)+','+'Warehouse'+','+str(agent.ind)+','+'Order is completed.')
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
                    agent.goalindex+=1
                elif  agent.goals[agent.goalindex]==[-21,-21]:
                    # logger.info('Bot '+str(agent.ind)+': Kept the Rack back which I was carrying')
                    logger.info('Event'+','+'-'+','+'Warehouse'+','+str(agent.ind)+','+'Kept the Rack back which it was carrying.')
                    agent.direction="rest"
                    agent.goals=[]
                    agent.nearestgoals=[]
                    agent.goalindex=0
                    agent.Index=-1
                    rack_available[agent.CurRack]=1
                    agent.Wait = True
                    agent.color = colors.YELLOW1
                    agent.size=2
                    pygame.draw.circle(screen, agent.color, agent.position, agent.size)
                    
                    remove=[]
                    for colo in range(len(coloring)):
                        if coloring[colo][2]==agent:
                            remove.append(coloring[colo])
                    for i in remove:
                        coloring.remove(i)
                    continue
                elif agent.goals[agent.goalindex]==[-11,-11]:
                    # logger.info('Bot '+str(agent.ind)+': Reached the Charging Station')
                    logger.info('Charging'+','+'-'+','+'Warehouse'+','+str(agent.ind)+','+'Bot Reached the Charging Station.')
                    agent.size=2
                    agent.direction="rest"
                    agent.goals=[]
                    agent.nearestgoals=[]
                    agent.goalindex=0
                    agent.Index=-1
                    pygame.draw.circle(screen, agent.color, agent.position, agent.size)
                    continue
                elif agent.goals[agent.goalindex]==[-200,-200]:
                    # logger.info('Bot '+str(agent.ind)+': Reached back to its rack with full Charge')
                    logger.info('Charging'+','+'-'+','+'Warehouse'+','+str(agent.ind)+','+'Bot Reached back to its Rack with full Charge.')
                    agent.direction="rest"
                    agent.goals=[]
                    agent.nearestgoals=[]
                    agent.goalindex=0
                    agent.Index=-1
                    agent.color = colors.YELLOW1
                    agent.size=2
                    agent.Wait=True
                    pygame.draw.circle(screen, agent.color, agent.position, agent.size)
                    continue
                        
            if agent.position in Intersections:
                togoal=agent.goals[agent.goalindex]
                nearestIntersec=agent.nearestgoals[agent.goalindex] 
                if agent.position==nearestIntersec:       # Goal is very near to this
                    agent.Path=nearest_intersection_path(agent.position,togoal)
                    agent.direction="motion"
                    agent.Index=len(agent.Path)-1
                else:
                    nAgent = Search(agent.position,nearestIntersec)
                    nAgent.AStar(Agents,Truck_Agents,Sorting_Agents)
                    # nextIntersec=nAgent.getPath()
                    agent.direction="motion"
                    # agent.Path=nearest_intersection_path(agent.position,nextIntersec)
                    # agent.Index=len(agent.Path)-1

                    nextIntersec_path=nAgent.getPathLong()
                    nextIntersec_path.reverse()
                    path_temp1=[]

                    for i in range(len(nextIntersec_path)-1):
                        temp2=nearest_intersection_path(nextIntersec_path[i],nextIntersec_path[i+1])
                        temp2.reverse()
                        path_temp1+=temp2
                    agent.Path=path_temp1
                    agent.Index=len(agent.Path)-1   
                    
            else:
                nearestIntersec=nearest_intersection(agent.position) 
                agent.Path=nearest_intersection_path(agent.position,nearestIntersec)
                agent.direction="motion"
                agent.Index=len(agent.Path)-1

            agent.position = (agent.Path[agent.Index][0], agent.Path[agent.Index][1])
        

        pygame.draw.circle(screen, agent.color, agent.position, agent.size)

def handle_conveyor_belt(sorting_orders):
    removing_conveyor=[]
    for i in range(len(Conveyor_Agents)):
        conveyor_agent=Conveyor_Agents[i]
        if conveyor_agent.position==(racks_width,(80+racks_height//2)//2+20):
            # logger.info("Conveyor Belt Moved Order with ID :"+str(conveyor_agent.order_id)+" to the Sorting Area")
            logger.info('Conveyor Belt'+','+str(conveyor_agent.order_id)+','+'Conveyor Belt'+','+'-'+','+'Shifted Order to the Sorting Area.')
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
        # logger.info("Sorting Bot is moving order with Order ID: "+str(sorder)+" to it's dumping point")
        logger.info('Sorting Order'+','+str(sorder)+','+'Sorting Bot'+','+str(ind)+','+"Bot is moving order to it's dumping point.")
        agent.ind=ind
        #sorting_bots.insert_one({"_id":ind,"Order_ID":order_id})
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
        agent.size = 4
        agent.order_id=sorder       
              
    for ind in finished_sorder:
        sorting_orders.remove(ind)
    finished_sorder.clear()
    for sagent in Sorting_Agents:
       # print(100*heat_value(sagent.position,1,Agents,Truck_Agents,Sorting_Agents))
        if sagent.waitingperiod>0:
            sagent.waitingperiod-=1

        if sagent.changelane==1:
                sagent.changelane=0
                sagent.Index=-1
                sagent.Path=[]

        if sagent.Index>=0: 
            sagent.position = (sagent.Path[sagent.Index][0], sagent.Path[sagent.Index][1])
            sagent.Index-=1
            if sagent.waitingperiod==0 and Intersec_dic[(sagent.position[0],sagent.position[1])]==1 and 100*heat_value(sagent.position,1,Agents,Truck_Agents,Sorting_Agents)>16:
                print("changing Lanes")
                sagent.changelane=1
                sagent.waitingperiod=10
                
        elif sagent.direction!="rest":
            if sagent.position==sagent.goals[sagent.goalindex]:
                sagent.goalindex+=1
            if sagent.goalindex<len(sagent.goals):
                if sagent.goals[sagent.goalindex]==[-7,-7]:
                    sagent.goalindex+=1
                elif  sagent.goals[sagent.goalindex]==[-14,-14]:
                    # logger.info("Sorting Bot dumped the order with Order ID: "+str(sagent.order_id)+" to it's dumping point")
                    logger.info('Sorting Order'+','+str(sagent.order_id)+','+'Sorting Bot'+','+str(sagent.ind)+','+"Bot placed the order to it's dumping point.")
                    sagent.Wait=True       
                    sagent.Path=[]
                    sagent.size=2
                    # sagent.color=colors.PALEGREEN
                    sagent.direction="rest"
                    sagent.goals=[]
                    sagent.nearestgoals=[]
                    sagent.goalindex=0
                    sagent.Index=-1
                    pygame.draw.circle(screen, sagent.color, sagent.position, sagent.size)

                    continue
            
            if sagent.position in Intersections:
                togoal=sagent.goals[sagent.goalindex]
                nearestIntersec=sagent.nearestgoals[sagent.goalindex] 
                if sagent.position==nearestIntersec:       # Goal is very near to this
                   sagent.Path=nearest_intersection_path(sagent.position,togoal)
                   sagent.direction="motion"
                   sagent.Index=len(sagent.Path)-1
                else:
               #     print('else',agent.nearestgoals)    
                    nAgent = Search(sagent.position,nearestIntersec)
                    nAgent.AStar(Agents,Truck_Agents,Sorting_Agents)
                    sagent.direction="motion"
                    # nextIntersec=nAgent.getPath()
                    #sagent.Path=nearest_intersection_path(agent.position,nextIntersec)
                    #sagent.Index=len(agent.Path)-1
                    nextIntersec_path=nAgent.getPathLong()
                    nextIntersec_path.reverse()
                    path_temp1=[]
                    #print(nextIntersec_path)
                    for i in range(len(nextIntersec_path)-1):
                        temp2=nearest_intersection_path(nextIntersec_path[i],nextIntersec_path[i+1])
                        # print(temp2)
                        # print(type(temp2),type(path_temp1))
                        temp2.reverse()
                        path_temp1+=temp2
                    sagent.Path=path_temp1
                    sagent.Index=len(sagent.Path)-1     
            else:
                nearestIntersec=nearest_intersection(sagent.position) 
               # print(agent.position,nearestIntersec)
                sagent.Path=nearest_intersection_path(sagent.position,nearestIntersec)
                sagent.direction="motion"
                sagent.Index=len(sagent.Path)-1
            if sagent.Index!=-1:
                sagent.position = (sagent.Path[sagent.Index][0],sagent.Path[sagent.Index][1])
        pygame.draw.circle(screen, sagent.color, sagent.position, sagent.size)


def handle_truck_agents():
    for agent in Truck_Agents:
        # print(100*heat_value(agent.position,2,Agents,Truck_Agents,Sorting_Agents))
        if agent.waitingperiod>0:
            agent.waitingperiod-=1

        if agent.changelane==1:
                agent.changelane=0
                agent.Index=-1
                agent.Path=[]

        if agent.Index>=0:
            agent.position = (agent.Path[agent.Index][0], agent.Path[agent.Index][1])
            agent.Index-=1
            if agent.waitingperiod==0 and Intersec_dic[(agent.position[0],agent.position[1])]==1 and 100*heat_value(agent.position,2,Agents,Truck_Agents,Sorting_Agents)>11:
              #  print("changing Lanes")
                agent.changelane=1
                agent.waitingperiod=10
            
        elif agent.direction!="rest":
            if agent.position==agent.goals[agent.goalindex]:
                agent.goalindex+=1
            if agent.goalindex<len(agent.goals):
                if agent.goals[agent.goalindex]==[-7,-7]:
                    agent.goalindex+=1
                    add_item(agent.items_carrying[0],agent.items_carrying[1],agent.CurRack)
                    # logger.info('Truck Bot '+str(agent.ind)+': Reached the Desired Rack with item type'+str(agent.items_carrying[0])+' with quant '+str(agent.items_carrying[1]))
                    logger.info('Trucks in Warehouse'+','+'-'+','+'Truck Bot'+','+'-'+','+"Reached the Desired Rack with some new item type.")
                elif  agent.goals[agent.goalindex]==[-14,-14]:
                    agent.Path = []
                    rack_available[agent.CurRack]=1
                    agent.Wait = True   
                    agent.size=2
                    agent.direction="rest"
                    agent.goals=[]
                    agent.nearestgoals=[]
                    agent.goalindex=0
                    agent.Index=-1
                    pygame.draw.circle(screen, agent.color, agent.position, agent.size)
                    continue

            if agent.position in Intersections:
                togoal=agent.goals[agent.goalindex]
                nearestIntersec=agent.nearestgoals[agent.goalindex] 
                if agent.position==nearestIntersec:       # Goal is very near to this
                    agent.Path=nearest_intersection_path(agent.position,togoal)
                    agent.direction="motion"
                    agent.Index=len(agent.Path)-1
                else:
               #     print('else',agent.nearestgoals)    
                    nAgent = Search(agent.position,nearestIntersec)
                    nAgent.AStar(Agents,Truck_Agents,Sorting_Agents)
                    agent.direction="motion"
                    # nextIntersec=nAgent.getPath()
                    # agent.Path=nearest_intersection_path(agent.position,nextIntersec)
                    # agent.Index=len(agent.Path)-1
                    nextIntersec_path=nAgent.getPathLong()
                    nextIntersec_path.reverse()
                    path_temp1=[]
                    #print(nextIntersec_path)
                    for i in range(len(nextIntersec_path)-1):
                        temp2=nearest_intersection_path(nextIntersec_path[i],nextIntersec_path[i+1])
                        # print(temp2)
                        # print(type(temp2),type(path_temp1))
                        temp2.reverse()
                        path_temp1+=temp2
                    agent.Path=path_temp1
                    agent.Index=len(agent.Path)-1     
            else:
                nearestIntersec=nearest_intersection(agent.position) 
               # print(agent.position,nearestIntersec)
                agent.Path=nearest_intersection_path(agent.position,nearestIntersec)
                agent.direction="motion"
                agent.Index=len(agent.Path)-1

            agent.position = (agent.Path[agent.Index][0], agent.Path[agent.Index][1])

        pygame.draw.circle(screen, agent.color, agent.position, agent.size)