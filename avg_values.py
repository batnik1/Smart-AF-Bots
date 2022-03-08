density_dic={}
import numpy as np
# open Density_vs_Velocity and use avg_density dictionary to store avg_velocities
with open('Density_vs_Velocitysss','r') as f:
    for line in f:
        line=line.strip().split(',')
       # print(line)
        if line[1]=="density":
            continue
        #print(line)
        density_dic[float(line[1])]=float(line[0])

# print(density_dic)
# density= all the density values
density=list(density_dic.keys())
# sort them in ascending order
density.sort()
# print them one after other with their avg velocity
X_Y=[(density[i],density_dic[density[i]]) for i in range(len(density))]
# for i in density:
#     print(i,density_dic[i])
 
 # draw a graph for the same with mathplotlib

import matplotlib.pyplot as plt
X=[i[0] for i in X_Y]
Y=[i[1] for i in X_Y]
# plt.plot(X,Y)
# plt.xlabel('Density')
# plt.ylabel('Average Velocity')
# plt.title('Density vs Average Velocity')
# plt.show()

# density_vs_flow_dic={}
# new_X_Y=[(density[i],density[i]*density_dic[density[i]]) for i in range(len(density))]
# X=[i[0] for i in new_X_Y]
# Y=[i[1] for i in new_X_Y]
# print(new_X_Y)
# plt.plot(X,Y)
# plt.xlabel('Density')
# plt.ylabel('Flow')
# plt.title('Density vs Flow')
# plt.show()

# velocity_vs_flow_dic={}
# new_X_Y=[(density_dic[density[i]],density[i]*density_dic[density[i]]) for i in range(len(density))]
# # sort them in ascending order
# new_X_Y.sort()
# # print(new_X_Y)
# X=[i[0] for i in new_X_Y]
# Y=[i[1] for i in new_X_Y]
# plt.plot(X,Y)
# plt.xlabel('Velocity')
# plt.ylabel('Flow')
# plt.title('Velocity vs Flow')
# plt.show()

# use curve fitting on X,Y
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def objective(x,a,b,c,d):
    v= a*(x**3)+b*x**2+c*x+d
    return v
popt,_=curve_fit(objective,X,Y)
a,b,c,d=popt
a_,b_,c_,d_=a,b,c,d
def get_velocity(x):
    v= a_*(x**3)+b_*x**2+c_*x+d_
    if v<0.01:
        v=0.01
    return v
#print(a,b,c,d)

# plt.plot(X,Y)
x_line = np.arange(int(100*min(X)), int(100*max(X)),1)
x_line=x_line/100
# calculate the output for the range
#print(x_line)

y_line = objective(x_line, a_, b_, c_,d_)
#print(y_line)
# # create a line plot for the mapping function
# plt.plot(x_line, y_line, '--', color='red')
# plt.show()

# print(get_velocity(0.4))
# print(get_velocity(0.5))
# print(get_velocity(0.6))
