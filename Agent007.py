import math
import random
import colors
#  1 toh yeh truck wale aur varna yeh counter


class Agent():
    def __init__(self, type,n,m):
        self.position = (0, 0)
        self.Wait = True
        self.type = type
        self.Index = -1
        self.Path = []
        self.CurRack = str((random.randint(0,n-1), random.randint(0,m-1), random.randint(0, 4), random.randint(0, 4)))
        self.color = colors.YELLOW1
        self.size = 2
        self.order_id=0
        self.items_carrying=[]
        self.ind=0
        self.charge=200
        self.needcharge=False
        self.charging=False
        self.cStation=-1
        self.truck_rest=-1
