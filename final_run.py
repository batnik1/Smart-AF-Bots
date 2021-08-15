from Map_Simul import *
import pickle
start = numofrack[str((1,0,1,1))]
goal1 = numofrack[str((0,0,1,1))]
Agent1 = Agent(start, goal1)

print("here to load 2")

pickle_in = open("source_to_goal.pickle","rb")
Reverse_Counter=pickle.load(pickle_in)


print("here to load 1")
pickle_in = open("goal_to_source.pickle","rb")
Counter=pickle.load(pickle_in)

print("loaded successfully")

which_counter=0

#Path.reverse()
