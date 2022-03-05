from queue import PriorityQueue
import math
import heapq
import queue
import collections
from Grid import Grid
import time
import yaml
from avg_values import *

ks=0
Golden_Grid={}

def get_config(config):
    with open(config, 'r') as stream:
        return yaml.load(stream,yaml.SafeLoader)

config = get_config('parameters.yaml')
congestion_flag=config['congestion_flag']

def ManhattanDistance(start, end):
    return abs(start[0]-end[0])+abs(start[1]-end[1])


dx4 = [(-1, 0), (0, -1), (1, 0), (0, 1)]
INF = math.inf
dir = [(-1, -1), (0, -1), (0, 1), (1, 0), (-1, 0)]      # (-1,-1) is just pushed to make it 1 based indexing
revdir = [(-1, -1), (0, 1), (0, -1), (-1, 0), (1, 0)]

# density_dic={}
# density_dic[0.04]=0.8849388764779784
# density_dic[0.05]=0.8422870938888083
# density_dic[0.1]=0.6598127291564279
# density_dic[0.08]=0.7908560072151424
# density_dic[0.12]=0.6316617300675831
# density_dic[0.15]=0.491562152469726
# density_dic[0.03]=0.8799984059669639
# density_dic[0.2]=0.3999772068236708
# density_dic[0.16]=0.4935203863876017
# density_dic[0.01]=1.1849992315902942
# density_dic[0.25]=0.18067947929292297
# density_dic[0.3]=0.19653789061143037
# density_dic[0.24]=0.35449773005951474
# density_dic[0.07]=0.800190339844804
# density_dic[0.02]=1.0702664571213356
# density_dic[0.06]=0.962159466366327
# density_dic[0.09]=0.8318022972901102
# density_dic[0.13]=0.566065271223799
# density_dic[0.17]=0.47711237571118814
# density_dic[0.11]=0.78492482407427
# density_dic[0.14]=0.3751944014274457
# density_dic[0.18]=0.41059596785296576
# density_dic[0.19]=0.39169760953750776
# density_dic[0.21]=0.34688303277550997



N = 1500

diss = [[INF for i in range(N)] for j in range(N)]
press = [[[-1, -1] for i in range(N)] for j in range(N)]

def heat_value(Point,z,Agents,Truck_Agents,Sorting_Agents):         # To get Heat Value at position = Point with flag as z depicting which type of bot we want to calculate for 
    x,y=Point
    heat=0
    sigma=100
    num=0
    if z==0:
        for agent in Agents:
            if agent.Wait==True or agent.direction=='rest':
                continue
            num+=1
            X,Y=agent.position
            heat+=math.exp(-(pow(x-X,2)+pow(y-Y,2))/pow(sigma,2))
        for agent in Truck_Agents:
            if agent.Wait==True or agent.direction=='rest':
                continue
            num+=1
            X,Y=agent.position
            heat+=math.exp(-(pow(x-X,2)+pow(y-Y,2))/pow(sigma,2))        
    if z==1:
        num=len(Sorting_Agents)
        for agent in Sorting_Agents:
            if agent.Wait==True or agent.direction=='rest':
                continue    
            num+=1
            X,Y=agent.position
            heat+=math.exp(-(pow(x-X,2)+pow(y-Y,2))/pow(sigma,2))
    if z==2:
        num=len(Agents)+len(Truck_Agents)
        for agent in Agents:
            if agent.Wait==True or agent.direction=='rest':
                continue
            num+=1
            X,Y=agent.position
            heat+=math.exp(-(pow(x-X,2)+pow(y-Y,2))/pow(sigma,2))
        for agent in Truck_Agents:
            if agent.Wait==True or agent.direction=='rest':
                continue
            num+=1
            X,Y=agent.position
            heat+=math.exp(-(pow(x-X,2)+pow(y-Y,2))/pow(sigma,2))/10    
    if num==0:
        return 0
    return (heat-1)/num

Matrix = Grid(N, N)

def get_heuristic(Point,Goal,Roads_Grid=None,original=None):              # Heuristic Function
    if congestion_flag:
        velocities=[]
        for agent in Roads_Grid[((Point[0],Point[1]),(Goal[0],Goal[1]))]:
            if agent.ind!=original.ind: 
              #  print(agent.ind,original.ind,(Point,Goal),agent.position,original.position)
              #  print(Roads_Grid[((Point[0],Point[1]),(Goal[0],Goal[1]))])
                velocities.append(agent.v)
        len_vel=len(velocities)+1 #1
        if round(len_vel/ManhattanDistance(Point,Goal),2) in density_dic:
            return ManhattanDistance(Point,Goal)/density_dic[round(len_vel/ManhattanDistance(Point,Goal),2)]
        print('other one',round(len_vel/ManhattanDistance(Point,Goal),2))
        if len(velocities)==0:
            velocities=[1]
        # calculate avg velocity
        avg_velocity=sum(velocities)/len(velocities)
        if avg_velocity==0:
            avg_velocity=0.0000001
        time=ManhattanDistance(Point,Goal)/avg_velocity
        return time
        
        return ManhattanDistance(Point,Goal)
    else:
        return ManhattanDistance(Point,Goal)

