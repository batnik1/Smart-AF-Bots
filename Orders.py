"""
This file contains functions to do the following tasks:
1) Random Order Generation
2) Adding Items into DB

"""
import uuid
from Map_Simul import *
import random
random.seed(2500)
import numpy as np
import logging

import pymongo
from pymongo import MongoClient
connection = MongoClient('localhost', 27017)

item_types_in_db = set()  # List of all item type which have non zero quantity in our DB

db = connection['Warehouse']
collection = db["big_database"]
order_db = db["order_db"]
order_history = db["order_history"]

order_db.drop()
collection.drop()

type_of_items = config['type_of_items']
max_diff_item = config['max_diff_item']
max_order_limit = config['max_order_limit']
initial_items= config['initial_items']
# Creating Log File
logging.basicConfig(filename="Warehouse.log",format='%(asctime)s %(message)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# After we get the list of Orders which is of form (Item,Quantity) , here the function returns the list of racks on which those items lie.
def assign_rack(orders):    
  racks_dict={}
  for order in orders:
    docker=collection.find({"type":order[0]})
    target=order[1]
    lst=[]
    collection.update_one({"type":order[0]},{"$inc":{"quantity":-1*target}})   
    for nobj in list(docker):
        for obj in nobj['shelves']:
          shelf=obj['shelf']
          quant=obj['quantity']
          lst.append([quant,shelf])
        lst.sort(reverse=True)
        for j in range(len(lst)):
          if lst[j][0]>target:
            collection.update_one({"type":order[0],"shelves.shelf":lst[j][1]},{"$inc":{"shelves.$.quantity":-1*target}})  
            if lst[j][1] in racks_dict:
              racks_dict[lst[j][1]].append([order[0],target])
            else:
              racks_dict[lst[j][1]]=[[order[0],target]]
            target=0
          else:
            target-=lst[j][0]
            collection.update_one({"type":order[0]},{"$pull":{"shelves":{"shelf":lst[j][1], "quantity":lst[j][0]}}})
            if lst[j][1] in racks_dict:
              racks_dict[lst[j][1]].append([order[0],lst[j][0]])
            else:
              racks_dict[lst[j][1]]=[[order[0],lst[j][0]]]
          if target<=0:
            break
            
    if collection.find_one({"type":order[0]}): 
      if collection.find_one({"type":order[0]})["quantity"]==0:
        collection.delete_one({"type":order[0]})

  return racks_dict

# To generate a random order by initializing all the fields required (Order ID , Human Counter Index , List of Racks)
def gen_a_order(): 
  global item_types_in_db
  num_types_ordered=random.randint(1,max_diff_item)
  order=[]
  sum=0  
  types_chosen=random.sample(item_types_in_db,min(num_types_ordered,len(item_types_in_db)))
  for type in types_chosen:
    if collection.find_one({"type":type}):
      quant=collection.find_one({"type":type})["quantity"]
      low=1
      high=min(max_order_limit,quant)
      if low>high:
        continue
      order.append([type,random.randint(low,high)])
      sum+=order[-1][1]
      
  racks=assign_rack(order)
  
  human_counter= random.randint(0,2*m-1)
  order_id=str(uuid.uuid4())
  if len(order)==0:
    return "Nothing"
  sorting_random=(random.randint(0,2*sorting_n-3),random.randint(0,2*sorting_m-3))
  logger.info('New Order'+','+str(order_id)+','+'-'+','+'-'+','+'New Order is Placed.')
  order_db.insert_one({"_id":order_id,"order_progress":0,"ordered_quantity":sum,"Target_Racks":racks,"human_counter":human_counter})  
  order_history.insert_one({"_id":order_id,"ordered":order,"address":sorting_random})  
  return (racks,human_counter,order_id)  



# This function is to add ay arbitary number of items in warehouse on random racks with random quantity.
def add_items(count):
  global item_types_in_db
  for _ in range(count):
    type=random.randint(0,type_of_items)
    item_types_in_db.add(type)
    quantity=random.randint(1,max_order_limit)
    shelf=str((random.randint(0, n-1), random.randint(0,m-1), random.randint(0, 4), random.randint(0, 4)))
    if collection.find_one({"type":type}):
      collection.update_one({"type":type},{"$inc":{"quantity":quantity}})
      if collection.find_one({"type":type, "shelves":{"$elemMatch":{"shelf":shelf}}}):
        collection.update_one({"type":type,"shelves.shelf":shelf},{"$inc":{"shelves.$.quantity":quantity}})
      else:
        collection.update_one({"type":type},{"$push":{"shelves":{"shelf":shelf, "quantity":quantity}}}) 
    else:
      collection.insert_one({"type":type, "quantity":quantity, "shelves":[{"shelf":shelf, "quantity":quantity}]})
  return item_types_in_db

# This function is to update the DB when Truck bots arrive to racks with new items
def add_item(type, quantity, shelf):
    global item_types_in_db
    item_types_in_db.add(type)
    if collection.find_one({"type": type}):
        collection.update_one({"type": type}, {"$inc": {"quantity": quantity}})
        if collection.find_one({"type": type, "shelves": {"$elemMatch": {"shelf": shelf}}}):
            collection.update_one({"type": type, "shelves.shelf": shelf}, {
                                  "$inc": {"shelves.$.quantity": quantity}})
        else:
            collection.update_one(
                {"type": type}, {"$push": {"shelves": {"shelf": shelf, "quantity": quantity}}})
    else:
        collection.insert_one({"type": type, "quantity": quantity, "shelves": [
                              {"shelf": shelf, "quantity": quantity}]})


add_items(initial_items)    # Adding some Items initially in Warehouse so that Bots don't have to sit idle

# total items in warehouse
total_items=0
for obj in collection.find():
  total_items+=obj["quantity"]
print("Total Items in Warehouse:",total_items)
# input()