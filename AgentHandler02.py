from torch import le
from window_Util import *   
from math import *   
Number_of_Agents=config['Number_of_Agents']
Number_of_SAgents= config['Number_of_SAgents']
Number_of_TAgents=len(truck_resting)
Agents = []
Conveyor_Agents=[]
Sorting_Agents=[]
Truck_Agents=[]

random_intersection_flag=config['random_intersection_flag']
epsilon=config['epsilon']
Traffic_Flag=config['Traffic_Flag']


# Used for Initialising our agents of rack/truck/sorting
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

# Get the nearest agent from the rack given

def get_Agent(rack_pos):
    mindis = 99999999999999999
    for agent in Agents:
        d = ManhattanDistance(rack_pos, agent.position)
        if agent.Wait == True and mindis > d and agent.charge > 20:  # 10*agent.charge>=d:TODO: change to charge
            mindis = d

    for i in range(len(Agents)):
        if Agents[i].Wait == True:
            if mindis == ManhattanDistance(rack_pos, Agents[i].position) and Agents[i].charge > 20:
                return i
    return -1


def get_SAgent(rack_pos):
    mindis = 99999999999999999
    for agent in Sorting_Agents:
        if agent.Wait == True and mindis > ManhattanDistance(rack_pos, agent.position):
            mindis = ManhattanDistance(rack_pos, agent.position)

    for i in range(len(Sorting_Agents)):
        if Sorting_Agents[i].Wait == True:
            if mindis == ManhattanDistance(rack_pos, Sorting_Agents[i].position):
                return i
    return -1


def get_TAgent():
    for i in range(len(Truck_Agents)):
        if Truck_Agents[i].Wait == True:
            return i
    return -1

def robo_rack_entry(agent):
    # find nearest intersection 
    First=nearest_intersection((int(agent.position[0]),int(agent.position[1])))                
    # go in back direction from intersection
   
    D=Matrix.grid[int(agent.position[0])][int(agent.position[1])]
    if len(D)>2:
        print(agent.type,'dikkat h bhai')
        input()
    D=D[1]
    revD=revdir[D] 
    pos=(int(agent.position[0]),int(agent.position[1]))
    while pos not in Intersections:
        pos=(pos[0]+revD[0],pos[1]+revD[1])
    Sec=pos
    Road=Roads_Grid[(Sec,First)]
    safe=True
    for nagent in Road:
        if nagent.direction!="motion":
            continue
        if abs(nagent.position[0]-agent.position[0])+abs(nagent.position[1]-agent.position[1])<3:
            safe=False
              
    if safe==False:
        return -1,First       
    index=0
    for nagent in Road:
        if D==1:
            if nagent.position[1]<=agent.position[1]:
                break
        elif D==2:
            if nagent.position[1]>=agent.position[1]:
                break
        elif D==3:
            if nagent.position[0]>=agent.position[0]:
                break
        elif D==4:
            if nagent.position[0]<=agent.position[0]:
                break
        index+=1
    
    Roads_Grid[(Sec,First)].insert(index,agent)
    return 1,First

def is_overshoot(D,agent, GG):
    flag=0
    if D==1 and agent.position[1]<=GG[1]:
        flag=1
    elif D==2 and agent.position[1]>=GG[1]:
        flag=1
    elif D==3 and agent.position[0]>=GG[0]:
        flag=1
    elif D==4 and agent.position[0]<=GG[0]:
        flag=1

    return flag

def motion_to_rest(agent):
    agent.Wait=True
    agent.Index=-1
    agent.goalindex=-1
    agent.direction="rest"
    agent.goals=[]
    agent.nearestgoals=[]
    agent.size=2

def get_direction(a,b):
    x1,y1=a
    x2,y2=b
    
    if x1==x2:
        if y1<y2:
            return 2
        else:
            return 1
    elif y1==y2:
        if x1<x2:
            return 3
        else:
            return 4
    

def intT(A):
    B=(int(A[0]),int(A[1]))
    return B

