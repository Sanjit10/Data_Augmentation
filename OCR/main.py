import augmentation
import os
import argparse
import yaml
import random
import shutil
from PIL import Image
import time
import label_conveter

parser=argparse.ArgumentParser() #CLI documentation for commandline input

parser.add_argument('--dir=',type=str)
parser.add_argument('--label_format=', type=str, choices=['OCR', 'YOLO5', 'YOLO8'], help='The format to convert the data to', default=None)
parser.add_argument('--n=',type=str)
parser.add_argument('--rotate=',type=str)
parser.add_argument('--blur=',type=str)
parser.add_argument('--contrast=',type=str)
parser.add_argument('--elastic=',type=str)
parser.add_argument('--rigid=',type=str)
parser.add_argument('--percent=',type=int)
parser.add_argument('--recursion_rate=',type=float)
parser.add_argument('--master_dir=',type=str)
parser.add_argument('--gui_dir_path=',type=str)
args=parser.parse_args()

dir=vars(args)['dir=']
labelvalue=vars(args)['label_format=']
n=vars(args)['n=']
blvalue=vars(args)['blur=']
rotate=vars(args)['rotate=']
cvalue=vars(args)['contrast=']
percent=vars(args)['percent=']
evalue=vars(args)['elastic=']
rvalue=vars(args)['rigid=']
rr = vars(args)['recursion_rate=']
master_dir = vars(args)['master_dir=']
gui_dir_path = vars(args)['gui_dir_path=']

type = 'paddle'
dir_name = dir+'_Detection_Dataset'
if not os.path.isdir(dir_name):
    os.mkdir(dir_name,)
    print('Detection_Dataset Folder Created')
else:
    pass
outdir=dir_name+'/'
count=0
n=int(n.replace('x',''))
rotate_list=rotate.split('to')
blvalue_list=blvalue.split('to')
cvalue_list=cvalue.split('to')
evalue_list=evalue.split('to')
rvalue_list=rvalue.split('to')

print("Augmentation Started")

aug_weight = 0
current_file_name = ''
weights = [0.2, 0.2, 0.0,0.2,0.2,0.1,0.1]   ####### probability values of each augmentation methods

start = time.time()

def train_test_split(aug_master_dir, percent):
    """
    A function that splits the aug_master_dir into train and test directories based on the percentage provided.
    It creates a structure where train and test directories contain 'images' and 'labels' subdirectories.
    """
    # Get the list of all files in the aug_master_dir
    file_list = os.listdir(aug_master_dir)
    
    # Filter the files into images and labels
    images = [f for f in file_list if '.jpg' in f]  # Adjust the condition based on your naming convention
    labels = [f for f in file_list if '.txt' in f]  # Adjust the condition based on your naming convention

    # Ensure there is a corresponding label for each image
    images.sort()
    labels.sort()
    
    # Calculate the number of files for training and testing based on the percentage
    train_count = int(len(images) * (percent / 100))
    
    # Shuffle the file lists randomly
    combined_list = list(zip(images, labels))
    random.shuffle(combined_list)
    
    # Create the train and test directories with images and labels subdirectories
    train_images_dir = os.path.join(aug_master_dir, 'train', 'images')
    train_labels_dir = os.path.join(aug_master_dir, 'train', 'labels')
    test_images_dir = os.path.join(aug_master_dir, 'test', 'images')
    test_labels_dir = os.path.join(aug_master_dir, 'test', 'labels')
    
    os.makedirs(train_images_dir, exist_ok=True)
    os.makedirs(train_labels_dir, exist_ok=True)
    os.makedirs(test_images_dir, exist_ok=True)
    os.makedirs(test_labels_dir, exist_ok=True)
    
    # Move the files to the train and test directories
    for i, (image, label) in enumerate(combined_list):
        if i < train_count:
            shutil.move(os.path.join(aug_master_dir, image), os.path.join(train_images_dir, image))
            shutil.move(os.path.join(aug_master_dir, label), os.path.join(train_labels_dir, label))
        else:
            shutil.move(os.path.join(aug_master_dir, image), os.path.join(test_images_dir, image))
            shutil.move(os.path.join(aug_master_dir, label), os.path.join(test_labels_dir, label))
    
    print(f"Train-Test split completed. {train_count} image-label pairs moved to train directory and {len(images) - train_count} pairs moved to test directory.")
    update_data_yaml(os.path.join(dir, 'data.yaml'), os.path.join(aug_master_dir,'data.yaml'), os.path.join(aug_master_dir,'train'), os.path.join(aug_master_dir,'test'))

def update_data_yaml(source_yaml_path, destination_yaml_path, train_path, test_path):
    """
    A function that reads an existing data.yaml file from the source directory, updates it with the
    train and test paths and the number of classes, and writes the updated data.yaml file to the destination directory.
    """
    #check if the source yaml file exists
    if not os.path.exists(source_yaml_path):
        print(f"Error: {source_yaml_path} does not exist.")
        return
    # Load the existing yaml file
    with open(source_yaml_path, 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)
    
    # Calculate the number of classes based on the 'names' field
    num_classes = len(data.get('names', {}))
    
    # Update the yaml data
    data['train'] = train_path
    data['test'] = test_path
    data['nc'] = num_classes
    
    # Write the updated data back to the new yaml file in the destination directory
    with open(destination_yaml_path, 'w') as yaml_file:
        yaml.dump(data, yaml_file, default_flow_style=False)
    
    print(f"data.yaml file updated and saved at {destination_yaml_path}")

