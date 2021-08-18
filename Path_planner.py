from Map_Simul import *
from AStar import Search
import pickle
import gc

gc.disable()
Counter = []
Reverse_Counter = []
for j in range(2*m):
    cAgent = Search(numofhcounter[str((int(j/m), j % m))], [-1, 1])
    cAgent.BFS(True)
    Reverse_Counter.append(cAgent)
    print("a")
    cAgent = Search(numofhcounter[str((int(j/m), j % m))], [-1, 1])
    cAgent.BFS()
    Counter.append(cAgent)
    print("b")
    print(j)

Reverse_Station = []
Station = []
station_counter = (30, 80+(n//2+n % 2)*50)
cAgent = Search(station_counter, [-1, -1])
cAgent.BFS(True)
Reverse_Station.append(cAgent)
cAgent = Search(station_counter, [-1, -1])
cAgent.BFS()
Station.append(cAgent)

# print("here")
# pickle_out= open("source_to_goal.pickle","wb")
# pickle.dump(Reverse_Counters,pickle_out,protocol=-1)
# pickle_out.close()
# print("1done")

# pickle_out= open("goal_to_source.pickle","wb")
# pickle.dump(Counters,pickle_out,protocol=-1)
# pickle_out.close()
