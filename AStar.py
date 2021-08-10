from queue import PriorityQueue
import math ,heapq
import queue
import collections
from Grid import Grid
from Make_map import Matrix
def ManhattanDistance(start,end):
        return abs(start[0]-end[0])+abs(start[1]-end[1])

dx4=[(-1,0),(0,-1),(1,0),(0,1)]
INF=int(1e12)

N=1600
class Search():
   
    def __init__(self,source,destination):
        self.heap=[]
        self.source=source
        self.dest=destination
        self.dist=[[INF for i in range(N)] for j in range(N)]
        self.prev=[[[-1,-1] for i in range(N)] for j in range(N)]
    
    def AStar(self):
        heapq.heappush(self.heap,(ManhattanDistance(self.source,self.dest),self.source))   # Cost,x,y   
        self.dist[self.source[0]][self.source[1]]= ManhattanDistance(self.source,self.dest)
        while len(self.heap)>0:
            (d,cState)=heapq.heappop(self.heap)
            if d >self.dist[cState[0]][cState[1]]:
                continue
            if cState==self.dest:
                break
            
            for (x,y) in dx4:
                nextX=x+cState[0]
                nextY=y+cState[1]
                if nextX>=0 and nextY>=0 and nextX<Matrix.height and nextY<Matrix.width and Matrix.grid[nextX][nextY]==1:
                    if self.dist[nextX][nextY]> d+ManhattanDistance([nextX,nextY],self.dest)+1:
                        self.dist[nextX][nextY]=d+ManhattanDistance([nextX,nextY],self.dest)+1
                        self.prev[nextX][nextY]=cState
                        heapq.heappush(self.heap,(self.dist[nextX][nextY],[nextX,nextY]))
    
    def BFS(self):
        queue = collections.deque([self.source])
        self.dist[self.source[0]][self.source[1]]=0
        while queue: 
            cState = queue.popleft()
            if cState==self.dest:
                break
            for (x,y) in dx4:
                nextX=x+cState[0]
                nextY=y+cState[1] 
                if nextX>=0 and nextY>=0 and nextX<Matrix.height and nextY<Matrix.width and Matrix.grid[nextX][nextY]==1 and self.dist[nextX][nextY]==INF: 
                    self.dist[nextX][nextY]=1+self.dist[cState[0]][cState[1]]
                    self.prev[nextX][nextY]=cState
                    queue.append([nextX,nextY])


    def getPath(self):
        if self.prev[self.dest[0]][self.dest[1]]==[-1,-1]:
            print("Not Possible")
            return []
        else:
            res=[self.dest]
            cur=self.dest
            while self.prev[cur[0]][cur[1]]!=[-1,-1]:
                res.append(self.prev[cur[0]][cur[1]])
                cur=self.prev[cur[0]][cur[1]]
            res.reverse()
            print("Solution Exists")
            return res