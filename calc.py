import sys
from os import path
if(path.exists('read.txt')):
     sys.stdin = open('read.txt','r')

sum100,sum200,sum300=0,0,0
maxi=0
a,b,c=[],[],[]
for i in range(30):
    d=input().split(' ')
    print(d[11],d[-1])
    if d[11]=='100':
        a.append(int(d[-1]))
        sum100+=int(d[-1])
    elif d[11]=='200':
        sum200+=int(d[-1])
        b.append((int(d[-1])))
    else:
        sum300+=int(d[-1])
        c.append(int(d[-1]))

# sum300-=maxi
# a.sort()
# b.sort()
# c.sort()
# sum100-=a[-1]+a[-2]+a[-3]+a[-4]+a[-5]
# sum200-=b[-1]+b[-2]+b[-3]+b[-4]+b[-5]
# sum300-=c[-1]+c[-2]+c[-3]

sum100/=10
sum200/=10
sum300/=10

print(sum100,sum200,sum300)