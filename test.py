import yaml

congestion=[0,1,2]
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
        
    exec(open("window.py").read())