def random_augment():
    '''
    A function that chooses the augmentation method randomly and return the 
    probability values, image_path, bounding_box_path, augmentation method name
    '''
    (aug_method, weights_1), = random.choices(list(zip(aug_methods,weights)))
    #print("Augmentation Method",aug_method)
    aug_methods.pop(aug_methods.index(aug_method))
    aug_method_name, func, args = aug_method
    new_file = os.path.join(outdir,args[0])
    args = (new_file,*args[1:])
    if not isinstance(args, list):
        args = [*args]
    # print("Function Info",func(*args))
    image, bounding_box = func(*args)
    return weights_1, image, bounding_box, aug_method_name

def recursive_augment(img, bounding_box, outdir, rr):
    '''
    Implement an augmentation method recursively by adding its associated probability until the sum of probabilities is greater than the recursion rate.

    Parameters:
    - img (str): Path of the image returned by the augmentation method.
    - bounding_box (str): Path of the bounding box returned by the augmentation method.
    - rr (float): Recursion rate indicating the threshold for stopping the recursion.
    '''

    global aug_weight, current_file_name
    prob_val, img, bbox, aug_method_name = random_augment()
    # print("[*] Augmenting Image ", img)
    # print("     [*] Choosing methods ", aug_method_name)
    aug_weight += prob_val
    if aug_weight >= rr:
        # print("Complete Image",filename)
        aug_weight = 0
        
        augmented_image_path = os.path.join(outdir, f"{current_file_name}_aug_{count}.jpg")
        shutil.copy(img, augmented_image_path)
        
        augmented_text_path = os.path.join(outdir,f"{current_file_name}_aug_{count}.txt")
        shutil.copy(bounding_box, augmented_text_path)
        
        # print('[+] save file ', os.path.join(outdir, augmented_image_path))
        return
    else:
        # print("[*] added weight value",aug_weight)
        current_file_name = current_file_name + '_' + aug_method_name  #### For file name
        recursive_augment(img, bbox, outdir, rr)
    
# Copy all the files in the output directory
for filename in os.listdir(dir):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        for i in range(0,n):
            i = str(i)
            shutil.copy(os.path.join(dir, filename), os.path.join(outdir, filename.replace('.jpg', f'_{i}.jpg')))
            shutil.copy(os.path.join(dir, filename.replace(".jpg",'.txt')), os.path.join(outdir, filename.replace(".jpg",'.txt').replace('.txt', f'_{i}.txt')))


# Apply Augmentation
list_of_files = os.listdir(outdir)
for filename in list_of_files:
    if filename.endswith('.jpg') or filename.endswith('.png'):
        # print('---------------------------------------------')
        bounding_box = filename.replace(".jpg",'.txt')
        i = ''
        angle = float(random.randrange(float(rotate_list[0]), float(rotate_list[1])))
        blur = int(random.randrange(float(blvalue_list[0]), float(blvalue_list[1])))
        contrast = float(random.randrange(float(cvalue_list[0]), float(cvalue_list[1])))
        elastic = int(random.randrange(float(evalue_list[0]), float(evalue_list[1])))
        rigid = int(random.randrange(float(rvalue_list[0]), float(rvalue_list[1])))
        aug_methods = [                                               ###### Augmentation methods
            ('ori', augmentation.original, (filename,outdir,i)),
            ('ro', augmentation.rotate, (filename,angle,outdir,i)),
            ('fl', augmentation.img_flip, (filename,outdir,i)),
            ('bl', augmentation.blur, (filename,blur,outdir,i)),
            ('co', augmentation.contrast, (filename,contrast,outdir,i)),
            ('el', augmentation.elastic_transform, (filename,elastic,outdir,i)),
            ('ri', augmentation.rigid, (filename,rigid,outdir,i))
        ]
        current_file_name = filename.replace('.jpg', '')
        recursive_augment(filename, bounding_box, outdir, rr)  ###### calling recursive function

        # unaugmented image remove
        os.remove(os.path.join(outdir, filename)) ##### remove existing image
        os.remove(os.path.join(outdir, filename.replace('.jpg', '.txt')))   ##### remove existing files
        # print('[-] removed file ', os.path.join(outdir, filename))

        # print('--------------------------------------')
        count += 1
        if count % 100 == 0:
            print("Number of data created: ", count)
            print("Total time taken",time.time()-start)

#Apply conversion to the format
if labelvalue is not None:
    list_of_files = os.listdir(outdir)
    for filename in list_of_files:
        if filename.endswith('.txt'):
            label_conveter.label_converter_main(os.path.join(outdir, filename), labelvalue)
    print(f"Conversion to {labelvalue} format complete. Original text file replaced.")


print("Total number of data created: ", count)

print("Augmentation Completed")

train_test_split(outdir, 80)



