import cv2
import numpy as np
import glob
 
img_array = []
x_arr=[]
count=0
for filename in glob.glob('./Pics/*.jpg'):
    x_arr.append(filename)
y_arr=[x_arr[i][12:] for i in range(len(x_arr))]
print(y_arr[0][:-4])
y_arr=[int(y_arr[i][:-4]) for i in range(len(y_arr))]

dis={}
for i in range(len(y_arr)):
    dis[y_arr[i]]=i
y_arr.sort()
#print(dis)
pro=0
count=0
for fil in range(len(y_arr)):
    count+=1
    filename='./Pics/image'+str(y_arr[fil])+'.jpg'

    # filename=x_arr[dis[y_arr[fil]]]
   # print(filename)
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
    if count%500==0:
        out = cv2.VideoWriter('project'+str(pro)+'.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
        pro+=1
        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()
        img_array.clear()
        img_array=[]
out = cv2.VideoWriter('project'+str(pro)+'.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

for i in range(len(img_array)):
    out.write(img_array[i])
out.release()