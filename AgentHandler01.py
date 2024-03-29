from window_Util import *
from math import *
Number_of_Agents = config['Number_of_Agents']
Number_of_SAgents = config['Number_of_SAgents']
Number_of_TAgents = len(truck_resting)
Agents = []
Conveyor_Agents = []
Sorting_Agents = []
Truck_Agents = []
All_Agents = []
random_intersection_flag = config['random_intersection_flag']
epsilon = config['epsilon']
Traffic_Flag = config['Traffic_Flag']
SBIG = config['SBIG']
Density_vs_Velocity_flag = config['Density_vs_Velocity']
queryFlag=config['queryFlag']
intersecFlag=config['intersecFlag']
similarityFlag=config['similarityFlag']
# Used for Initialising our agents of rack/truck/sorting
def init_agents():

    for i in range(Number_of_Agents):
        nAgent = Agent(0, n, m)
        nAgent.CurRack = str((random.randint(0, m-1), random.randint(0, n-1), random.randint(0, 4), random.randint(0, 4)))
        nAgent.position = numofrack[nAgent.CurRack]
      #  print(nAgent.position)
        nAgent.ind = i
        Agents.append(nAgent)
        All_Agents.append(nAgent)

    for _ in range(Number_of_SAgents):
        nAgent = Agent(2, n, m)
        nAgent.color = colors.PALEGREEN
        sorting_random = (random.randint(0, 2*sorting_n-3),
                          random.randint(0, 2*sorting_m-3))
        nAgent.position = numofdump[str(sorting_random)]
        All_Agents.append(nAgent)
        Sorting_Agents.append(nAgent)

    for i in range(Number_of_TAgents):
        nAgent = Agent(1, n, m)
        nAgent.truck_rest = i
        nAgent.color=colors.PINK1
        nAgent.position = truck_resting[i]
        nAgent.size=5
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
    First = nearest_intersection(
        (int(All_Agents[agent_id].position[0]), int(All_Agents[agent_id].position[1])))
    # go in back direction from intersection
    D = Matrix.grid[int(All_Agents[agent_id].position[0])
                    ][int(All_Agents[agent_id].position[1])]
    if len(D) > 2:
        print('dikkat h bhai')
        input()
    D = D[1]
    revD = revdir[D]
    pos = (int(All_Agents[agent_id].position[0]),
           int(All_Agents[agent_id].position[1]))
    while pos not in Intersections:
        pos = (pos[0]+revD[0], pos[1]+revD[1])
    Sec = pos
    # print("Firs,sec",First,Sec)
    Road = Roads_Grid[(Sec, First)]
    safe = True
    for agent in Road:
        if agent.direction == "rest":
            continue
        if abs(agent.position[0]-All_Agents[agent_id].position[0])+abs(agent.position[1]-All_Agents[agent_id].position[1]) < 3:
            safe = False

    if safe == False:
        return -1, First
    index = 0
    for agent in Road:
        if D == 1:
            if agent.position[1] <= All_Agents[agent_id].position[1]:
                break
        elif D == 2:
            if agent.position[1] >= All_Agents[agent_id].position[1]:
                break
        elif D == 3:
            if agent.position[0] >= All_Agents[agent_id].position[0]:
                break
        elif D == 4:
            if agent.position[0] <= All_Agents[agent_id].position[0]:
                break

        index += 1
    #Agents[agent_id].v=1.5
    Roads_Grid[(Sec, First)].insert(index, All_Agents[agent_id])
    return 1, First


def is_overshoot(D, agent, GG):
    flag = 0
    if D == 1 and agent.position[1] <= GG[1]:
        flag = 1
    elif D == 2 and agent.position[1] >= GG[1]:
        flag = 1
    elif D == 3 and agent.position[0] >= GG[0]:
        flag = 1
    elif D == 4 and agent.position[0] <= GG[0]:
        flag = 1

    return flag


def motion_to_rest(agent):
    agent.Wait = True
    agent.Index = -1
    agent.goalindex = -1
    agent.direction = "rest"
    agent.goals = []
    agent.nearestgoals = []
    agent.size = 2
    agent.path = []



def get_direction(a, b):
    x1, y1 = a
    x2, y2 = b

    if x1 == x2:
        if y1 < y2:
            return 2
        else:
            return 1
    elif y1 == y2:
        if x1 < x2:
            return 3
        else:
            return 4


def intT(A):
    B = (int(A[0]), int(A[1]))
    return B

