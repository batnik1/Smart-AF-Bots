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
# 
def robo_rack_entry(agent_id):
    # find nearest intersection 
    First=nearest_intersection((int(Agents[agent_id].position[0]),int(Agents[agent_id].position[1])))                
    # go in back direction from intersection
    D=Matrix.grid[int(Agents[agent_id].position[0])][int(Agents[agent_id].position[1])][1]
    revD=revdir[D] 
    pos=(int(Agents[agent_id].position[0]),int(Agents[agent_id].position[1]))
    while pos not in Intersections:
        pos=(pos[0]+revD[0],pos[1]+revD[1])
    Sec=pos
    # print("Firs,sec",First,Sec)
    Road=Roads_Grid[(Sec,First)]
    safe=True
    for agent in Road:
        if abs(agent.position[0]-Agents[agent_id].position[0])+abs(agent.position[1]-Agents[agent_id].position[1])<3:
            safe=False
              
    if safe==False:
        return -1,First       
    index=0
    for agent in Road:
        if D==1:
            if agent.position[1]<=Agents[agent_id].position[1]:
                break
        elif D==2:
            if agent.position[1]>=Agents[agent_id].position[1]:
                break
        elif D==3:
            if agent.position[0]>=Agents[agent_id].position[0]:
                break
        elif D==4:
            if agent.position[0]<=Agents[agent_id].position[0]:
                break
        index+=1
    
    Roads_Grid[(Sec,First)].insert(index,Agents[agent_id])
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

def handle_rack_agents(key):
    for Road in Roads_lr:
        if Roads_lr[Road]==-1:
            continue
        removal=[]
        for i in range(len(Roads_Grid[Road])): 
            D=Matrix.grid[int(Roads_Grid[Road][i].position[0])][int(Roads_Grid[Road][i].position[1])][1]
            agent=Roads_Grid[Road][i]
            if agent.key_field==key:
                continue
            agent.key_field=key
            if agent.Index>0:
                if i==len(Roads_Grid[Road])-1:
                    agent.update(None,D)
                else:
                    agent.update(Roads_Grid[Road][i+1],D)
                    
            if agent.Index==0:
                new_flag=1
                next_agent_pos=(inf,inf)
                if i+1<len(Roads_Grid[Road]):
                    next_agent_pos=(Roads_Grid[Road][i+1].position[0],Roads_Grid[Road][i+1].position[1])
                D1=ManhattanDistance(agent.position,next_agent_pos)
                D2=ManhattanDistance(agent.position,agent.valet.position)
                if D1<=4:
                    if D1>D2:
                        new_flag=0
                if new_flag:
                    if next_agent_pos==(inf,inf):
                        agent.update(None,D)
                    else:
                        agent.update(Roads_Grid[Road][i+1],D)
                else:
                    agent.update(agent.valet,D)
                if ManhattanDistance(agent.position,agent.valet.position)<2:
                    print('Goal Reached')
                    
            fir,sec=Road
            flag=is_overshoot(D,agent,sec)
            if flag:
                agent.position=sec
                agent.Index-=1
                agent.v=0
                new_fir=sec
                new_sec=tuple(agent.path[agent.Index])
                Roads_Grid[(new_fir,new_sec)].insert(0,agent)
                removal.append((fir,sec))


                
        for r in removal:   
            Roads_Grid[r].pop()

            
    for i in range(len(Agents)):
        agent=Agents[i]
        pygame.draw.circle(screen, agent.color, agent.position, agent.size)
      
        if agent.direction=='motion' and agent.Index==-1: #Order assigned hua h bhai ko naya naya 
            allowed,First=robo_rack_entry(i)
            if allowed==-1:
                continue
            togoal=agent.goals[agent.goalindex]
            Ghost=Agent(0,n,m)
            Ghost.position=togoal
            agent.valet=Ghost
            nearestIntersec=agent.nearestgoals[agent.goalindex]
            nAgent = Search(First,nearestIntersec)
            nAgent.AStar(agent.theta,Agents,Truck_Agents,Sorting_Agents,0)
            nextIntersec_path=nAgent.getPathLong()
            agent.path=nextIntersec_path
            pos=togoal
            last=nearest_intersection(togoal)
            agent.path.append(last)
            nextIntersec_path.reverse()
            agent.Index=len(nextIntersec_path)-1
            


            
            
            














