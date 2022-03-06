density_dic={}
# open Density_vs_Velocity and use avg_density dictionary to store avg_velocities
with open('Density_vs_Velocity','r') as f:
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
# X=[i[0] for i in X_Y]
# Y=[i[1] for i in X_Y]
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
