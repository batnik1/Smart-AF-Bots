density_dic={}
# open Density_vs_Velocity and use avg_density dictionary to store avg_velocities
with open('Density_vs_Velocity','r') as f:
    for line in f:
        line=line.strip().split(',')
        if line[1]=="density":
            continue
        #print(line)
        density_dic[float(line[1])]=float(line[0])

print(density_dic)