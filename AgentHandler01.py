from window_Util import *   
from math import *   
Number_of_Agents=config['Number_of_Agents']
Number_of_SAgents= config['Number_of_SAgents']
Number_of_TAgents=len(truck_resting)
Agents = []
Conveyor_Agents=[]
Sorting_Agents=[]
Truck_Agents=[]
All_Agents=[]
random_intersection_flag=config['random_intersection_flag']
epsilon=config['epsilon']
Traffic_Flag=config['Traffic_Flag']
SBIG=config['SBIG']



# Used for Initialising our agents of rack/truck/sorting
def init_agents():
 
    for i in range(Number_of_Agents):
        nAgent=Agent(0,n,m)
        nAgent.CurRack=str((random.randint(0,m-1), random.randint(0,n-1), random.randint(0, 4), random.randint(0, 4)))
        nAgent.position=numofrack[nAgent.CurRack]
        nAgent.ind=i
        Agents.append(nAgent)
        All_Agents.append(nAgent)

    for _ in range(Number_of_SAgents):
        nAgent=Agent(2,n,m)
        nAgent.color=colors.PALEGREEN
        sorting_random=(random.randint(0,2*sorting_n-3),random.randint(0,2*sorting_m-3))
        nAgent.position=numofdump[str(sorting_random)]
        All_Agents.append(nAgent)
        Sorting_Agents.append(nAgent)
        
    for i in range(Number_of_TAgents):
        nAgent=Agent(1,n,m)
        nAgent.truck_rest=i
        nAgent.position=truck_resting[i]
        All_Agents.append(nAgent)
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
                return i+Number_of_Agents
    return -1


def get_TAgent():
    for i in range(len(Truck_Agents)):
        if Truck_Agents[i].Wait == True:
            return i + Number_of_Agents + Number_of_SAgents
    return -1

def robo_rack_entry(agent_id):
    # find nearest intersection 
    First=nearest_intersection((int(All_Agents[agent_id].position[0]),int(All_Agents[agent_id].position[1])))                
    # go in back direction from intersection
    D=Matrix.grid[int(All_Agents[agent_id].position[0])][int(All_Agents[agent_id].position[1])]
    if len(D)>2:
        print('dikkat h bhai')
        input()
    D=D[1]
    revD=revdir[D] 
    pos=(int(All_Agents[agent_id].position[0]),int(All_Agents[agent_id].position[1]))
    while pos not in Intersections:
        pos=(pos[0]+revD[0],pos[1]+revD[1])
    Sec=pos
    # print("Firs,sec",First,Sec)
    Road=Roads_Grid[(Sec,First)]
    safe=True
    for agent in Road:
        if agent.direction=="rest":
            continue
        if abs(agent.position[0]-All_Agents[agent_id].position[0])+abs(agent.position[1]-All_Agents[agent_id].position[1])<3:
            safe=False
              
    if safe==False:
        return -1,First       
    index=0
    for agent in Road:
        if D==1:
            if agent.position[1]<=All_Agents[agent_id].position[1]:
                break
        elif D==2:
            if agent.position[1]>=All_Agents[agent_id].position[1]:
                break
        elif D==3:
            if agent.position[0]>=All_Agents[agent_id].position[0]:
                break
        elif D==4:
            if agent.position[0]<=All_Agents[agent_id].position[0]:
                break
    
        index+=1
    
    Roads_Grid[(Sec,First)].insert(index,All_Agents[agent_id])
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
    agent.path=[]

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
        Intersection_Timeout[I]=200

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

def get_subgoals(agent):
    agent.direction="motion"
    agent.nearestgoals=[]
    agent.goalindex=0
    for g in range(len(agent.goals)):
        if agent.goals[g][0]<0:
            agent.nearestgoals.append(agent.goals[g])
            continue
        togoal=agent.goals[g]
        nearestIntersec=nearest_intersection(togoal,rev=True) 
        agent.nearestgoals.append(nearestIntersec)

