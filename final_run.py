#from Map_Simul import *
from Path_planner import *
import pymongo
from pymongo import MongoClient
connection=MongoClient('localhost',27017)

db=connection['amazon']
collection=db["item shelf"]

for i in range(2*m):
    collection.update_one({"_id":i},{"$set": {"score":0}})

import gc
gc.disable()

# print("here to load 2")

# pickle_in = open("source_to_goal.pickle","rb")
# Reverse_Counter=pickle.load(pickle_in)


# print("here to load 1")
# pickle_in = open("goal_to_source.pickle","rb")
# Counter=pickle.load(pickle_in)

# print("loaded successfully")

which_counter=0

#Path.reverse()
