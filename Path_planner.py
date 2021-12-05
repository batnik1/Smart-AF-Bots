"""
This file contains functions that pre-calculate the Path from each Human Counter to the Sorting Area.
Formally, we have the backend of how conveyor belt is moving order from every H-Counter to the Sorting Area.

"""
from Map_Simul import *
from AStar import *
import gc

gc.disable()
Counter = []

print('Pre-Calculating Stuff')

HCtoSorting={}
ConvUpInters=(racks_width,0)
ConvDownInters=(racks_width,racks_height+10)
target_sorting=(racks_width,(80+racks_height//2)//2+20)
#Utility Function - To Get straight line path from Point a to Point b
def goto(a,b):
    path=[]
    if a[0]==b[0]:
        y=a[1]
        while y!=b[1]+1:
            path.append((a[0],y))
            y+=1
    else:
        x=a[0]
        while x!=b[0]+1:
            path.append((x,a[1]))
            x+=1
    return path

i=m-1
x=130+120*m
while i>=0:
    x-=120
    if i==m-1:
        HCtoSorting[str((0,i))]=goto((x,0),ConvUpInters)    
    else:
        HCtoSorting[str((0,i))]=goto((x,0),(x+120,0))
        HCtoSorting[str((0,i))]+=HCtoSorting[str((0,i+1))]
    i-=1

i=m-1
x=130+120*m
while i>=0:
    x-=120
    if i==m-1:
        HCtoSorting[str((1,i))]=goto((x,racks_height+10),ConvDownInters)
    else:
        HCtoSorting[str((1,i))]=goto((x,racks_height+10),(x+120,racks_height+10))
        HCtoSorting[str((1,i))]+=HCtoSorting[str((1,i+1))]
    i-=1

common_up=goto(ConvUpInters,target_sorting)
common_down=goto(target_sorting,ConvDownInters)
common_down.reverse()

x=130

for i in range(m):
    lst=goto((x,0),(x,15))
    lst.reverse()
    HCtoSorting[str((0,i))]=lst+HCtoSorting[str((0,i))]+common_up       # To go From Common_up to target_sorting
    lst=goto((x,racks_height-5),(x,racks_height+10))
    HCtoSorting[str((1,i))]=lst+HCtoSorting[str((1,i))]+common_down  # To go From Common_down to target_sorting
    x+=120

for i in range(m):
    HCtoSorting[str((0,i))]=list(dict.fromkeys(HCtoSorting[str((0,i))]))
    HCtoSorting[str((1,i))]=list(dict.fromkeys(HCtoSorting[str((1,i))]))

print('Pre-Computation Done')
