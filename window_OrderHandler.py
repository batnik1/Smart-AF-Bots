from window_AgentHandler import *

def handle_orders(orders,coloring):
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
            nAgent = Search(agent.position,rack_location)
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

