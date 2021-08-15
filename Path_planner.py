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



cAgent=Search(numofrack[str((0,0,1,1))],[-1,1])
cAgent.BFS()

pickle_out= open("source_to_goal.pickle","wb")
pickle.dump(cAgent,pickle_out)
pickle_out.close()



cAgent=Search(numofrack[str((0,0,1,1))],[-1,1])
cAgent.BFS(False)

pickle_out= open("goal_to_source.pickle","wb")
pickle.dump(cAgent,pickle_out)
pickle_out.close()