def jaccard(A,B):
    Uni=[]
    And=[]
    for a in A:
        if a[0]<0:
            continue
        if a not in Uni:
            Uni.append(a)
        if (a not in And) and (a in B):
            And.append(a)
    for b in B:
        if b[0]<0:
            continue
        if b not in Uni:
            Uni.append(b)
    numerator=1.0*len(And)
    denominator=len(Uni)
    return numerator/denominator

def similarity(A,B):
    if similarityFlag==0:
        return min(0.99,jaccard(A,B))
    

def corelate(Agent1,Agent2):
    if Agent1.path==[] or Agent2.path==[]:
        return 0

    return similarity(Agent1.path,Agent2.path)

def computePriority():
    TrafficPriorityOld={}
    TrafficPriorityNew={}
    for i in range(len(All_Agents)):
        TrafficPriorityOld[i]=1.0/len(All_Agents)
    max_iterations=100
    errorThresh=0.001
    cache={}
    while max_iterations:
        # print("Iterations Left",iterations,":",TrafficPriority[0],TrafficPriority[1],TrafficPriority[2],TrafficPriority[3],TrafficPriority[4])
        for i in range(len(All_Agents)):
            damping=0.9
            currentPriority=0
            for j in range(len(All_Agents)):
                if j==i:
                    continue
                if (i,j) not in cache:
                    cache[(min(i,j),max(i,j))]=corelate(All_Agents[i],All_Agents[j])
                relate=cache[(min(i,j),max(i,j))]
                currentPriority+=relate*TrafficPriorityOld[j]
            TrafficPriorityNew[i]=(1-damping)+damping*currentPriority  
            TrafficPriorityNew[i]=min(0.99,TrafficPriorityNew[i])          
        error=sum([abs(a-TrafficPriorityOld[i]) for i,a in TrafficPriorityNew.items()])
        if error<errorThresh*len(All_Agents):
            break
        TrafficPriorityOld=TrafficPriorityNew.copy()
        max_iterations-=1
    v=[r for _,r in TrafficPriorityNew.items()]
    for e in v:
        assert(e<=2)
    # print(v)
    return TrafficPriorityNew
def change_signal():
    if intersecFlag==0:
        for I in Intersections:
            index = 0
            for j in range(1, len(Matrix.grid[I[0]][I[1]])):
                if j == 0:
                    continue
                D = Matrix.grid[I[0]][I[1]][j]
                if Intersection_Gateway[I][D] == 1:
                    index = j
                    break
            if index == len(Matrix.grid[I[0]][I[1]])-1:
                index = 0

            nxtD = Matrix.grid[I[0]][I[1]][index+1]
            Intersection_Gateway[I] = [0]*5
            Intersection_Gateway[I][nxtD] = 1
            Intersection_Timeout[I] = 25
    else:
        TrafficPrioirity=computePriority()
        for I in Intersections:
            maxPriority=-inf
            bestDir=-1
            D=0
            scores=[-1]*5
            for nebrI in Golden_Grid[(I[0],I[1])]:
                D+=1
                if nebrI==():
                    continue
                curPriority=0
                for bot in Roads_Grid[((I[0],I[1]),nebrI)]:
                    curPriority+=TrafficPrioirity[All_Agents.index(bot)]

                totalPriority=curPriority*0.5+0.5*StarvingD[I][D]
                scores[D]=totalPriority
            for j in range(1, len(Matrix.grid[I[0]][I[1]])):
                D = Matrix.grid[I[0]][I[1]][j]
                if scores[D]==-1:
                    scores[D]=StarvingD[I][D] 
            for r in range(1,5):
                if scores[r]>maxPriority:
                    maxPriority=scores[r]
                    bestDir=r            
            Intersection_Gateway[I] = [0]*5
            Intersection_Gateway[I][bestDir] = 1
            Intersection_Timeout[I] = 25
            for j in range(1, len(Matrix.grid[I[0]][I[1]])):
                StarvingD[I][Matrix.grid[I[0]][I[1]][j]]+=0.5
            StarvingD[I][bestDir]=0


    
                
def traffic_intersection(P, D):
    Pos = intT(P)
    if Intersection_Gateway[Pos][D] == 1:
        return True, Intersection_Timeout[Pos]

    return False, -1


def update_intersection():
    for I in Intersections:
        if Intersection_Timeout[I] == 0:
            change_signal()
        else:
            Intersection_Timeout[I] -= 1


