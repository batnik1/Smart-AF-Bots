from queue import PriorityQueue

from Grid import Grid
from matplotlib import pyplot as plt
import numpy as np
from matplotlib import path

x=0
direction_change_penalty=5
from Make_map import Matrix
#Creating Base Class
class State(object):
    def __init__(self, value, parent, start = 0, goal = 0):
        self.children = []
        self.parent = parent
        self.value = value
        self.dist = 0
        self.cost = 0
        self.direction=0
        if parent:
            self.start = parent.start
            self.goal = parent.goal
            self.path = parent.path[:]
            self.cost = parent.cost
            self.path.append(value)
 
        else:
            self.path = [value]
            self.start = start
            self.goal = goal
        
        #print(value)
 
    def GetDistance(self):
        pass
    def CreateChildren(self,vistedQueue):
        pass
 
 
# Creating subclass
class State_String(State):
    def __init__(self, value, parent, start = 0, goal = 0 ):
        super(State_String, self).__init__(value, parent, start, goal)
        self.dist = self.GetDistance()
 
    def GetDistance(self):
            dist = abs(self.value[0]-self.goal[0])+abs(self.value[1]-self.goal[1])
            return dist
            
            # for i in range(len(self.goal)):
            #     letter = self.goal[i]
            #     dist += abs(i - self.value.index(letter))
            # return dist
 
    def CreateChildren(self,vistedQueue):
            global x
            global direction_change_penalty
            if self.value==[198,200]:
                x=0
            if self.value==[200,202]:
                x=0
            #print(self.value, abs(self.value[0]-self.goal[0])+abs(self.value[1]-self.goal[1]),x)
            if not self.children:
                if Matrix.grid[self.value[0]-1][self.value[1]]==1:
                    val=[self.value[0]-1,self.value[1]]
                    if self.parent!=0 and self.parent.direction!=0:
                        self.cost+=direction_change_penalty
                    if val not in vistedQueue:
                        self.direction=0
                        child=State_String(val,self)
                        self.children.append(child)
                    if self.parent!=0 and self.parent.direction!=0:
                        self.cost-=direction_change_penalty

                if Matrix.grid[self.value[0]+1][self.value[1]]==1 :
                    val=[self.value[0]+1,self.value[1]]
                    if self.parent!=0 and self.parent.direction!=2:
                        self.cost+=direction_change_penalty
                    if val not in vistedQueue:
                        self.direction=2
                        child=State_String(val,self)
                        self.children.append(child)
                    if self.parent!=0 and self.parent.direction!=2:
                        self.cost-=direction_change_penalty

                if Matrix.grid[self.value[0]][self.value[1]-1]==1 :
                    val=[self.value[0],self.value[1]-1]
                    if self.parent!=0 and self.parent.direction!=1:
                        self.cost+=direction_change_penalty
                    if val not in vistedQueue:
                        self.direction=1
                        child=State_String(val,self)
                        self.children.append(child)
                    if self.parent!=0 and self.parent.direction!=1:
                        self.cost-=direction_change_penalty

                if Matrix.grid[self.value[0]][self.value[1]+1]==1 :
                    val=[self.value[0],self.value[1]+1]
                    if self.parent!=0 and self.parent.direction!=3:
                        self.cost+=direction_change_penalty
                    if val not in vistedQueue:
                        self.direction=3
                        child=State_String(val,self)
                        self.children.append(child)  
                    if self.parent!=0 and self.parent.direction!=3:
                        self.cost-=direction_change_penalty

                # for i in range(len(self.goal)-1):
                #     val = self.value
                #     val = val[:i] + val[i+1] + val[i] + val[i+2:]
                #     child = State_String(val, self)
                #     self.children.append(child)

# Creating a class that hold the final magic
class A_Star_Solver:
    def __init__(self, start, goal):
        self.path = []
        self.vistedQueue =[]
        self.priorityQueue = PriorityQueue()
        self.start = start
        self.goal = goal
 
    def Solve(self):
        startState = State_String(self.start,0,self.start,self.goal)
        count = 0
        self.priorityQueue.put((0,count, startState))
        while(not self.path and self.priorityQueue.qsize()):
               if x:
                   print("in while loop",end=' ') 
               closesetChild = self.priorityQueue.get()[2]
               #print(closesetChild.value) 
               closesetChild.CreateChildren(self.vistedQueue)
               self.vistedQueue.append(closesetChild.value)
               #print(self.vistedQueue[-1],closesetChild.cost + closesetChild.dist ,len(self.vistedQueue))
               #print(closesetChild.value)
               for child in closesetChild.children:
                   if child.value not in self.vistedQueue:
                        count += 1
                        if not child.dist:
                            self.path = child.path
                            break
                        self.priorityQueue.put((child.dist+child.cost,count,child))
                        #print(child.value, self.vistedQueue)
                   else:
                       pass  
        if not self.path:
            print("Goal Of  is not possible !")
        return self.path
 

# Matrix = Grid(1600, 1600)
# Matrix.build_roads() 



# for i in range(650,700):
#     Matrix.grid[i][199]=0
#     pass
# for i in range(175,375):
#     Matrix.grid[400][i]=0
#     pass

# Calling all the existing stuffs
if __name__ == "__main__":
    start1 = [100,200]
    goal1 = [200,300]
    
    print("Starting....")
    a = A_Star_Solver(start1,goal1)
    a.Solve()
    for i in range(len(a.path)):
       #
       #print("{0}){1}".format(i,a.path[i]))
       pass 