# importing os module
import os
import random
# Function to rename multiple files
def change_name(dir1):
    
    i = 1
    j = 1
    os.chdir(dir1)
    for filename in os.listdir(dir1):
            if '.jpg' in filename:
                os.rename(filename,str(i)+'.jpg')
                i= i+1
            if '.txt' in filename:
                os.rename(filename,str(j)+'.txt')
                j = j+1

    image = []
    for img in os.listdir(dir1):  
        os.chdir(dir1)
        if '.jpg' in img:
             image.append(img)
    u = random.sample(range(1,len(image)+1),len(image))
    # print(u)
    for k in range(1,len(u)+1):
        os.rename(str(k)+'.jpg','img_'+str(u[k-1])+'.jpg')
        os.rename(str(k)+'.txt','img_'+str(u[k-1])+'.txt')
