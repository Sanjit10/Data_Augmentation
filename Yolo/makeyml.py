import os
import yaml
def makeYML(dir,outdir):
    fn=[]
    lb=[]
    for filename in os.listdir(dir):
        if '.txt' in filename:
            os.chdir(dir)
            fn.append(filename)

    for j in range(0,len(fn)):        
        f=open(fn[j],'r')
        ln=len(f.readlines())
        f.close()
        for i in range(0,ln):
            f=open(fn[j],'r')
            lb.append(f.readlines()[i].split(' ')[0])
            f.close
    data={
        'train':outdir+'Train',
        'val': outdir+'Test',
        'nc':len(list(set(lb))),
        'names':list(set(lb)),
        
        'crimson':{
            'workspace': 'crimson_yolo',
            'project': 'train_yolo',
            'version': 1,
            'license': 'Private',
            'url': 'crimsontech.io'
            }
        }

    with open(outdir+'data.yaml', 'w') as file:
        yaml.dump(data, file)
    
   


    
        
        
        