import random
import os
import shutil
import yaml

def split(dir:str,per:int)->None:
    '''
    This function splits dataset into train and test as percentage entered by user. If percent=70 is applied
    that 70% becomes train and 30% becomes test randomly
    '''
    img=[]
    txt=[]

    if 'Train' not in os.listdir(dir):
        os.makedirs(dir+'Train')

    if 'Test' not in os.listdir(dir):
        os.makedirs(dir+'Test')

    for filename in os.listdir(dir):
        if '.jpg' in filename:
            img.append(filename)
        if '.txt' in filename:
            txt.append(filename)
 
    split=int(len(img)*(per/100))

    r=random.sample(range(split), split)
    for i in r:

        shutil.move(dir+'/'+img[i],dir+'Train'+'/'+img[i])
        shutil.move(dir+'/'+txt[i],dir+'Train'+'/'+txt[i])

    for fname in os.listdir(dir): 
        if '.jpg' in fname or '.txt' in fname:
            shutil.move(dir+fname,dir+'Test')

   
