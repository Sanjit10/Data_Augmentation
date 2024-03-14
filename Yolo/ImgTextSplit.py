import shutil
import os
import yaml


def img_text_split(dir:str)->None:
    '''
    This function splits images and annotation in different folder for both train and test
    '''

    if 'TrainAnno' not in os.listdir(dir):
        os.makedirs(dir+'TrainAnno')

    for trname in os.listdir(dir+'Train'):
        if '.txt' in trname:
            shutil.move(dir+'Train/'+trname,dir+'TrainAnno/'+trname) 

    if 'TestAnno' not in os.listdir(dir):
        os.makedirs(dir+'TestAnno')

    for tename in os.listdir(dir+'Test'):
        if '.txt' in tename:
            shutil.move(dir+'Test/'+tename,dir+'TestAnno/'+tename)

   
