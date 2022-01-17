import math
import random
random.seed(2600)
import colors


class Agent():
    def __init__(self, type,n,m):
        self.position = (0, 0)
        self.Wait = True  # State Wait T/F, T if it can receive new orders, F is it is busy and cannot.
        self.type = type  # Type Rack/Warehouse/Sorting  -- 0/1/2
        self.Index = -1   # Path Index location
        self.Path = []
        self.CurRack = str((random.randint(0,n-1), random.randint(0,m-1), random.randint(0, 4), random.randint(0, 4))) #default-rack for agent 
        self.color = colors.YELLOW1  
        self.size = 1
        self.order_id=0
        self.items_carrying=[]
        self.ind=0        
        self.charge=200000   # Initial Charge
        self.needcharge=False  # If Agent is Assisgned to a Chargin Station
        self.charging=False    # If Agent is Charging
        self.cStation=-1       # Current Charging Station
        self.truck_rest=-1    
        self.direction="rest"  # State Direction Rest/Motion 
        self.goalindex=0       # Current goal index
        self.goals=[]          # list of goals
        self.nearestgoals=[]   # list of goals  on workspace
        self.changelane=0      # if the agent wants to re-configure its path
        self.waitingperiod=0   # Waiting period for next time to calculate if the agent wants to change its lane
        self.cooldown_rack=0   # Cooldown period of racks assigned if congestion near the rack is too high
        self.velocity=1.5
        self.theta="North"
        self.maxcharge=self.charge
        self.human_delay=0
        