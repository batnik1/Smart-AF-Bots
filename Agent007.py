import math
import random
random.seed(2000)
import colors
import numpy as np

class Agent():
    def __init__(self, type,n,m):
        self.position = (0, 0)
        self.Wait = True  # State Wait T/F, T if it can receive new orders, F is it is busy and cannot.
        self.type = type  # Type Rack/Warehouse/Sorting  -- 0/1/2
        self.Index = -1   # Path Index location
        self.path = []
        self.CurRack = str((random.randint(0,n-1), random.randint(0,m-1), random.randint(0, 4), random.randint(0, 4))) #default-rack for agent 
        self.color = colors.YELLOW1  
        self.size = 2
        self.order_id=0
        self.items_carrying=[]
        self.ind=0        
        self.charge=50   # Initial Charge
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
        self.velocity=1
        self.theta="North"
        self.maxcharge=self.charge
        self.human_delay=0
        self.key_field=-1       # Key field is used to test when did agent moved last
        self.valet=None
        self.temp_valet=None
        self.onroad=False
        self.timestamps=[]
        self.Originaltimestamps=[]
        # Vehicle's Fields
        self.l = 0.5
        self.dt=1
        self.s0 = 3
        self.T = 0.1
        self.v_max = 1.5
        self.a_max = .1
        self.b_max = .1 # TODO: Can change this to be same as a_max
        self.x = 0
        self.v = 0
        self.a = 0
        self.stopped = False
        self.sqrt_ab = 2*np.sqrt(self.a_max*self.b_max)
        self._v_max = self.v_max

    def update(self, lead,motion):
        movexy=0
        movenp=1
        if motion==1:
            movexy=1
            movenp=-1
        elif motion==2:
            movexy=1
        elif motion==4:
            movenp=-1 

        self.x=(movenp)*self.position[movexy]
        # Update position and velocity
        if self.v + self.a*self.dt < 0:
            self.x -= 1/2*self.v*self.v/self.a
            self.v = 0
        else:
            self.v += self.a*self.dt
            self.x += self.v*self.dt + self.a*self.dt*self.dt/2
        
        # Update acceleration
        alpha = 0
        if lead:
            lead.x=(movenp)*lead.position[movexy]
            delta_x = lead.x - self.x - lead.l
            delta_v = self.v - lead.v

            alpha = (self.s0 + max(0, self.T*self.v + delta_v*self.v/self.sqrt_ab)) / delta_x

        self.a = self.a_max * (1-(self.v/self.v_max)**4 - alpha**2)

        if self.stopped: 
            self.a = -self.b_max*self.v/self.v_max

        
        # print(self.position,self.x*movenp)
        if movexy:
            self.position=(self.position[0],self.x*movenp)
        else:
            self.position=(self.x*movenp,self.position[1])

    def stop(self):
        self.stopped = True

    def unstop(self):
        self.stopped = False

    def slow(self, v):
        self.v_max = v

    def unslow(self):
        self.v_max = self._v_max


