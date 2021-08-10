import math
from queue import PriorityQueue
import heapq
import numpy as np
from Grid import Grid
from matplotlib import path
from matplotlib import pyplot as plt
import time

import Make_map
# x=0
direction_change_penalty=5
from Make_map import matrix,Display_width,Display_height
class State(object):
    def __init__(self, state, parent, action,path_cost):
        self.children = []
        self.parent = parent
        self.state = state
        self.path_cost = path_cost
        self.action = action

    def CreateChildren(self):
        #print(self.state, self.path_cost)
        if self.state[0]<0 or self.state[1]<0 or self.state[0]>=Display_width-1 or self.state[1]>=Display_height-1:
            return

        if matrix.grid[self.state[0] - 1][self.state[1]] == 1:
            state = [self.state[0] - 1, self.state[1]]
            if self.parent!=0 and self.parent.action!=0:
                self.path_cost+=direction_change_penalty
            child = State(state, self,0,self.path_cost+1)
            if self.parent!=0 and self.parent.action!=0:
                self.path_cost-=direction_change_penalty
            self.children.append(child)
        if matrix.grid[self.state[0] + 1][self.state[1]] == 1:
            state = [self.state[0] + 1, self.state[1]]
            if self.parent!=0 and self.parent.action!=1:
                self.path_cost+=direction_change_penalty
            child = State(state,self,1,self.path_cost+1)
            if self.parent!=0 and self.parent.action!=1:
                self.path_cost-=direction_change_penalty
            self.children.append(child)
        if matrix.grid[self.state[0]][self.state[1] - 1] == 1:
            state = [self.state[0], self.state[1] - 1]
            if self.parent!=0 and self.parent.action!=2:
                self.path_cost+=direction_change_penalty
            child = State(state, self,2,self.path_cost+1)
            self.children.append(child)
            if self.parent!=0 and self.parent.action!=2:
                self.path_cost-=direction_change_penalty
        if matrix.grid[self.state[0]][self.state[1] + 1] == 1:
            state = [self.state[0], self.state[1] + 1]
            if self.parent!=0 and self.parent.action!=3:
                self.path_cost+=direction_change_penalty
            child = State(state, self,3,self.path_cost+1)
            if self.parent!=0 and self.parent.action!=3:
                self.path_cost-=direction_change_penalty
            self.children.append(child)


class A_Star_Solver:
    def __init__(self, start, goal):
        self.priorityQueue = PriorityQueue()
        self.start = start
        self.goal = goal

    def Solve(self):
        startState = State(self.start, 0, 0, 0)
        count=0
        self.priorityQueue.put((0,count,startState))
        reached = {str(startState.state): startState}
        while (self.priorityQueue.qsize()):
            closesestChild = self.priorityQueue.get()[2]
            #print(type(closesestChild))
            if self.goal == closesestChild.state:
                return closesestChild
            closesestChild.CreateChildren()
            for child in closesestChild.children:
                s = child.state
                if str(s) not in reached or child.path_cost < reached[str(s)].path_cost:
                    reached[str(s)] = child
                    count+=1
                    print(child.state,child.path_cost+abs(child.state[0]-self.goal[0]) + abs(child.state[1]-self.goal[1]))
                    self.priorityQueue.put((child.path_cost+abs(child.state[0]-self.goal[0]) + abs(child.state[1]-self.goal[1]),count,child))
        


# Calling all the existing stuffs
if __name__ == "__main__":
    t0= time.perf_counter()
    print("Hello")
    matrix = Grid(1000, 1000)
    matrix.build_roads()
    start1 = [800, 800]
    goal1 = [900, 900]
   
    print("Starting....")
    a = A_Star_Solver(start1, goal1)
    done = a.Solve()
    bet=0
    while done.parent!=0:
        bet+=1
        print(done.parent.state, done.path_cost)
        done=done.parent
    print(done.state)
    print(bet)
    t1 = time.perf_counter() - t0
    print("Time elapsed: ", t1) # CPU seconds elapsed (floating point)
    # for i in range(len(a.path)):
    #    #
    #    #print("{0}){1}".format(i,a.path[i]))
    #    pass 