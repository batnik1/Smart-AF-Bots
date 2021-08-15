from Map_Simul import *
from AStar import Search
import pickle

# allRacks=[]
# print(n,m)
# for i in range(n):
#     for j in range(m):
#         for k in range(5):
#             for l in range(5):
#                 allRacks.append(numofrack[str((i,j,k,l))])
#                 print(str((i,j,k,l)))

Counters=[]
Reverse_Counters=[]
for j in range(2*m):
  cAgent=Search(numofhcounter[str((int(j/m),j%m))],[-1,1])
  cAgent.BFS(True)
  Reverse_Counters.append(cAgent)
  print("a")
  cAgent=Search(numofhcounter[str((int(j/m),j%m))],[-1,1])
  cAgent.BFS()
  Counters.append(cAgent)
  print("b")
  print(j)

print("here")
pickle_out= open("source_to_goal.pickle","wb")
pickle.dump(Reverse_Counters,pickle_out)
pickle_out.close()
print("1done")

pickle_out= open("goal_to_source.pickle","wb")
pickle.dump(Counters,pickle_out)
pickle_out.close()


