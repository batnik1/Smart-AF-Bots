from Map_Simul import *
import pickle
start = numofrack[str((1,0,1,1))]
goal1 = numofrack[str((0,0,1,1))]
Agent1 = Agent(start, goal1)

pickle_in = open("goal_to_source.pickle","rb")
cAgent=pickle.load(pickle_in)


pickle_in = open("source_to_goal.pickle","rb")
cAgents=pickle.load(pickle_in)


Path= cAgent.getBFSPath(numofrack[str((1,0,1,1))])
Path.reverse()
