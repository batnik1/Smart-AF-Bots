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

import re
import time
import collections
# from Map_Simul import *
import random
import numpy as np
from numpy.random.mtrand import rand
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
order_db=db["order_db"]
#rack_collection=db["rack_shelf"]

order_db.drop()
collection.drop()


type_of_items=2
max_order_limit=4


def random_order():
  racks_to_send=collections.deque()
  for document in collection.find():
    quantity=document["quantity"]
    order_quantity=1
    collection.update_one({"type":document["type"]},{"$inc":{"quantity":-1*order_quantity}})
    i=0
    while order_quantity!=0:
      if document["shelves"][i]["quantity"] > order_quantity:
        collection.update_one({"type":document["type"],"shelves.shelf":document["shelves"][i]["shelf"]},{"$inc":{"shelves.$.quantity":-1*order_quantity}})      
        racks_to_send.append((document["shelves"][i]["shelf"],(document["type"],order_quantity)))
        order_quantity=0
      else:
        order_quantity-=document["shelves"][i]["quantity"] 
        collection.update_one({"type":document["type"]},{"$pull":{"shelves":{"shelf":document["shelves"][i]["shelf"], "quantity":document["shelves"][i]["quantity"]}}})
        racks_to_send.append((document["shelves"][i]["shelf"],(document["type"],document["shelves"][i]["quantity"])))
      i+=1
  return racks_to_send


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
          if lst[j][0]==0:
            print('Repeat')
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
    if collection.find_one({"type":order[0]})["quantity"]==0:
      collection.delete_one({"type":order[0]})
      # print(100)
  return racks_dict

def gen_a_order(): 
  num_types_ordered=random.randint(1,3)

  order=[]
  sum=0  
  flg=0
  while flg==0:
    types_chosen=random.sample(range(0,type_of_items),min(num_types_ordered,type_of_items))
    for type in types_chosen:
      if collection.find_one({"type":type}):
        flg=1
        quant=collection.find_one({"type":type})["quantity"]
        order.append([type,random.randint(1,min(max_order_limit,quant))])
        sum+=order[-1][1]
      
  racks=assign_rack(order)
  print(racks,order,sep='\t')
  order_db.insert_one({"order_progress":0,"ordered_quantity":sum,"Target_Racks":racks})  
  return racks


def add_items(count):
  for _ in range(count):
    type=random.randint(0,type_of_items)
    quantity=random.randint(1,3)
    shelf=str((random.randint(0, 3), random.randint(0,3), random.randint(0, 4), random.randint(0, 4)))
    shelf=str((1,1,1,1))
    if collection.find_one({"type":type}):
      collection.update_one({"type":type},{"$inc":{"quantity":quantity}})
      if collection.find_one({"type":type, "shelves":{"$elemMatch":{"shelf":shelf}}}):
        collection.update_one({"type":type,"shelves.shelf":shelf},{"$inc":{"shelves.$.quantity":quantity}})
      else:
        collection.update_one({"type":type},{"$push":{"shelves":{"shelf":shelf, "quantity":quantity}}}) 
    else:
      collection.insert_one({"type":type, "quantity":quantity, "shelves":[{"shelf":shelf, "quantity":quantity}]})


add_items(100)
gen_a_order()
#print(racks)