def handle_rack_agents(key,coloring):
    current_items=0
    orders_completed_now=0
    Running_Finisher=0
    for Road in Roads_lr:
        if Roads_lr[Road]==-1:      #Road in Reverse Direction
            continue
        removal,remover=[],[]
        for i in range(len(Roads_Grid[Road])): 
            agent=Roads_Grid[Road][i]
            if agent.human_delay>0:
                agent.human_delay-=1
                continue
            if agent.type==0:
                agent.charge-=0.005
            if i==len(Roads_Grid[Road])-1:
                next_agent=Roads_Grid[Road][i]
            else:
                next_agent=Roads_Grid[Road][i+1]
            k=intT(agent.path[agent.Index])
            D=Matrix.grid[int(Roads_Grid[Road][i].position[0])][int(Roads_Grid[Road][i].position[1])]

            if len(D)>2:
                new_point=((agent.position[0]+k[0])/2,(agent.position[1]+k[1])/2) 
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
                        flag=1  # Reached the valet
                    agent.update(agent.valet,D)
                else:
                    agent.update(next_agent,D)

                if flag:
                    agent.position=agent.valet.position
                    agent.Index-=1
                    agent.goalindex+=1
                    if agent.goalindex<len(agent.goals):
                        if agent.type==0:
                            if agent.goals[agent.goalindex]==[-2,-2]:
                                if agent.position in israck:
                                    remover.append((Road,agent))
                                logger.info('Order'+','+str(agent.order_id)+','+'Warehouse'+','+str(agent.ind)+','+'Bot Reached the Rack No. '+str(agent.goalindex))
                                agent.goalindex+=1        
                            elif agent.goals[agent.goalindex]==[-7,-7]:
                                if agent.position in israck:
                                    remover.append((Road,agent))
                                logger.info('Order'+','+str(agent.order_id)+','+'Warehouse'+','+str(agent.ind)+','+'Bot Reached the Desired Rack.')
                                agent.goalindex+=1    
                                
                            elif agent.goals[agent.goalindex]==[-14,-14]:
                                agent.human_delay=25    
                                logger.info('Order'+','+str(agent.order_id)+','+'Warehouse'+','+str(agent.ind)+','+'Bot Reached the Human Counter with few items.')
                                doc=order_db.find_one({"_id":agent.order_id})
                                quantity=doc["ordered_quantity"]
                                progress=doc["order_progress"]
                                human_ct=doc["human_counter"]
                                total_items_carrying=0
                                if SBIG:
                                    for rack in agent.items_carrying:
                                        for items in agent.items_carrying[rack]:
                                            total_items_carrying+=items[1]  
                                else:
                                    for items in agent.items_carrying:
                                        total_items_carrying+=items[1]
                                current_items=total_items_carrying
                                if total_items_carrying+progress==quantity:
                                    orders_completed_now+=1
                                    logger.info('Finished Order'+','+str(agent.order_id)+','+'Warehouse'+','+str(agent.ind)+','+'Order is completed.')
                                    conveyor_agent= Agent(1,n,m)
                                    conveyor_agent.position=HCtoConveyor[human_ct]
                                    conveyor_agent.order_id=agent.order_id
                                    if human_ct<m: 
                                        conveyor_agent.path=HCtoSorting[str((0,human_ct))].copy()
                                    else:
                                        conveyor_agent.path=HCtoSorting[str((1,human_ct-m))].copy()
                                    conveyor_agent.path.reverse()
                                    conveyor_agent.Index=len(conveyor_agent.path)
                                    Conveyor_Agents.append(conveyor_agent)

                                order_db.update_one({"_id":agent.order_id},{"$inc":{"order_progress":total_items_carrying}})                            
                                agent.goalindex+=1
                            
                            elif  agent.goals[agent.goalindex]==[-21,-21]:
                                if agent.position in israck:
                                    remover.append((Road,agent))
                                logger.info('Event'+','+'-'+','+'Warehouse'+','+str(agent.ind)+','+'Kept the Rack back which it was carrying.')
                                motion_to_rest(agent)
                                rack_available[agent.CurRack]=1
                                agent.color = colors.YELLOW1
                                remove=[]
                                for colo in range(len(coloring)):
                                    if coloring[colo][2]==agent:
                                        remove.append(coloring[colo])
                                for i in remove:
                                    coloring.remove(i)
                                                            
                            elif agent.goals[agent.goalindex]==[-11,-11]:
                                logger.info('Charging'+','+'-'+','+'Warehouse'+','+str(agent.ind)+','+'Bot Reached the Charging Station.')
                                motion_to_rest(agent)
                                agent.Wait=False
                                remover.append((Road,agent))

                            elif agent.goals[agent.goalindex]==[-200,-200]:
                                logger.info('Charging'+','+'-'+','+'Warehouse'+','+str(agent.ind)+','+'Bot Reached back to its Rack with full Charge.')
                                motion_to_rest(agent)
                                agent.color = colors.YELLOW1
                                remover.append((Road,agent))
                        
                        elif agent.type==1:
                            if agent.goals[agent.goalindex]==[-7,-7]:
                                agent.goalindex+=1
                                add_item(agent.items_carrying[0],agent.items_carrying[1],agent.CurRack)
                                remover.append((Road,agent))
                                logger.info('Trucks in Warehouse'+','+'-'+','+'Truck Bot'+','+'-'+','+"Reached the Desired Rack with some new item type.")

                            elif  agent.goals[agent.goalindex]==[-14,-14]:
                                rack_available[agent.CurRack]=1
                                motion_to_rest(agent)
                                remover.append((Road,agent))

                        elif agent.type==2:
                            if agent.goals[agent.goalindex]==[-7,-7]:
                                agent.goalindex+=1
                            elif  agent.goals[agent.goalindex]==[-14,-14]:
                                Running_Finisher+=1
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
                               #     Intersection_Recal[k]=1
                                else:
                                    passing=False
                            if D!=r and Intersection_Booking[k]==agent.ind:
                                passing=True

                    else:
                        if Intersection_Booking[k] in [-1,agent.ind]:
                            Intersection_Booking[k]=agent.ind
                            Intersection_Coming_Dir[k]=D
                         #   Intersection_Recal[k]=1
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
                    Intersection_Recal[k]=1

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
        if Intersection_Recal[I]==0:
            continue

        agent=All_Agents[Intersection_Booking[I]]
        if agent.key_field==key:
            continue
        
        if Intersection_Calculated[I]==0:
            Intersection_Calculated[I]=1
            # calculate again its path
            togoal=agent.goals[agent.goalindex]
            nearestIntersec=agent.nearestgoals[agent.goalindex]
            nAgent = Search(I,nearestIntersec)
            nAgent.AStar(agent.theta,Agents,Truck_Agents,Sorting_Agents,agent.type,Roads_Grid,agent)
            nextIntersec_path=nAgent.getPathLong()
            agent.path=nextIntersec_path
            last=nearest_intersection(togoal)
            agent.path.append(last)
            # if agent.ind==73:
            #     print(agent.position,agent.path,last)
            agent.path.reverse()
            agent.path.pop()
            agent.Index=len(agent.path)-1
            
        try:
            nextI=intT(agent.path[agent.Index])
        except:
            print("new_wtf")
            # print(agent.type,agent.ind)
            # print(agent.position,numofrack[agent.CurRack])
            # print(agent.goals[agent.goalindex],agent.nearestgoals[agent.goalindex])
            # togoal=agent.goals[agent.goalindex]
            # print(nearest_intersection(togoal))
            # print(nearest_intersection(togoal,rev=True))
            for i in range(10000000):
                pygame.draw.circle(screen,colors.RED1,(int(agent.position[0]),int(agent.position[1])),5)
                pygame.display.flip()
            input()
        Road=(I,nextI)
        if Roads_Grid[Road]==[] or ManhattanDistance(I,Roads_Grid[Road][0].position)>2.5: # TODO: can improve this 2.5 later
            D_Dash=Matrix.grid[(I[0]+nextI[0])//2][(I[1]+nextI[1])//2][1]
            D=Intersection_Coming_Dir[I]
            x_gap=nextI[0]-I[0]
            y_gap=nextI[1]-I[1]
            if x_gap==0:    # move in y
                agent.position=(I[0],I[1]+y_gap/abs(y_gap))
            elif y_gap==0:  # move in x
                agent.position=(I[0]+x_gap/abs(x_gap),I[1])
         
            if D_Dash!=D:
                agent.v=0.1
            Roads_Grid[Road]=[agent]+Roads_Grid[Road]
            Intersection_Booking[I]=-1
            agent.key_field=key
            Intersection_Recal[I]=0
            Intersection_Calculated[I]=0
    
    for i in range(len(All_Agents)):
        
        agent=All_Agents[i]
        if agent.ind==2  and agent.type==2:
            pygame.draw.circle(screen,colors.RED1,(int(agent.position[0]),int(agent.position[1])),5)
            # draw red circle on its path
            for j in range(len(agent.path)):
                pygame.draw.circle(screen,colors.RED1,(int(agent.path[j][0]),int(agent.path[j][1])),3)
        elif agent.type==0:
            if agent.position in israck:
                pygame.draw.circle(screen, agent.color, (agent.position[0]+10,agent.position[1]),2)
            else: 
                pygame.draw.circle(screen, agent.color, agent.position, agent.size)
        elif agent.type==1:
            pygame.draw.circle(screen, agent.color, agent.position, agent.size)
        elif agent.type==2:
            pygame.draw.circle(screen, agent.color, agent.position, agent.size)  

        if agent.type==0 and agent.cStation!=-1 and agent.position==charging_loc[agent.cStation] and abs(agent.charge-agent.maxcharge)<=1:
            charging_state[agent.cStation]=0
            agent.cStation=-1
            agent.color = colors.LIGHTBLUE1
            agent.size = 3
            agent.needcharge=False
            agent.goals=[numofrack[agent.CurRack],[-200,-200]]
            get_subgoals(agent)
        if agent.direction=='motion' and agent.Index==-1: #Order assigned hua h bhai ko naya naya --> nope               
            Source=nearest_intersection(intT(agent.position))
            if (agent.position in israck) or (agent.position in isdump and agent.position!=numofdump["conveyor"]):
                allowed,First=robo_rack_entry(i)
                if allowed==-1:
                    continue
                else:
                    Source=First
            elif (agent.position not in numofhcounter.values()) and (agent.position!=numofdump["conveyor"]):
                las=nearest_intersection(intT(agent.position),rev=True)
                Roads_Grid[(las,Source)].append(agent)
                
            togoal=agent.goals[agent.goalindex]
            Ghost=Agent(0,n,m)
            Ghost.position=togoal
            agent.valet=Ghost
            nearestIntersec=agent.nearestgoals[agent.goalindex]
            nAgent = Search(Source,nearestIntersec)
            nAgent.AStar(agent.theta,Agents,Truck_Agents,Sorting_Agents,agent.type,Roads_Grid,agent)
            nextIntersec_path=nAgent.getPathLong()
            agent.path=nextIntersec_path
            last=nearest_intersection(togoal)
            if last==Source:
                agent.path=[Source]
            else:
                agent.path.append(last)
            agent.path.reverse()
            agent.Index=len(agent.path)-1

        if agent.type==0 and agent.Index <= -1 and agent.direction=="rest":
            
            # Increasing charge
            if agent.needcharge==True:
                agent.color = colors.GREEN
                agent.charge+=.05
            # Assigning agent a charging station if charge is low
            if agent.charge<20 and agent.needcharge == False:# and agent.cStation==-1: TODO: Remove this
                charge_ind,charge_box=get_charging()
                if charge_box==-1:
                    continue
                agent.color = colors.LIGHTBLUE1
                agent.cStation=charge_ind
                agent.needcharge=True
                agent.goals=[charge_box,[-11,-11]]
                get_subgoals(agent)
                agent.Wait = False
    return current_items,orders_completed_now,Running_Finisher
            
            