def change_signal():
    for I in Intersections:
        index=0
        for j in range(1,len(Matrix.grid[I[0]][I[1]])):
            if j==0:
                continue
            D=Matrix.grid[I[0]][I[1]][j]
            if Intersection_Gateway[I][D]==1:
                index=j
                break
        if index==len(Matrix.grid[I[0]][I[1]])-1:
            index=0

        nxtD=Matrix.grid[I[0]][I[1]][index+1]
        Intersection_Gateway[I]=[0]*5
        Intersection_Gateway[I][nxtD]=1
        Intersection_Timeout[I]=50

def traffic_intersection(P,D):
    Pos=intT(P)
    if Intersection_Gateway[Pos][D]==1:
        return True,Intersection_Timeout[Pos]
    
    return False,-1

def update_intersection():
    for I in Intersections:
        if Intersection_Timeout[I]==0:
            change_signal()
        else:
            Intersection_Timeout[I]-=1



def handle_rack_agents(key,coloring):
    # update_intersection()
    for Road in Roads_lr:
        if Roads_lr[Road]==-1:      #Road in Reverse Direction
            continue
        removal,remover=[],[]
        for i in range(len(Roads_Grid[Road])): 
            agent=Roads_Grid[Road][i]
            if agent.human_delay>0:
                agent.human_delay-=1
                continue
            agent.charge-=.5
            if i==len(Roads_Grid[Road])-1:
                next_agent=Roads_Grid[Road][i]
            else:
                next_agent=Roads_Grid[Road][i+1]
            k=intT(agent.Path[agent.Index])
            D=Matrix.grid[int(Roads_Grid[Road][i].position[0])][int(Roads_Grid[Road][i].position[1])]
            if len(D)>2:
                new_point=((agent.position[0]+k[0])/2,(agent.position[1]+k[1])/2) 
                try:
                    D=Matrix.grid[int(new_point[0])][int(new_point[1])][1]
                except:
                    print('On Intersection')
                    print(agent.position,k)
                    pygame.draw.circle(screen,(255,0,0),(int(new_point[0]),int(new_point[1])),5)
                    pygame.display.flip()
                    x=input()
            else:
                try:
                    D=D[1]
                except:
                    print('Out of Map')
                    x=input()
            if agent.key_field==key:
                continue
            agent.key_field=key
            
            if agent.Index==0:
                flag=0
                if next_agent==agent or (abs(agent.position[0]-next_agent.position[0])+abs(agent.position[1]-next_agent.position[1]))>abs(agent.position[0]-agent.valet.position[0])+abs(agent.position[1]-agent.valet.position[1]):
                    if agent.v==0: # can improve upon this condition but will work fine till any bot does not malfunction and stop in between
                        # Reached the valet
                        flag=1
                    agent.update(agent.valet,D)
                else:
                    agent.update(next_agent,D)

                if flag:
                    agent.position=agent.valet.position
                    agent.Index-=1
                    agent.goalindex+=1
                    if agent.goalindex<len(agent.goals):
                        
                        if agent.goals[agent.goalindex]==[-7,-7]:
                            if agent.position in israck:
                                remover.append((Road,agent))
                            agent.Deposit_Delay=50
                            rack_available[agent.CurRack]=0.5
                            logger.info('Order'+','+str(agent.order_id)+','+'Warehouse'+','+str(agent.ind)+','+'Bot Reached the Desired Rack.')
                            agent.goalindex+=1    
                            
                        elif agent.goals[agent.goalindex]==[-14,-14]:
                            agent.human_delay=150
                            logger.info('Order'+','+str(agent.order_id)+','+'Warehouse'+','+str(agent.ind)+','+'Bot Reached the Human Counter with few items.')
                            doc=order_db.find_one({"_id":agent.order_id})
                            quantity=doc["ordered_quantity"]
                            progress=doc["order_progress"]
                            human_ct=doc["human_counter"]
                            total_items_carrying=0
                            for items in agent.items_carrying:
                                total_items_carrying+=items[1]
                            if total_items_carrying+progress==quantity:
                                logger.info('Finished Order'+','+str(agent.order_id)+','+'Warehouse'+','+str(agent.ind)+','+'Order is completed.')
                                conveyor_agent= Agent(1,n,m)
                                conveyor_agent.position=HCtoConveyor[human_ct]
                                conveyor_agent.order_id=agent.order_id
                                if human_ct<m: 
                                    conveyor_agent.Path=HCtoSorting[str((0,human_ct))].copy()
                                else:
                                    conveyor_agent.Path=HCtoSorting[str((1,human_ct-m))].copy()
                                conveyor_agent.Path.reverse()
                                conveyor_agent.Index=len(conveyor_agent.Path)
                                Conveyor_Agents.append(conveyor_agent)

                            order_db.update_one({"_id":agent.order_id},{"$inc":{"order_progress":total_items_carrying}})                            
                            agent.goalindex+=1
                        elif  agent.goals[agent.goalindex]==[-21,-21]:
                            if agent.position in israck:
                                remover.append((Road,agent))
                            agent.Deposit_Delay=50
                            logger.info('Event'+','+'-'+','+'Warehouse'+','+str(agent.ind)+','+'Kept the Rack back which it was carrying.')
                            motion_to_rest(agent)
                            rack_available[agent.CurRack]=1
                            agent.color = colors.YELLOW1
                            remove=[]
                            for colo in range(len(coloring)):
                                if coloring[colo][2]==agent:
                                    remove.append(coloring[colo])
                            for g in remove:
                                coloring.remove(g)
                                                        
                        elif agent.goals[agent.goalindex]==[-11,-11]:
                            logger.info('Charging'+','+'-'+','+'Warehouse'+','+str(agent.ind)+','+'Bot Reached the Charging Station.')
                            motion_to_rest(agent)
                            remover.append((Road,agent))
                            agent.Wait=False

                        elif agent.goals[agent.goalindex]==[-200,-200]:
                            logger.info('Charging'+','+'-'+','+'Warehouse'+','+str(agent.ind)+','+'Bot Reached back to its Rack with full Charge.')
                            motion_to_rest(agent)
                            agent.color = colors.YELLOW1
                        elif agent.goals[agent.goalindex]==[-70,-70]:
                            logger.info('Sorting Order'+','+'-'+','+'Warehouse'+','+str(agent.ind)+','+'Sorting Bot Picked Box from Conveyor Belt.')
                            agent.goalindex+=1
                        elif agent.goals[agent.goalindex]==[-140,-140]:
                            logger.info('Sorting Order'+','+str(agent.order_id)+','+'Sorting Bot'+','+str(agent.ind)+','+"Bot placed the order to it's dumping point.")
                            motion_to_rest(agent)
                            remover.append((Road,agent))


            elif i==len(Roads_Grid[Road])-1:
                agent.unstop()
                dist_remaining=ManhattanDistance(agent.position,k)
                passing=True
                if dist_remaining<8:    # Booking Check
                    if Traffic_Flag:
                        r=Intersection_Gateway[k]
                        if 1 in r:
                            r=r.index(1)
                            if D != r:
                                passing=False
                            else:
                                if Intersection_Booking[k] in [-1,agent.ind]:
                                    Intersection_Booking[k]=agent.ind
                                    Intersection_Coming_Dir[k]=D
                                    Intersection_Recal[k]=1
                                else:
                                    passing=False
                            if D!=r and Intersection_Booking[k]==agent.ind:
                                passing=True

                    else:
                        if Intersection_Booking[k] in [-1,agent.ind]:
                            Intersection_Booking[k]=agent.ind
                            Intersection_Coming_Dir[k]=D
                            Intersection_Recal[k]=1
                        else:
                            passing=False
                    
                if passing:
                    agent.update(None,D)
                else:
                    agent.update(Intersection_Bot[k],D)
                
                dist_r=ManhattanDistance(agent.position,k)
             # TODO : Try to adjust speed as bots enter intersection
                if dist_r<=1.6 and passing:
                    
                    removal.append(Road)
                    agent.position=k
                    agent.Index-=1
            else:
                if ManhattanDistance(agent.position,k)<=5:
                    agent.stop()

                else:
                    agent.update(next_agent,D)
                
        for r in removal:   
            Roads_Grid[r].pop()
        for r,a in remover:
            Roads_Grid[r].remove(a)

    for I in Intersections:
        if Intersection_Booking[I]==-1:
            continue
        if I in Sorting_Intersections:
            agent=Sorting_Agents[Intersection_Booking[I]]
        else:
            agent=Agents[Intersection_Booking[I]]
            
        if agent.key_field==key:
            continue
        
        if Intersection_Recal[I]==0:
            Intersection_Recal[I]=1
            Source=nearest_intersection(intT(agent.position))
            togoal=agent.goals[agent.goalindex]
            nearestIntersec=agent.nearestgoals[agent.goalindex]
            nAgent = Search(Source,nearestIntersec)
            nAgent.AStar(agent.theta,Agents,Truck_Agents,Sorting_Agents,0)
            nextIntersec_path=nAgent.getPathLong()
            agent.Path=nextIntersec_path
            last=nearest_intersection(togoal)
            agent.Path.append(last)
            agent.Path.reverse()
            agent.Path.pop()
            agent.Index=len(agent.Path)-1
       

        nextI=intT(agent.Path[agent.Index])
        #    raod joining I and nextI
        Road=(I,nextI)
        if agent.type==2 and agent.position==nextI:     #For Sorting Bot to reach the Conveyor belt
            agent.goalindex+=1
            agent.Index-=1
            if agent.goals[agent.goalindex]==[-70,-70]:
                logger.info('Sorting Order'+','+'-'+','+'Warehouse'+','+str(agent.ind)+','+'Sorting Bot Picked Box from Conveyor Belt.')
                agent.goalindex+=1
            
        elif Roads_Grid[Road]==[] or ManhattanDistance(I,Roads_Grid[Road][0].position)>2.5: # TODO: can improve this 2.5 later
            D_Dash=Matrix.grid[(I[0]+nextI[0])//2][(I[1]+nextI[1])//2][1]
            D=Intersection_Coming_Dir[I]
            x_gap=nextI[0]-I[0]
            y_gap=nextI[1]-I[1]
            if x_gap==0:
                # move in y
                agent.position=(I[0],I[1]+y_gap/abs(y_gap))
            elif y_gap==0:
                # move in x
                agent.position=(I[0]+x_gap/abs(x_gap),I[1])
         
            if D_Dash!=D:
                agent.v=0.1
            Roads_Grid[Road]=[agent]+Roads_Grid[Road]
            Intersection_Booking[I]=-1
            agent.key_field=key
    

    for i in range(len(Agents)):
        agent=Agents[i]
       
        if agent.position in israck:
            pygame.draw.circle(screen, agent.color, (agent.position[0]+10,agent.position[1]),2)
        else: 
            pygame.draw.circle(screen, agent.color, agent.position, agent.size)
        
        if agent.Deposit_Delay>0:
            agent.Deposit_Delay-=1
            continue
        if agent.cStation!=-1 and agent.position==charging_loc[agent.cStation] and abs(agent.charge-agent.maxcharge)<=1:
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
            Source=nearest_intersection(intT(agent.position))
            togoal=agent.goals[agent.goalindex]
            Ghost=Agent(0,n,m)
            Ghost.position=togoal
            agent.valet=Ghost
            nearestIntersec=agent.nearestgoals[agent.goalindex]
            nAgent = Search(Source,nearestIntersec)
            nAgent.AStar(agent.theta,Agents,Truck_Agents,Sorting_Agents,0)
            nextIntersec_path=nAgent.getPathLong()
            agent.Path=nextIntersec_path
            last=nearest_intersection(togoal)
            if last==Source:
                agent.Path=[Source]
            else:
                agent.Path.append(last)
            agent.Path.reverse()
            agent.Index=len(agent.Path)-1
            Road=(intT(agent.Path[agent.Index]),intT(agent.Path[agent.Index-1]))
            Roads_Grid[Road]=[agent]+Roads_Grid[Road]
        
        if agent.direction=='motion' and agent.Index==-1: #Order assigned hua h bhai ko naya naya --> nope               
            Source=nearest_intersection(intT(agent.position))
            if agent.position in israck:
                allowed,First=robo_rack_entry(agent)
                if allowed==-1:
                    continue
                else:
                    Source=First
            
            togoal=agent.goals[agent.goalindex]
            Ghost=Agent(0,n,m)
            Ghost.position=togoal
            agent.valet=Ghost
            nearestIntersec=agent.nearestgoals[agent.goalindex]
            nAgent = Search(Source,nearestIntersec)
            nAgent.AStar(agent.theta,Agents,Truck_Agents,Sorting_Agents,0)
            nextIntersec_path=nAgent.getPathLong()
            agent.Path=nextIntersec_path
            last=nearest_intersection(togoal)
            if last==Source:
                agent.Path=[Source]
            else:
                agent.Path.append(last)
            agent.Path.reverse()
            agent.Index=len(agent.Path)-1

        elif agent.direction=="rest" and agent.Index<=-1:
            if agent.needcharge==True:
                agent.color = colors.GREEN
                agent.charge+=1
            elif agent.charge<20:
                agent.charge=0
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
                allowed,First=robo_rack_entry(agent)
                if allowed==-1:
                    continue
                else:
                    Source=First
                togoal=agent.goals[agent.goalindex]
                Ghost=Agent(0,n,m)
                Ghost.position=togoal
                agent.valet=Ghost
                nearestIntersec=agent.nearestgoals[agent.goalindex]
                nAgent = Search(Source,nearestIntersec)
                nAgent.AStar(agent.theta,Agents,Truck_Agents,Sorting_Agents,0)
                nextIntersec_path=nAgent.getPathLong()
                agent.Path=nextIntersec_path
                last=nearest_intersection(togoal)
                if last==Source:
                    agent.Path=[Source]
                else:
                    agent.Path.append(last)
                agent.Path.reverse()
                agent.Index=len(agent.Path)-1

            

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
            removing_conveyor.append(Conveyor_Agents[i])
            # conveyor_agent.color=colors.PALEGREEN
        pygame.draw.circle(screen, conveyor_agent.color, conveyor_agent.position,4)
    
    for ind in removing_conveyor:
        Conveyor_Agents.remove(ind)
    removing_conveyor.clear()
            
# Same as for rack agents
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
        if  sorder[0:3]=='Dum':
            address=(random.randint(0,2*sorting_n-1),random.randint(0,2*sorting_m-1))
        else:
            address=tuple(order_history.find_one({"_id":sorder})["address"])
        finished_sorder.append(sorder)
        agent.goals=[numofdump["conveyor"],[-70,-70],numofdump[str(address)],[-140,-140]]
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
    lstr=[]
    for agent in Sorting_Agents:
        if agent.direction=='motion' and agent.Index==-1: #Order assigned hua h bhai ko naya naya --> nope               
            Source=nearest_intersection(intT(agent.position))
            if agent.position in isdump:
                allowed,First=robo_rack_entry(agent)
                if allowed==-1:
                    continue
                else:
                    Source=First
            togoal=agent.goals[agent.goalindex]
            Ghost=Agent(2,n,m)
            Ghost.position=togoal
            agent.valet=Ghost
            nearestIntersec=agent.nearestgoals[agent.goalindex]
            nAgent = Search(Source,nearestIntersec)
            nAgent.AStar(agent.theta,Agents,Truck_Agents,Sorting_Agents,0)
            nextIntersec_path=nAgent.getPathLong()
            agent.Path=nextIntersec_path
            last=nearest_intersection(togoal)
            if last==Source:
                agent.Path=[Source]
            elif togoal not in Sorting_Intersections:
                agent.Path.append(last)
            agent.Path.reverse()
            agent.Index=len(agent.Path)-1
        pygame.draw.circle(screen, agent.color, agent.position, agent.size)
        if agent.Wait==False:
            lstr.append((int(100000*agent.position[0]),int(100000*agent.position[1])))

    d=list(set(lstr))
    print('Collisions:',len(lstr)-len(d))








