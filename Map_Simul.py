import pygame
from Agent007 import Agent
from Grid import Grid
import AStar
from AStar import Search,Matrix,Golden_Grid
import colors
from collections import defaultdict,deque
import yaml

import time

# get configs
def get_config(config):
    with open(config, 'r') as stream:
        return yaml.load(stream,yaml.SafeLoader)

config = get_config('parameters.yaml')


Intersections=[]

m = config['m']   # width
n = config['n']  # height     (n,m)>=2
sorting_m=config['sorting_m']
sorting_n=config['sorting_n']




display_width = 120*m+800
display_height = 120*n+300
racks_height = 120*n+160
racks_width = 120*m+160

# Availability Checking of Racks using rack_available dictionary
rack_available=defaultdict(int)
def rack_available_fn():
    for i in range(m):
        for j in range(n):
            for k in range(5):
                for l in range(5):
                    rack_available[str((i,j,k,l))]=1

rack_available_fn()
extras=[]
for i in range(m):
    for j in range(n):
        for k in range(5):
            for l in range(5):
                if rack_available[str((i,j,k,l))]!=1:
                    print(rack_available[str((i,j,k,l))])
                    extras.append(str((i,j,k,l)))

israck={}
# position of racks calculated 
numofrack={}
def num_racks(xx,xxx):
    for i in range(m):
        for j in range(n):
            for l in range(5):
                numofrack[str((i,j,0,l))]=(120*i+90,120*j+105+20*l)
                israck[(120*i+90,120*j+105+20*l)]=1
                numofrack[str((i,j,1,l))]=(25+numofrack[str((i,j,0,0))][0],l*20+numofrack[str((i,j,0,0))][1])
                israck[(25+numofrack[str((i,j,0,0))][0],l*20+numofrack[str((i,j,0,0))][1])]=1
                for k in range(2,5):
                    numofrack[str((i,j,k,l))]=((k-1)*20+numofrack[str((i,j,1,0))][0],numofrack[str((i,j,1,l))][1])
                    israck[((k-1)*20+numofrack[str((i,j,1,0))][0],numofrack[str((i,j,1,l))][1])]=1
num_racks(n,m)
#Dumping location 
numofdump={}
isdump={}
def numofdumping():
    x=racks_width+20
    for i in range(2*sorting_m-1):
        y=80
        for j in range(2*sorting_n-1):
            numofdump[str((j,i))]=(x-10,y+25)
            isdump[(x-10,y+25)]=1
            y+=30
        x+=30