def get_subgoals(agent):
    agent.direction = "motion"
    agent.nearestgoals = []
    agent.goalindex = 0
    for g in range(len(agent.goals)):
        if agent.goals[g][0] < 0:
            agent.nearestgoals.append(agent.goals[g])
            continue
        togoal = agent.goals[g]
        nearestIntersec = nearest_intersection(togoal, rev=True)
        agent.nearestgoals.append(nearestIntersec)

buffer=config['buffer']
def getFunc(t,T1,T2):
    if t<T1-buffer or t>T2+buffer:
        return 0
    if t>=T1-buffer and t<T1:
        return np.exp(-(t-T1)**2/buffer**2)
    if t>=T1 and t<=T2:
        return 1
    if t>T2 and t<=T2+buffer:
        return np.exp(-(t-T2)**2/buffer**2)

def query_time(Road,Time):
    count=1
    if queryFlag!=2:
        lst=Roads_Timestamp[tuple(Road)]
        for i in range(len(lst)):
            if Time>=lst[i][0] and Time<=lst[i][1]:
                if queryFlag==1:
                    count+=(lst[i][1]-Time)/(lst[i][1]-lst[i][0])
                else:
                    count+=1
    else:
        lst=Original_Timestamp[tuple(Road)]
        for i in range(len(lst)):
                count+=getFunc(Time,lst[i][0],lst[i][1])
    dense=count/ManhattanDistance(Road[0],Road[1])
    vel=get_velocity(dense)
    return vel



def put_timestamps(agent,key):
    future_time=[key,key]
    path=agent.path
    if agent.position in israck or (agent.position in isdump and agent.position != numofdump["conveyor"]) or agent.position in numofhcounter.values():
        Sorce=nearest_intersection(agent.position,rev=True)
        Road=(Sorce,agent.path[0])
        timez=ManhattanDistance(agent.position,agent.path[0])/query_time(Road,key)
        timez*=3
        future_time[0]=key
        future_time[1]=key+timez
        Original_Timestamp[(tuple(Sorce),tuple(path[0]))].append(tuple((future_time[0],future_time[1])))
        agent.Originaltimestamps.append([(tuple(Sorce),tuple(path[0])),tuple((future_time[0],future_time[1]))])
        Roads_Timestamp[(tuple(Sorce),tuple(path[0]))].append(tuple((future_time[0],future_time[1]+buffer)))
        agent.timestamps.append([(tuple(Sorce),tuple(path[0])),tuple((future_time[0],future_time[1]+buffer))])
    for i in range(len(path)-1):
        timez=ManhattanDistance(path[i],path[i+1])/query_time((tuple(path[i]),tuple(path[i+1])),future_time[0])
        future_time[0]=future_time[1]
        future_time[1]+=(timez)
        Original_Timestamp[(tuple(path[i]),tuple(path[i+1]))].append(tuple((future_time[0],future_time[1])))
        agent.Originaltimestamps.append([(tuple(path[i]),tuple(path[i+1])),tuple((future_time[0],future_time[1]))])
        Roads_Timestamp[(tuple(path[i]),tuple(path[i+1]))].append(tuple((future_time[0]-buffer,future_time[1]+buffer)))
        agent.timestamps.append([(tuple(path[i]),tuple(path[i+1])),tuple((future_time[0]-buffer,future_time[1]+buffer))])
        
def remove_timestamps(key):
    for Road in Roads_Timestamp:
        removed=[]
        for i,j in Roads_Timestamp[Road]:
            if key>j:
                removed.append((i,j))
        for r in removed:
           Roads_Timestamp[Road].remove(r)

    for Road in Original_Timestamp:
        removed=[]
        for i,j in Original_Timestamp[Road]:
            if key>j+10:
                removed.append((i,j))
        for r in removed:
           Original_Timestamp[Road].remove(r)
    
def remove_agent_timestamps(agent):
    for i in agent.timestamps:        
        Roads_Timestamp[i[0]].remove(i[1])
    agent.timestamps=[]
    for i in agent.Originaltimestamps:
        Original_Timestamp[i[0]].remove(i[1])
    agent.Originaltimestamps=[]


