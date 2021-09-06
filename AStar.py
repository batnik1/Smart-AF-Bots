from queue import PriorityQueue
import math
import heapq
import queue
import collections
from Grid import Grid
import time

def ManhattanDistance(start, end):
    return abs(start[0]-end[0])+abs(start[1]-end[1])


dx4 = [(-1, 0), (0, -1), (1, 0), (0, 1)]
INF = int(100000)
dir = [(-1, -1), (0, -1), (0, 1), (1, 0), (-1, 0)]      # (-1,-1) is just pushed to make it 1 based indexing
revdir = [(-1, -1), (0, 1), (0, -1), (-1, 0), (1, 0)]


N = 1000

diss = [[INF for i in range(N)] for j in range(N)]
press = [[[-1, -1] for i in range(N)] for j in range(N)]



Matrix = Grid(N, N)


class Search(): 

    def __init__(self, source, destination):
        self.heap = []
        self.source = source
        self.dest = destination
        start=time.perf_counter()
        self.dist=[x[:] for x in diss]
        self.prev=[x[:] for x in press]
        # self.dist = [[INF for i in range(N)] for j in range(N)]
        # self.prev = [[[-1, -1] for i in range(N)] for j in range(N)]
        end=time.perf_counter()
        #print(end-start)

    def AStarModif(self, sources):
        for k in range(0, len(sources)):
            heapq.heappush(self.heap, (ManhattanDistance(
                sources[k], self.dest), sources[k]))
            self.dist[sources[k][0]][sources[k][1]
                                     ] = ManhattanDistance(sources[k], self.dest)
        while len(self.heap) > 0:
            (d, cState) = heapq.heappop(self.heap)
            if d > self.dist[cState[0]][cState[1]]:
                continue
            if cState == self.dest:
                break
            # print(cState[0],cState[1],Matrix.grid[cState[0]][cState[1]],"bete")
            for i in range(1, len(Matrix.grid[cState[0]][cState[1]]), 1):
                de = Matrix.grid[cState[0]][cState[1]][i]
                # print(d)
                nextX = dir[de][0]+cState[0]
                nextY = dir[de][1]+cState[1]
                if nextX >= 0 and nextY >= 0 and nextX < Matrix.height and nextY < Matrix.width:
                    if self.dist[nextX][nextY] > d+ManhattanDistance([nextX, nextY], self.dest)+1:
                        self.dist[nextX][nextY] = d + \
                            ManhattanDistance([nextX, nextY], self.dest)+1
                        self.prev[nextX][nextY] = cState
                        heapq.heappush(
                            self.heap, (self.dist[nextX][nextY], [nextX, nextY]))

    def AStar(self):
        heapq.heappush(self.heap, (ManhattanDistance(
            self.source, self.dest), self.source))   # Cost,x,y
        self.dist[self.source[0]][self.source[1]
                                  ] = ManhattanDistance(self.source, self.dest)
        while len(self.heap) > 0:
            (d, cState) = heapq.heappop(self.heap)
            if d > self.dist[cState[0]][cState[1]]:
                continue
            if cState == self.dest:
                break

            for (x, y) in dx4:
                nextX = x+cState[0]
                nextY = y+cState[1]
                if nextX >= 0 and nextY >= 0 and nextX < Matrix.height and nextY < Matrix.width and Matrix.grid[nextX][nextY] == 1:
                    if self.dist[nextX][nextY]-ManhattanDistance([nextX, nextY], self.dest) > d-ManhattanDistance([cState[0], cState[1]], self.dest)+1:
                        self.dist[nextX][nextY] = d -ManhattanDistance([cState[0], cState[1]], self.dest)+ ManhattanDistance([nextX, nextY], self.dest)+1
                        self.prev[nextX][nextY] = cState
                        heapq.heappush(
                            self.heap, (self.dist[nextX][nextY], [nextX, nextY]))

    # def getPrev

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

    def getPath(self):
        if self.prev[self.dest[0]][self.dest[1]] == [-1, -1]:
            #print("Not Possible")
            return []
        else:
            res = [self.dest]
            cur = self.dest
            while self.prev[cur[0]][cur[1]] != [-1, -1]:
                res.append(self.prev[cur[0]][cur[1]])
                cur = self.prev[cur[0]][cur[1]]
            res.reverse()
            # print("Solution Exists")
            return res

    def getBFSPath(self, destiny):
        if self.prev[destiny[0]][destiny[1]] == [-1, -1]:
            #print("Not Possible")
            return []
        else:
            res = [destiny]
            cur = destiny
            while self.prev[cur[0]][cur[1]] != [-1, -1]:
                res.append(self.prev[cur[0]][cur[1]])
                cur = self.prev[cur[0]][cur[1]]
            res.reverse()
            # print("Solution Exists")
            return res