def turning_time(A,B,theta):
    if A==B:
        return theta,0
    
    if A[0]==B[0]:
        if A[1]>B[1]:
            curTheta="North"
        else:
            curTheta="South"
    else:
        if A[0]>B[0]:
            curTheta="West"
        else:
            curTheta="East"
    
    if curTheta==theta:
        return curTheta,0

    return curTheta,50


class Search(): 

    def __init__(self, source, destination):
        self.heap = []
        self.source = source
        self.dest = destination
        self.dist=[x[:] for x in diss]
        self.prev=[x[:] for x in press]

    def AStar(self,theta,Agents,Truck_Agents,Sorting_Agents,flag,Roads_Grid,agent):    # Main Path Planning Function for all type of Agents
       # print(self.source,self.dest)
        if congestion_flag==0:
            heapq.heappush(self.heap, (get_heuristic(self.source, self.dest),0,theta, self.source)) 
            self.dist[self.source[0]][self.source[1]] = get_heuristic(self.source, self.dest)
            while len(self.heap) > 0:
                (cumltv,g,curTheta,cState) = heapq.heappop(self.heap)      
                if cumltv > self.dist[cState[0]][cState[1]]:
                    continue
                if cState == self.dest:
                    break
                
                for nextZ in Golden_Grid[(cState[0],cState[1])]:
                    if nextZ==():
                        continue
                    (nextX,nextY)=nextZ
                    if nextX >= 0 and nextY >= 0 and nextX < Matrix.height and nextY < Matrix.width:
                        nextTheta,turnTime=turning_time(cState,nextZ,curTheta)
                        newDist=g+get_heuristic(cState,[nextX,nextY])+get_heuristic([nextX,nextY],self.dest)
                        if self.dist[nextX][nextY] > newDist:
                            self.dist[nextX][nextY] = newDist
                            self.prev[nextX][nextY] = cState
                            heapq.heappush(self.heap, (self.dist[nextX][nextY],g+get_heuristic(cState,[nextX,nextY]),nextTheta, [nextX, nextY]))
        else:
            # UCS
            heapq.heappush(self.heap,(0,theta,self.source))
            self.dist[self.source[0]][self.source[1]] = 0
            while len(self.heap) > 0:
                (g,curTheta,cState) = heapq.heappop(self.heap)
                if cState == self.dest:
                    break
                for nextZ in Golden_Grid[(cState[0],cState[1])]:
                    if nextZ==():
                        continue
                    (nextX,nextY)=nextZ
                    if nextX >= 0 and nextY >= 0 and nextX < Matrix.height and nextY < Matrix.width:
                        nextTheta,turnTime=turning_time(cState,nextZ,curTheta)
                        newDist=g+get_heuristic(cState,[nextX,nextY],Roads_Grid=Roads_Grid,original=agent)
                        if self.dist[nextX][nextY] > newDist:
                            self.dist[nextX][nextY] = newDist
                            self.prev[nextX][nextY] = cState
                            heapq.heappush(self.heap, (self.dist[nextX][nextY],nextTheta,[nextX, nextY]))
    def BFS(self, rev=False):
        queue = collections.deque([self.source])
        self.dist[self.source[0]][self.source[1]] = 0
        while queue:
            cState = queue.popleft()
            
            for i in range(1, len(Matrix.grid[cState[0]][cState[1]]), 1):
                de = Matrix.grid[cState[0]][cState[1]][i]
                if rev:
                    nextX = revdir[de][0]+cState[0]
                    nextY = revdir[de][1]+cState[1]
                else:
                    nextX = dir[de][0]+cState[0]
                    nextY = dir[de][1]+cState[1]
                if nextX >= 0 and nextY >= 0 and nextX < Matrix.height and nextY < Matrix.width and self.dist[nextX][nextY] == INF:
                    self.dist[nextX][nextY] = 1+self.dist[cState[0]][cState[1]]
                    self.prev[nextX][nextY] = cState
                    queue.append([nextX, nextY])
                
            if cState == self.dest:
                break

    def getPath(self):          # To get next immediate Point in Path
        if self.prev[self.dest[0]][self.dest[1]] == [-1, -1]:
            return []
        else:
            res = [self.dest]
            cur = self.dest
            while self.prev[cur[0]][cur[1]] != [-1, -1]:
                res.append(self.prev[cur[0]][cur[1]])
                cur = self.prev[cur[0]][cur[1]]
            res.reverse()
            return res[1]

    def getPathLong(self):          # To get Path in Ambient Graph
        if self.source == self.dest:
                return [self.source]
        if self.prev[self.dest[0]][self.dest[1]] == [-1, -1]:
            print('Path not found')
            return []
        else:
            res = [self.dest]
            cur = self.dest
            while self.prev[cur[0]][cur[1]] != [-1, -1]:
                res.append(self.prev[cur[0]][cur[1]])
                cur = self.prev[cur[0]][cur[1]]
            res.reverse()
            return res