def handle_rack_agents(key, coloring,picks):
    current_items = 0
    orders_completed_now = 0
    Running_Finisher = 0
    for Road in Roads_lr:
        if Roads_lr[Road] == -1:  # Road in Reverse Direction
            continue
        removal, remover = [], []
        if Density_vs_Velocity_flag:
            velocities = []
            for agent in Roads_Grid[(Road)]:
                velocities.append(agent.v)
            if len(velocities) != 0:
                # calculate avg velocity
                avg_velocity = sum(velocities)/len(velocities)
                # See if entry of avg_velocity/ManhattanDistance(Point,Goal) is in the mongodb database Density_vs_Velocity
                x = len(velocities)/ManhattanDistance(Road[0], Road[1])
                # round it to 2 decimal places
                x = round(x, 2)
                y = Density_vs_Velocity.find_one({'density': x})
                if y == None:
                    # insert into database
                    Density_vs_Velocity.insert_one(
                        {'density': x, 'number': 1, 'avg_velocity': avg_velocity})
                else:
                    # see the number with density x
                    number = y['number']
                    avg_velocity = (y['avg_velocity'] *
                                    number+avg_velocity)/(number+1)
                    # update the database
                    Density_vs_Velocity.update_one(
                        {'density': x}, {'$set': {'avg_velocity': avg_velocity, 'number': number+1}})

       
        for i in range(len(Roads_Grid[Road])):
            agent = Roads_Grid[Road][i]
            if agent.human_delay > 0:
                agent.human_delay -= 1
                continue
            if agent.type == 0:
                agent.charge -= 0.005
            if i == len(Roads_Grid[Road])-1:
                next_agent = Roads_Grid[Road][i]
            else:
                next_agent = Roads_Grid[Road][i+1]
            k = intT(agent.path[agent.Index])
            D = Matrix.grid[int(Roads_Grid[Road][i].position[0])][int(
                Roads_Grid[Road][i].position[1])]

            if len(D) > 2:
                new_point = ((agent.position[0]+k[0])/2,
                             (agent.position[1]+k[1])/2)
                print('On Intersection')
                print(agent.position, k)
                pygame.draw.circle(screen, (255, 0, 0),
                                   (int(new_point[0]), int(new_point[1])), 5)
                pygame.display.flip()
                x = input()
            else:
                try:
                    D = D[1]
                except:
                    print('Out of Map')
                    x = input()
            if agent.key_field == key:
                continue
            agent.key_field = key
            
            if agent.Index == 0:
                flag = 0
                if next_agent == agent or (abs(agent.position[0]-next_agent.position[0])+abs(agent.position[1]-next_agent.position[1])) > abs(agent.position[0]-agent.valet.position[0])+abs(agent.position[1]-agent.valet.position[1]):
                    if agent.v == 0:  # can improve upon this condition but will work fine till any bot does not malfunction and stop in between
                        flag = 1  # Reached the valet
                    agent.update(agent.valet, D)
                else:
                    agent.update(next_agent, D)

                if flag:
                    agent.position = agent.valet.position
                    agent.Index -= 1
                    agent.goalindex += 1
                    if agent.goalindex < len(agent.goals):
                        if agent.type == 0:
                            if agent.goals[agent.goalindex] == [-2, -2]:
                                if agent.position in israck:
                                    remover.append((Road, agent))
                                logger.info('Order'+','+str(agent.order_id)+','+'Warehouse'+','+str(
                                    agent.ind)+','+'Bot Reached the Rack No. '+str(agent.goalindex))
                                picks+=1
                                agent.goalindex += 1
                            elif agent.goals[agent.goalindex] == [-7, -7]:
                                if agent.position in israck:
                                    remover.append((Road, agent))
                                logger.info('Order'+','+str(agent.order_id)+','+'Warehouse' +
                                            ','+str(agent.ind)+','+'Bot Reached the Desired Rack.')
                                agent.goalindex += 1
                                picks+=1
                            elif agent.goals[agent.goalindex] == [-14, -14]:
                                agent.human_delay = 25
                                logger.info('Order'+','+str(agent.order_id)+','+'Warehouse'+','+str(
                                    agent.ind)+','+'Bot Reached the Human Counter with few items.')
                                doc = order_db.find_one(
                                    {"_id": agent.order_id})
                                quantity = doc["ordered_quantity"]
                                progress = doc["order_progress"]
                                human_ct = doc["human_counter"]
                                total_items_carrying = 0
                                if SBIG:
                                    for rack in agent.items_carrying:
                                        for items in agent.items_carrying[rack]:
                                            total_items_carrying += items[1]
                                else:
                                    for items in agent.items_carrying:
                                        total_items_carrying += items[1]
                                current_items = total_items_carrying
                                if total_items_carrying+progress == quantity:
                                    orders_completed_now += 1
                                    logger.info('Finished Order'+','+str(agent.order_id)+',' +
                                                'Warehouse'+','+str(agent.ind)+','+'Order is completed.')
                                    conveyor_agent = Agent(1, n, m)
                                    conveyor_agent.position = HCtoConveyor[human_ct]
                                    conveyor_agent.order_id = agent.order_id
                                    if human_ct < m:
                                        conveyor_agent.path = HCtoSorting[str(
                                            (0, human_ct))].copy()
                                    else:
                                        conveyor_agent.path = HCtoSorting[str(
                                            (1, human_ct-m))].copy()
                                    conveyor_agent.path.reverse()
                                    conveyor_agent.Index = len(
                                        conveyor_agent.path)
                                    Conveyor_Agents.append(conveyor_agent)

                                order_db.update_one({"_id": agent.order_id}, {
                                                    "$inc": {"order_progress": total_items_carrying}})
                                agent.goalindex += 1

                            elif agent.goals[agent.goalindex] == [-21, -21]:
                                if agent.position in israck:
                                    remover.append((Road, agent))
                                logger.info('Event'+','+'-'+','+'Warehouse'+','+str(
                                    agent.ind)+','+'Kept the Rack back which it was carrying.')
                                motion_to_rest(agent)
                                # remove_timestamps(key)
                                rack_available[agent.CurRack] = 1
                                agent.color = colors.YELLOW1
                                remove = []
                                for colo in range(len(coloring)):
                                    if coloring[colo][2] == agent:
                                        remove.append(coloring[colo])
                                for i in remove:
                                    coloring.remove(i)

                            elif agent.goals[agent.goalindex] == [-11, -11]:
                                logger.info('Charging'+','+'-'+','+'Warehouse'+',' +
                                            str(agent.ind)+','+'Bot Reached the Charging Station.')
                                motion_to_rest(agent)
                                # remove_timestamps(key)
                                agent.Wait = False
                                remover.append((Road, agent))

                            elif agent.goals[agent.goalindex] == [-200, -200]:
                                logger.info('Charging'+','+'-'+','+'Warehouse'+','+str(
                                    agent.ind)+','+'Bot Reached back to its Rack with full Charge.')
                                motion_to_rest(agent)
                                # remove_timestamps(key)
                                agent.color = colors.YELLOW1
                                remover.append((Road, agent))

                        elif agent.type == 1:
                            if agent.goals[agent.goalindex] == [-7, -7]:
                                agent.goalindex += 1
                                add_item(agent.items_carrying[0], agent.items_carrying[1], agent.CurRack)
                                remover.append((Road, agent))
                                logger.info('Trucks in Warehouse'+','+'-'+','+'Truck Bot'+',' +
                                            '-'+','+"Reached the Desired Rack with some new item type.")

                            elif agent.goals[agent.goalindex] == [-14, -14]:
                                rack_available[agent.CurRack] = 1
                                motion_to_rest(agent)
                                # remove_timestamps(key)
                                remover.append((Road, agent))

                        elif agent.type == 2:
                            if agent.goals[agent.goalindex] == [-7, -7]:
                                agent.goalindex += 1
                                picks+=1
                            elif agent.goals[agent.goalindex] == [-14, -14]:
                                Running_Finisher += 1
                                logger.info('Sorting Order'+','+str(agent.order_id)+','+'Sorting Bot'+','+str(
                                    agent.ind)+','+"Bot placed the order to it's dumping point.")
                                motion_to_rest(agent)
                                # remove_timestamps(key)
                                remover.append((Road, agent))

            elif i == len(Roads_Grid[Road])-1:
                agent.unstop()
                dist_remaining = ManhattanDistance(agent.position, k)
                passing = True
                if dist_remaining < 8:    # Booking Check
                    if Traffic_Flag:
                        r = Intersection_Gateway[k]
                        if 1 in r:
                            r = r.index(1)
                            if D != r:
                                passing = False
                            else:
                                if Intersection_Booking[k] in [-1, agent.ind]:
                                    Intersection_Booking[k] = agent.ind
                                    Intersection_Coming_Dir[k] = D
                               #     Intersection_Recal[k]=1
                                else:
                                    passing = False
                            if D != r and Intersection_Booking[k] == agent.ind:
                                passing = True

                    else:
                        if Intersection_Booking[k] in [-1, agent.ind]:
                            Intersection_Booking[k] = agent.ind
                            Intersection_Coming_Dir[k] = D
                         #   Intersection_Recal[k]=1
                        else:
                            passing = False

                if passing:
                    agent.update(None, D)
                else:
                    agent.update(Intersection_Bot[k], D)

                dist_r = ManhattanDistance(agent.position, k)
                # TODO : Try to adjust speed as bots enter intersection
                if dist_r <= 1.6 and passing:
                    removal.append(Road)
                    #print("passed")
                    agent.position = k
                    agent.Index -= 1
                    Intersection_Recal[k] = 1

            else:

                if ManhattanDistance(agent.position, k) <= 5:
                    agent.stop()
                else:
                    agent.update(next_agent, D)

        for r in removal:
            Roads_Grid[r].pop()
        for r, a in remover:
            Roads_Grid[r].remove(a)

    for I in Intersections:
        if Intersection_Recal[I] == 0:
            continue

        agent = All_Agents[Intersection_Booking[I]]
        if agent.key_field == key:
            continue
        if congestion_flag !=0:
            if Intersection_Calculated[I] == 0:
                Intersection_Calculated[I] = 1
                # calculate again its path
                if congestion_flag==2:
                    remove_agent_timestamps(agent)
                togoal = agent.goals[agent.goalindex]
                nearestIntersec = agent.nearestgoals[agent.goalindex]
                nAgent = Search(I, nearestIntersec)
                nAgent.AStar(Roads_Grid,agent,Roads_Timestamp,query_time,key)
                nextIntersec_path = nAgent.getPathLong()
                agent.path = nextIntersec_path
                last = nearest_intersection(togoal)
                agent.path.append(last)
                if congestion_flag==2:
                 #   remove_agent_timestamps(agent)
                    put_timestamps(agent,key)
                # if agent.ind==73:
                #     print(agent.position,agent.path,last)
                agent.path.reverse()
                agent.path.pop()
                agent.Index = len(agent.path)-1

        try:
            nextI = intT(agent.path[agent.Index])
        except:
            print("new_wtf")
            print(agent.type, agent.ind)
            print(agent.position, numofrack[agent.CurRack])
            print(agent.goals[agent.goalindex],
                  agent.nearestgoals[agent.goalindex])
            togoal = agent.goals[agent.goalindex]
            print(nearest_intersection(togoal))
            print(nearest_intersection(togoal, rev=True))
            for i in range(10000000):
                pygame.draw.circle(screen, colors.RED1, (int(
                    agent.position[0]), int(agent.position[1])), 5)
                pygame.display.flip()
            input()
        Road = (I, nextI)
        # TODO: can improve this 2.5 later
        if Roads_Grid[Road] == [] or ManhattanDistance(I, Roads_Grid[Road][0].position) > 2.5:
            D_Dash = Matrix.grid[(I[0]+nextI[0])//2][(I[1]+nextI[1])//2][1]
            D = Intersection_Coming_Dir[I]
            x_gap = nextI[0]-I[0]
            y_gap = nextI[1]-I[1]
            if x_gap == 0:    # move in y
                agent.position = (I[0], I[1]+y_gap/abs(y_gap))
            elif y_gap == 0:  # move in x
                agent.position = (I[0]+x_gap/abs(x_gap), I[1])

            if D_Dash != D:
                agent.v = 0.1
            Roads_Grid[Road] = [agent]+Roads_Grid[Road]
            Intersection_Booking[I] = -1
            agent.key_field = key
            Intersection_Recal[I] = 0
            Intersection_Calculated[I] = 0

    for i in range(len(All_Agents)):

        agent = All_Agents[i]
        if agent.ind == -1 and agent.type == 0:
            pygame.draw.circle(screen, colors.RED1, (int(
                agent.position[0]), int(agent.position[1])), 5)
            # print(agent.v,end=",")
            # if agent.v==0.1:
            #     print()
            # draw red circle on its path
            for j in range(len(agent.path)):
                pygame.draw.circle(screen, colors.RED1, (int(
                    agent.path[j][0]), int(agent.path[j][1])), 3)
        # elif agent.ind == 1 and agent.type == 0:
        #     pygame.draw.circle(screen, colors.GREEN1, (int(
        #         agent.position[0]), int(agent.position[1])), 5)
        #     # print(agent.v,end=",")
        #     # if agent.v==0.1:
        #     #     print()
        #     # draw red circle on its path
        #     for j in range(len(agent.path)):
        #         pygame.draw.circle(screen, colors.GREEN1, (int(
        #             agent.path[j][0]), int(agent.path[j][1])), 3)
        # elif agent.ind == 2 and agent.type == 0:
        #     pygame.draw.circle(screen, colors.YELLOW1, (int(
        #         agent.position[0]), int(agent.position[1])), 5)
        #     # print(agent.v,end=",")
        #     # if agent.v==0.1:
        #     #     print()
        #     # draw red circle on its path
        #     for j in range(len(agent.path)):
        #         pygame.draw.circle(screen, colors.YELLOW1, (int(
        #             agent.path[j][0]), int(agent.path[j][1])), 3)
        # elif agent.ind == 3 and agent.type == 0:
        #     pygame.draw.circle(screen, colors.CADETBLUE1, (int(
        #         agent.position[0]), int(agent.position[1])), 5)
        #     # print(agent.v,end=",")
        #     # if agent.v==0.1:
        #     #     print()
        #     # draw red circle on its path
        #     for j in range(len(agent.path)):
        #         pygame.draw.circle(screen, colors.CADETBLUE1, (int(
        #             agent.path[j][0]), int(agent.path[j][1])), 3)
        elif agent.type == 0:
            if agent.position in israck:
                pygame.draw.circle(screen, agent.color,
                                   (agent.position[0]+10, agent.position[1]), 2)
            else:
                pygame.draw.circle(screen, agent.color,
                                   agent.position, agent.size)
        elif agent.type == 1:
            pygame.draw.circle(screen, agent.color, agent.position, agent.size)
        elif agent.type == 2:
            pygame.draw.circle(screen, agent.color, agent.position, agent.size)

        if agent.type == 0 and agent.cStation != -1 and agent.position == charging_loc[agent.cStation] and abs(agent.charge-agent.maxcharge) <= 1:
            charging_state[agent.cStation] = 0
            agent.cStation = -1
            agent.color = colors.LIGHTBLUE1
            agent.size = 3
            agent.needcharge = False
            agent.goals = [numofrack[agent.CurRack], [-200, -200]]
            get_subgoals(agent)
        if agent.direction == 'motion' and agent.Index == -1:  # Order assigned hua h bhai ko naya naya --> nope
            Source = nearest_intersection(intT(agent.position))
            if (agent.position in israck) or (agent.position in isdump and agent.position != numofdump["conveyor"]):
                allowed, First = robo_rack_entry(i)
                if allowed == -1:
                    continue
                else:
                    Source = First
            elif (agent.position not in numofhcounter.values()) and (agent.position != numofdump["conveyor"]):
                las = nearest_intersection(intT(agent.position), rev=True)
                Roads_Grid[(las, Source)].append(agent)

            togoal = agent.goals[agent.goalindex]
            Ghost = Agent(0, n, m)
            Ghost.position = togoal
            agent.valet = Ghost
            if congestion_flag==2:
                remove_agent_timestamps(agent)
            nearestIntersec = agent.nearestgoals[agent.goalindex]
            nAgent = Search(Source, nearestIntersec)
            nAgent.AStar(Roads_Grid, agent,Roads_Timestamp,query_time,key)
            nextIntersec_path = nAgent.getPathLong()
            agent.path = nextIntersec_path
            last = nearest_intersection(togoal)
            if last == Source:
                agent.path = [Source]
            else:
                agent.path.append(last)
            if congestion_flag==2:
                #remove_agent_timestamps(agent)
                put_timestamps(agent,key)
            agent.path.reverse()
            agent.Index = len(agent.path)-1

        if agent.type == 0 and agent.Index <= -1 and agent.direction == "rest":

            # Increasing charge
            if agent.needcharge == True:
                agent.color = colors.GREEN
                agent.charge += .05
            # Assigning agent a charging station if charge is low
            if agent.charge < 20 and agent.needcharge == False:  # and agent.cStation==-1: TODO: Remove this
                charge_ind, charge_box = get_charging()
                if charge_box == -1:
                    continue
                agent.color = colors.LIGHTBLUE1
                agent.cStation = charge_ind
                agent.needcharge = True
                agent.goals = [charge_box, [-11, -11]]
                get_subgoals(agent)
                agent.Wait = False
    return current_items, orders_completed_now, Running_Finisher,picks
