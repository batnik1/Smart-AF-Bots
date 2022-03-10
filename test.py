import yaml
import os
import time
congestion=[0,1,2]
# save a copy of parameters.yaml file in the folder Tested Yaml in same directory
# titime.time()
# get date and time from time
date=time.strftime("%d%m")
tt=time.strftime("%H%M%S")
file_name=str(date)+'t'+str(tt)+'parameters.yaml'
print(file_name)
os.system("cp parameters.yaml TestedYaml/"+file_name)

for c in congestion:
    # open parameters.yaml file and change the value of congestion_flag to c
    with open('parameters.yaml', 'r') as stream:
        try:
            parameters = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    parameters['congestion_flag']=c
    
    # write the changed parameters to parameters.yaml file
    with open('parameters.yaml', 'w') as outfile:
        yaml.dump(parameters, outfile, default_flow_style=False)
    # save the parameters.yaml file
        
    # run window.py file
    os.system("python3 window.py")