numofdumping()
numofdump["conveyor"]=(racks_width-40,(80+racks_height//2)//2+10)

# Human counter location
numofhcounter={}
def num_hcounter(n,m):
    for i in range(2):
        for j in range(m):
            numofhcounter[str((i,j))]=(90+120*j+i*(80), i*(120*(n+1)-40)+45)
num_hcounter(n,m)
# pygame.display.set_caption("Warehouse Simulation V1.0")


# waste 1,2,3 for making roadmap
def waste3(x, y, dir):
    if x:
        add_edge((x, 80), (x, racks_height-70),dir)
    elif y:
        add_edge((80, y), (racks_width-70, y),dir)


def waste1(n,m):
    y = 100
    for ro in range(0, n):
        x = 100
        for cols in range(0, m):
            marking_line(x, y)
            x += 120
        y += 120

def waste2(n, m):
    x = 80
    for _ in range(m+1):
        waste3(x,0,direction["up"])
        waste3(x+10, 0, direction["down"])  # down
        x += 120
    y = 80
    for _ in range(n+1):
        waste3(0, y, direction["right"])  # right
        waste3(0, y+10, direction["left"])  # left
        y += 120


# Direction dictionary
direction = {}
direction["up"] = 1
direction["down"] = 2
direction["right"] = 3
direction["left"] = 4


# add edge function to make connectivity edge between two points in a particualr direction
def add_edge(X, Y, dir):
    if X[0] == Y[0]:
        for i in range(X[1], Y[1]+1, 1):
            Matrix.grid[X[0]][i].append(dir)
    else:
        for i in range(X[0], Y[0]+1, 1):
            Matrix.grid[i][X[1]].append(dir)


# Making the sorting area
def marking_line(x,y):
    add_edge((x+15,y-10),(x+15,y+100),direction["up"])
    add_edge((x+55,y-10),(x+55,y+100),direction["up"])
    add_edge((x+35,y-10),(x+35,y+100),direction["down"])
    add_edge((x+75,y-10),(x+75,y+100),direction["down"])
    add_edge((x-10,y+15),(x+100,y+15),direction["right"])
    add_edge((x-10,y+55),(x+100,y+55),direction["right"])
    add_edge((x-10,y+35),(x+100,y+35),direction["left"])
    add_edge((x-10,y+75),(x+100,y+75),direction["left"])

def marking_queue_line(n,m):
    x=90
    for i in range(m):
        add_edge((x, 10), (x, 80),direction["down"])
        add_edge((x+80,10),(x+80,80),direction["up"])
        add_edge((x, 10), (x+80,10),direction["left"])
        x+=120
    x=90
    for i in range(m):
        add_edge((x, 120*(n+1)-30), (x, 40+120*(n+1)),direction["down"])
        add_edge((x+80, 120*(n+1)-30), (x+80, 40+120*(n+1)),direction["up"])
        add_edge((x, 40+120*(n+1)), (x+80,40+120*(n+1)),direction["right"])
        x+=120

truck_resting={}
def marking_station_line():
    add_edge((30, 80), (80, 80),direction["left"])
    add_edge((30, (n//2+n%2)*100), ((80, (n//2+n%2)*100)),direction["right"])
    add_edge((30,80) , (30, (n//2+n%2)*100),direction["down"])
    countin=0
    for y in range(80+10,(n//2+n % 2)*100,10):
        add_edge((30, y), (80,y),direction["right"])
        truck_resting[countin]=(55,y)
        countin+=1
    

# Making the conveyor belt
def waste_conveyor_belt():
    # add_edge((130, 0), (racks_width, 0),direction["right"])
    # add_edge((130, racks_height+10), (racks_width, racks_height+10),direction["right"])
    # add_edge((racks_width, 0),(racks_width,(80+racks_height//2)//2+20),direction["down"])
    # add_edge((racks_width,(80+racks_height//2)//2+20), (racks_width, racks_height+10),direction["up"])
    x=130
    for _ in range(m):
        add_edge((x,1),(x,15),direction["up"])
        add_edge((x, racks_height-5), (x,racks_height+9),direction["down"])
        x+=120

# Making the charging area add_edge((130, 0), (racks_width, 0),direction["right"])
    add_edge((130, racks_height+10), (racks_width, racks_height+10),direction["right"])
    add_edge((racks_width, 0),(racks_width,(80+racks_height//2)//2+20),direction["down"])
   
def waste_charging():
    for i in range((n//2+n % 2)*100+20,racks_height-90,10):
        add_edge((30,i),(80,i),direction["right"])

    add_edge((30, (n//2+n % 2)*100+10), (80, (n//2+n % 2)*100+10),direction["left"])
    add_edge((30, racks_height-90), (80, racks_height-90),direction["right"])
    add_edge((30, (n//2+n % 2)*100+10), (30, racks_height-90),direction["down"])

# making the connectivity lanes in sorting area
def waste_sorting_area():
    sorting_w=sorting_m*60+20
    sorting_h=sorting_n*60+20
    
    # add_edge((racks_width,80),(sorting_w+racks_width,80),direction["left"])
    # add_edge((racks_width,sorting_h+80),(sorting_w+racks_width,sorting_h+80),direction["right"])
    # add_edge((sorting_w+racks_width,80),(sorting_w+racks_width,sorting_h+80),direction["down"])
 #   add_edge((sorting_w+racks_width,80),(sorting_w+racks_width,sorting_h+80),direction["up"])


    add_edge((racks_width-40,(80+racks_height//2)//2-20),(racks_width+10,(80+racks_height//2)//2-20),direction["left"]) #left queue
    add_edge((racks_width-40,int((80+racks_height//2)//2+70)),(racks_width+10,int((80+racks_height//2)//2+70)),direction["right"]) #right queue
    add_edge((racks_width-40,int((80+racks_height//2)//2-20)),(racks_width-40,int((80+racks_height//2)/2+70)),direction["down"]) #down queue
    #pygame.draw.line(screen,colors.RED,(racks_width,(80+racks_height//2)/2-25),(racks_width-25,(80+racks_height//2)/2-25),width=2)    # Left
    # pygame.draw.line(screen,colors.BLUE,(racks_width-25,(80+racks_height//2)/2+20),(racks_width,(80+racks_height//2)/2+20),width=2)    # Right
    # pygame.draw.line(screen,colors.BLUE,(racks_width-25,(80+racks_height//2)/2-25),(racks_width-25,(80+racks_height//2)/2+20),width=2)             #Down

    # (n+1)*15+n*10=sorting_n*100+15
    # (m+1)*15+m*10=sorting_m*100+15
    # x=racks_width+20

    # x=racks_width+10
    # y=80
    # for _ in range(sorting_m+1):    
    #     add_edge((x, 80),(x,sorting_h+80),direction["up"])
    #     x+=60
    
    # x=racks_width+40
    # for _ in range(sorting_m):
    #     add_edge((x, 80),(x,sorting_h+80),direction["down"])
    #     x+=60
    
    # for _ in range(sorting_n+1):
    #     add_edge((racks_width, y+10),(racks_width+sorting_w,y+10),direction["right"])
    #     y+=60
    # y=110
    # for _ in range(sorting_n):
    #     add_edge((racks_width, y+10),(racks_width+sorting_w,y+10),direction["left"])
    #     y+=60
    lis_hori=[]
    x=racks_width+10
    y=80
    for i in range(2*sorting_m):
        lis_hori.append(((x,90),(x,sorting_h+40)))
        x+=30
    lis_vert=[]
    for i in range(2*sorting_n):
        lis_vert.append(((racks_width+10,y+10),(racks_width+sorting_w-40,y+10)))
        y+=30
    # lis_vert=lis_vert[:-1]
    # lis_hori=lis_hori[:-1]
    alt=1
    for i in range(len(lis_hori)):
        if alt==1:
            direct=direction["up"]
        else:
            direct=direction["down"]
        add_edge(lis_hori[i][0],lis_hori[i][1],direct)
        alt*=-1
    alt=1
    for i in range(len(lis_vert)):
        
        if alt==1:
            direct=direction["right"]
        else:
            direct=direction["left"]
        add_edge(lis_vert[i][0],lis_vert[i][1],direct)
        alt*=-1
new_praylist=[]
# Assigning directions to all interesections
def duplicate_grid():

    for i,j in Intersections:
            cnt=[0]*5
            updated=[]
            for d in Matrix.grid[i][j]:
                if cnt[d]==0:
                    updated.append(d)
                    cnt[d]+=1
            Matrix.grid[i][j]=updated.copy()           

waste1(n, m)
waste2(n,m)
marking_queue_line(n,m)
# waste_conveyor_belt()
waste_sorting_area()
waste_charging()
marking_station_line()


# Calculating Intersections
stack=[]
for i in range(1500):
    for j in range(1500):
        #print(len(Matrix.grid[i][j]))
        if len(list(set(Matrix.grid[i][j])))>2:
            stack.append((i,j))
            Intersections.append((i,j))
           # print("AA")

duplicate_grid()
my_list=[(-1,-1),(-1,-1),(-1,-1),(-1,-1),(-1,-1)]
# for i in range(N):
#     for j in range(N):
#         Golden_Grid[(i,j)]=my_list

dir = [(-1, -1), (0, -1), (0, 1), (1, 0), (-1, 0)]      # (-1,- 1) is just pushed to make it 1 based indexing
revdir = [(-1, -1), (0, 1), (0, -1), (-1, 0), (1, 0)]
leftorightindexing=[-1,2,1,4,3]
# revdir = [(-1, -1), (0, 1), (0, -1), (-1, 0), (1, 0)]
for i,j in Intersections:
    Golden_Grid[(i,j)]=[(),(),(),()]   #Up,Down,Right,Left

# make a small rectangle for each intersection
pradius=[]
count=0
vis={}


# BFS on our ambient workspace
while len(stack):
    x,y=stack.pop()
    if (x,y) in vis:
        continue
    vis[(x,y)]=1

    for pops in range(1,5):

        if (pops in Matrix.grid[x][y]):
            
            i,j=x,y
            eligible=1

            while i >= 0 and j >= 0 and i < Matrix.height and j < Matrix.width:
                if pops not in Matrix.grid[i][j]:
                    # print("Fucked",(i,j))
                    eligible=0
                    break
                if (i,j)!=(x,y) and (i,j) in Intersections:
                    break
                i+=dir[pops][0]
                j+=dir[pops][1]
                
            if eligible and (i,j)!=(x,y):
                Golden_Grid[(x,y)][pops-1]=(i,j)
               # Golden_Grid[(i,j)][leftorightindexing[pops]-1]=(x,y)
                if i >= 0 and j >= 0 and i < Matrix.height and j < Matrix.width:
                    stack.append((i,j))
                





def ged(x):
    if x>0:
        return 1
    else:
        return 0
# Make a dictionary for intersections
Intersec_dic=defaultdict(int)
Position_Booking=defaultdict(int)
# Index_Booking=defaultdict(int)
Intersection_Gateway={}
Intersection_Timeout={}
Intersection_Booking={}
Intersection_Bot={}
# Assigning default directions to all intersections
for i,j in Intersections:
    # if ged(len(Golden_Grid[i,j][0]))+ged(len(Golden_Grid[i,j][1]))+ged(len(Golden_Grid[i,j][2]))+ged(len(Golden_Grid[i,j][3]))==4:
    Intersec_dic[(i,j)]=1
    Intersection_Gateway[(i,j)]=[0]*5
    Intersection_Timeout[(i,j)]=50
    Intersection_Booking[(i,j)]=-1
    Intersection_Bot[(i,j)]=Agent(0,n,m)
    Intersection_Bot[(i,j)].l=2
    Intersection_Bot[(i,j)].position=(i,j)

# Calculating nearest_intersection from our ambient workspace into our roadmap
def nearest_intersection(source,rev=False):
    source=tuple(source)
    stack=[source]
    vis={}
    while(len(stack)): 
        node = stack.pop()
        if node in Intersections:
            return node
        if node in vis:
            continue

        vis[node]=1

        for d in Matrix.grid[node[0]][node[1]]:
            if d==0:
                continue
            if rev:
                (x,y)=(node[0]+revdir[d][0],node[1]+revdir[d][1])
            else:
                (x,y)=(node[0]+dir[d][0],node[1]+dir[d][1])
            if (x,y) not in vis:
                stack.append((x,y))    
    return None

# Returning the path from earlier function
def nearest_intersection_path(source,destination):
    if source==None or destination==None:
        return []
    x1,y1=source
    x2,y2=destination
    if source==destination:
        return []
    if x1==x2:
        path=[]
        if y2>y1:
            path=list(range(y2,y1,-1))
        else:
            path=list(range(y2,y1))
        #path.reverse()            
        return list(zip([x1]*len(path),path))
    elif y1==y2:
        path=[]
        if x2>x1:
            path=list(range(x2,x1,-1))
        else:
            path=list(range(x2,x1))
        return list(zip(path,[y1]*len(path)))


Roads_Grid=defaultdict(list)
Roads_lr=defaultdict(int)

def divide_roads():
    for i,j in Intersections:
        for nebr in Golden_Grid[(i,j)]:
            if ((i,j),nebr) not in Roads_lr:
                Roads_lr[((i,j),nebr)]=1
                Roads_lr[(nebr,(i,j))]=-1


divide_roads()
