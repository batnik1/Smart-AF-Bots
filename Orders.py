"""
Which rack has which item

total items in workshop, item type id in :{all the racks that have it}


Item - Item  type Id ,Item ID, Rack Numbers in which it is stored
 
Gen_order():
  rand item id

Call_Truck():
    for item in type of items:
        d=rand_quantity()


"""

import time
import collections
# from Map_Simul import *
import random
# def generate_order():
#     item = rand() % num_of_items
#     quant = rand() % 10
#     return (item, quant)

import pymongo
from pymongo import MongoClient
connection=MongoClient('localhost',27017)

db=connection['amazon']
collection=db["big_database"]
delivered=db["delivered"]
#rack_collection=db["rack_shelf"]

collection.drop()

#find if already there increment it, if not there then put it


def random_order():
  racks_to_send=collections.deque()
  for document in collection.find():
    quantity=document["quantity"]
    order_quantity=random.randint(0,1)
    collection.update_one({"type":document["type"]},{"$inc":{"quantity":-1*order_quantity}})
    i=0
    while order_quantity!=0 and i < len(document["shelves"]):
      if document["shelves"][i]["quantity"] > order_quantity:
        collection.update_one({"type":document["type"],"shelves.shelf":document["shelves"][i]["shelf"]},{"$inc":{"shelves.$.quantity":-1*order_quantity}})      
        order_quantity=0
      else:
        collection.update_one({"type":document["type"]},{"$pull":{"shelves":{"shelf":document["shelves"][i]["shelf"], "quantity":document["shelves"][i]["quantity"]}}})
        order_quantity-=document["shelves"][i]["quantity"] 
      racks_to_send.append(document["shelves"][i]["shelf"])
      i+=1
  return racks_to_send



for i in range(10):
  type=random.randint(0,1)
  quantity=random.randint(1,3)
  shelf=str((random.randint(0, 3), random.randint(0,3), random.randint(0, 4), random.randint(0, 4)))
  if collection.find_one({"type":type}):
    collection.update_one({"type":type},{"$inc":{"quantity":quantity}})
    collection.update_one({"type":type},{"$push":{"shelves":{"shelf":shelf, "quantity":quantity}}}) 
  else:
    collection.insert_one({"type":type, "quantity":quantity, "shelves":[{"shelf":shelf, "quantity":quantity}]})

