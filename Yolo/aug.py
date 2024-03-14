import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps,ImageDraw
import random
import shutil
from scipy.ndimage.interpolation import map_coordinates
from scipy.ndimage.filters import gaussian_filter
from random import randint,choice
import math
import os
import pybboxes

def rotate(dir,angle,outdir,n,type):
    #dir='C:/innate2/AugmentationWork/AugCLI/images/'
    '''
    A function that generates augmented images by rotating the images in random multiple degrees.

    Parameters:
    dir (str): The path of the input directory.
    Angle (int): The angle of rotation.
    outdir (str): The path of the output directory.
    n (int): The number of times the image should be augmented.
    type (str): The type of framework, i.e., "paddleocr" or "yolo".
    '''
    img=dir
    img2=Image.open(img)
    #img.show()
    bb=img.replace('.jpg','.txt')
    #angle=15
    f=open(bb,'r')
    l=len(f.readlines())
    f.close()
    def rotateBox(image,angle,bbox):
    # Load the image
        #image=cv2.resize(image)
        # Convert the image from RGB to BGR
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Get the image dimensions
        height, width = image.shape[:2]
        image_center = (width / 2, height / 2)  # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape

        # Define the rotation angle
        value = angle

        # Compute the rotation matrix
        rotation_mat = cv2.getRotationMatrix2D(image_center, value, 1.)

        # Compute the new dimensions of the image after rotation
        abs_cos = abs(rotation_mat[0, 0])
        abs_sin = abs(rotation_mat[0, 1])
        bound_w = int(height * abs_sin + width * abs_cos)
        bound_h = int(height * abs_cos + width * abs_sin)

        # Update the rotation matrix with the new dimensions
        rotation_mat[0, 2] += bound_w / 2 - image_center[0]
        rotation_mat[1, 2] += bound_h / 2 - image_center[1]

        # Rotate the image using the rotation matrix
        rotated_image = cv2.warpAffine(image, rotation_mat, (bound_w, bound_h))

        # Define the bounding box coordinates
        bounding_box = bbox

        # Reshape the bounding box coordinates
        bounding_box = bounding_box.reshape((-1, 1, 2))

        # Rotate the bounding box coordinates using the rotation matrix
        rotated_bounding_box = cv2.transform(bounding_box, rotation_mat)

        coordinates_text = rotated_bounding_box.reshape((-1, 1, 2))
        coordinates_text=coordinates_text.flatten()
        rgb = cv2.cvtColor(rotated_image, cv2.COLOR_BGR2RGB)
        return Image.fromarray(rgb),coordinates_text
    if type=='paddle':
        for i in range(0,l):
            f=open(bb,'r')
            x1=f.readlines()[i].split(',')[0]
            f.close()

            f=open(bb,'r')
            y1=f.readlines()[i].split(',')[1]
            f.close()

            f=open(bb,'r')
            x2=f.readlines()[i].split(',')[2]
            f.close()

            f=open(bb,'r')
            y2=f.readlines()[i].split(',')[3]
            f.close()

            f=open(bb,'r')
            x3=f.readlines()[i].split(',')[4]
            f.close()

            f=open(bb,'r')
            y3=f.readlines()[i].split(',')[5]
            f.close()

            f=open(bb,'r')
            x4=f.readlines()[i].split(',')[6]
            f.close()

            f=open(bb,'r')
            y4=f.readlines()[i].split(',')[7]
            f.close()

            bobox = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], np.int32)
            
            imgo,cor=rotateBox(img2,angle,bobox)
            
            
            f=open(bb,'r')
            a=f.readlines()[i].split(',')[8]
            f.close()
            imgo.save(outdir+img.replace('.jpg','_r_'+str(angle)+str(n)+'.jpg'))
            g=open(outdir+bb.replace('.txt','_r_'+str(angle)+str(n)+'.txt'),'a')
            g.write(str(str(cor.tolist())+','+a).replace(']','').replace('[',''))
            g.close

    elif type=="yolo":
        for i in range(0,l):
            f=open(bb,'r')
            x=(float(f.readlines()[i].split(" ")[1:][0]))
            f.close()

            f=open(bb,'r')
            y=(float(f.readlines()[i].split(" ")[1:][1]))
            f.close()

            f=open(bb,'r')
            w=(float(f.readlines()[i].split(" ")[1:][2]))
            f.close()

            f=open(bb,'r')
            h=(float(f.readlines()[i].split(" ")[1:][3]))
            f.close()

            image_w=img2.size[0]
            image_h=img2.size[1]

            w = w * image_w
            h = h * image_h
            x1 = ((2 * x * image_w) - w)/2
            y1 = ((2 * y * image_h) - h)/2
            x2 = x1 + w
            y2 = y1 + h

            xmin = round(x1)
            xmax = round(x2)
            ymin = round(y1)
            ymax = round(y2)
            
            bobox = np.array([[xmin, ymax], [xmax, ymax], [xmax, ymin], [xmin, ymin]], np.int32)
            
            imgo,cor=rotateBox(img2,angle,bobox)
            b=cor.tolist()
            f.close()
            
            x_center = (b[0] + b[2] + b[4] + b[6]) / 4
            y_center = (b[1] + b[3] + b[5] + b[7]) / 4

            # Calculate the width and height of the bounding box
            width = max(b[0] , b[2] , b[4] , b[6]) - min(b[0] , b[2] , b[4] , b[6])
            height = max(b[1] , b[3] , b[5] ,b[7]) - min(b[1] , b[3] , b[5] ,b[7])

            # Normalize the coordinates, width, and height to be between 0 and 1
            x_center /= imgo.size[0]
            y_center /= imgo.size[1]
            width /= imgo.size[0]
            height /= imgo.size[1]
            c=[x_center,y_center,width,height]
            f=open(bb,'r')
            a=f.readlines()[i].split(' ')[0]
            f.close()
            imgo.save(img.replace('.jpg','_r_'+str(angle)+str(n)+'.jpg'))
            g=open(bb.replace('.txt','_r_'+str(angle)+str(n)+'.txt'),'a')
            g.write(a+' '+str(c).replace(']','').replace('[','').replace(',',''))
            g.write('\n')
            g.close

    return img,bb
def original(dir,outdir,n):
    '''
    A function that generates augmented images by copying the original images.

    Parameters:
    dir (str): The path of the input directory.
    outdir (str): The path of the output directory.
    n (int): The number of times the image should be augmented.
    '''
    img=dir
    img2=Image.open(img)
    bb=img.replace('.jpg','.txt')
    img_name = os.path.basename(img)
    img2.save(outdir+img_name)
    text_path = os.path.basename(bb)
    shutil.move(bb,outdir+text_path)
    
    return img, bb

def blur(dir,value,outdir,n):
    '''
    A function that generates augmented images by blurring the images in random values.

    Parameters:
    dir (str): The path of the input directory.
    value (int): The random value.
    outdir (str): The path of the output directory.
    n (int): The number of times the image should be augmented.
    '''
    img=dir
    img2=Image.open(img)
    bb=img.replace('.jpg','.txt')
    img2=img2.filter(ImageFilter.GaussianBlur(value / 4))
    
    img_name = os.path.basename(img)
    img2.save(outdir+img_name)
    text_path = os.path.basename(bb)
    shutil.move(bb,outdir+text_path)

    return img, bb

def img_flip(dir, outdir, n):
    '''
    A function that generates augmented images by flipping the images in random values.

    Parameters:
    dir (str): The path of the input directory.
    outdir (str): The path of the output directory.
    n (int): The number of times the image should be augmented.
    '''
    img = dir
    img_name = os.path.basename(img)
    bbox = img.replace('.jpg', '.txt')
    bb_path = bbox
    bbox_name = os.path.basename(bb_path)
    image = Image.open(img)
    # Get the rotation angle of the image (if any)
    angle = float(image.info.get('rotate', 0))
    # Convert angle to radians
    angle_radians = math.radians(angle)
    # Define the flip methods
    transform_methods = [
        Image.FLIP_LEFT_RIGHT,
        Image.FLIP_TOP_BOTTOM
    ]
    # Generate a random index to choose a transformation method
    random_index = random.randint(0, len(transform_methods) - 1)

    if angle != 0:
        image = image.rotate(-angle)  # Negative angle to counter-clockwise rotation

    # Apply the randomly chosen transformation method (flip)
    flipped_image = image.transpose(transform_methods[random_index])

    # Save the flipped image
    img_name = os.path.basename(img)
    flipped_image.save(os.path.join(outdir, img_name))

    # Read and adjust bounding box coordinates
    with open(bbox, 'r') as bbox_file:
        bounding_boxes = bbox_file.readlines()
    # Define a function to rotate a point around an origin
    def rotate_point(point, origin, angle):
        ox, oy = origin
        px, py = point
        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return int(qx), int(qy)

    adjusted_bounding_boxes = []

    # if type == 'paddle':

    #     for bbox in bounding_boxes:
    #         bbox = bbox.strip().split(',')
    #         # Check if there are enough values (8) for valid annotation
    #         if len(bbox) != 9:
    #             print(f"Skipping invalid annotation: {bbox}")
    #             continue
    #         x1, y1, x2, y2, x3, y3, x4, y4, label = map(str.strip, bbox)
    #         x1, y1, x2, y2, x3, y3, x4, y4 = map(int, [x1, y1, x2, y2, x3, y3, x4, y4])

    #         # Rotate the bounding box points if the image was rotated
    #         if angle != 0:
    #             center_x = (x1 + x2 + x3 + x4) // 4
    #             center_y = (y1 + y2 + y3 + y4) // 4
    #             rotated_points = [
    #                 rotate_point((x1, y1), (center_x, center_y), angle_radians),
    #                 rotate_point((x2, y2), (center_x, center_y), angle_radians),
    #                 rotate_point((x3, y3), (center_x, center_y), angle_radians),
    #                 rotate_point((x4, y4), (center_x, center_y), angle_radians)
    #             ]
    #         else:
    #             rotated_points = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]

    #         # Adjust bounding box coordinates based on flip method
    #         if transform_methods[random_index] == Image.FLIP_LEFT_RIGHT:
    #             adjusted_bbox = [(image.width - x, y) for x, y in rotated_points]
    #         else:  # Image.FLIP_TOP_BOTTOM
    #             adjusted_bbox = [(x, image.height - y) for x, y in rotated_points]

    #         adjusted_bbox = [str(x) for point in adjusted_bbox for x in point]  # Flatten the list
    #         adjusted_bbox = ','.join(adjusted_bbox)
    #         adjusted_bounding_boxes.append(f"{adjusted_bbox},{label}")

    # elif type == 'yolo':

    for bbox in bounding_boxes:
        bbox = bbox.strip().split()
        
        # Check if there are enough values (5) for a valid YOLO annotation
        if len(bbox) != 5:
            print(f"Skipping invalid YOLO annotation: {bbox}")
            continue

        class_label, x_center, y_center, width, height = map(float, bbox)

        # Flip the bounding box coordinates based on flip method
        if transform_methods[random_index] == Image.FLIP_LEFT_RIGHT:
            x_center = 1.0 - x_center  # Flip the x-coordinate
        else:  # Image.FLIP_TOP_BOTTOM
            y_center = 1.0 - y_center  # Flip the y-coordinate

        adjusted_bbox = f"{int(class_label)} {x_center} {y_center} {width} {height}"
        adjusted_bounding_boxes.append(adjusted_bbox)

    # Save the adjusted bounding box coordinates to a new text file
    adjusted_bbox_path = os.path.join(outdir, bbox_name)
    with open(adjusted_bbox_path, 'w') as adjusted_bbox_file:
        adjusted_bbox_file.write('\n'.join(adjusted_bounding_boxes))

    return img, bb_path
    

def contrast(dir,value,outdir,n):
    '''
    A function that generates augmented images by applying contrast to the images with random values.

    Parameters:
    dir (str): The path of the input directory.
    value (int): The random value.
    outdir (str): The path of the output directory.
    n (int): The number of times the image should be augmented.
    '''
    img=dir
    img2=Image.open(img)
    bb=img.replace('.jpg','.txt')
    img2=ImageEnhance.Brightness(img2).enhance(1.0 + value / 100)
    img_name = os.path.basename(img)
    img2.save(outdir+img_name)
    text_name = os.path.basename(bb)
    shutil.move(bb,outdir+text_name) 

    return img, bb

def elastic_transform(dir, value,outdir,n):
    '''
    A function that generates augmented images by applying elastic_transformation to the images with random values.

    Parameters:
    dir (str): The path of the input directory.
    value (int): The random value.
    outdir (str): The path of the output directory.
    n (int): The number of times the image should be augmented.
    '''
    img=dir
    img3=Image.open(img)
    img2 = cv2.cvtColor(np.array(img3), cv2.COLOR_RGB2BGR)
    bb=img.replace('.jpg','.txt')
    sigma=8
    random_state=None
    if random_state is None:
        random_state = np.random.RandomState(None)

    shape = img2.shape
    dx = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma, mode="constant", cval=0) * value
    dy = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma, mode="constant", cval=0) * value
    dz = np.zeros_like(dx)
    x, y, z = np.meshgrid(np.arange(shape[1]), np.arange(shape[0]), np.arange(shape[2]))
    indices = np.reshape(y+dy, (-1, 1)), np.reshape(x+dx, (-1, 1)), np.reshape(z, (-1, 1))
    img2 = map_coordinates(img2, indices, order=1, mode='reflect').reshape(img2.shape)
    img4 = Image.fromarray(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
    
    img_name = os.path.basename(img)
    img4.save(outdir+img_name)
    bb_name = os.path.basename(bb)
    shutil.move(bb,outdir+bb_name)

    return img, bb


def rigid(dir,value,outdir,n):
    '''
    A function that generates augmented images by applying rigid transformation to the images with random values.

    Parameters:
    dir (str): The path of the input directory.
    value (int): The random value.
    outdir (str): The path of the output directory.
    n (int): The number of times the image should be augmented.
    '''
        # ------------------------ Moving Least square ------------- rigid deformation ------------------------------------
    np.seterr(divide='ignore', invalid='ignore')

    def mls_rigid_deformation(vy, vx, p, q, alpha=1.0, eps=1e-8):

        q = np.ascontiguousarray(q.astype(np.int16))
        p = np.ascontiguousarray(p.astype(np.int16))

        # Exchange p and q and hence we transform destination pixels to the corresponding source pixels.
        p, q = q, p

        grow = vx.shape[0]  # grid rows
        gcol = vx.shape[1]  # grid cols
        ctrls = p.shape[0]  # control points

        # Compute
        reshaped_p = p.reshape(ctrls, 2, 1, 1)                                              # [ctrls, 2, 1, 1]
        reshaped_v = np.vstack((vx.reshape(1, grow, gcol), vy.reshape(1, grow, gcol)))      # [2, grow, gcol]
        
        w = 1.0 / (np.sum((reshaped_p - reshaped_v).astype(np.float32) ** 2, axis=1) + eps) ** alpha    # [ctrls, grow, gcol]
        w /= np.sum(w, axis=0, keepdims=True)                                               # [ctrls, grow, gcol]

        pstar = np.zeros((2, grow, gcol), np.float32)
        for i in range(ctrls):
            pstar += w[i] * reshaped_p[i]                                                   # [2, grow, gcol]

        vpstar = reshaped_v - pstar                                                         # [2, grow, gcol]
        reshaped_vpstar = vpstar.reshape(2, 1, grow, gcol)                                  # [2, 1, grow, gcol]
        neg_vpstar_verti = vpstar[[1, 0],...]                                               # [2, grow, gcol]
        neg_vpstar_verti[1,...] = -neg_vpstar_verti[1,...]                                  
        reshaped_neg_vpstar_verti = neg_vpstar_verti.reshape(2, 1, grow, gcol)              # [2, 1, grow, gcol]
        mul_right = np.concatenate((reshaped_vpstar, reshaped_neg_vpstar_verti), axis=1)    # [2, 2, grow, gcol]
        reshaped_mul_right = mul_right.reshape(2, 2, grow, gcol)                            # [2, 2, grow, gcol]

        # Calculate q
        reshaped_q = q.reshape((ctrls, 2, 1, 1))                                            # [ctrls, 2, 1, 1]
        qstar = np.zeros((2, grow, gcol), np.float32)
        for i in range(ctrls):
            qstar += w[i] * reshaped_q[i]                                                   # [2, grow, gcol]
        
        temp = np.zeros((grow, gcol, 2), np.float32)
        for i in range(ctrls):
            phat = reshaped_p[i] - pstar                                                    # [2, grow, gcol]
            reshaped_phat = phat.reshape(1, 2, grow, gcol)                                  # [1, 2, grow, gcol]
            reshaped_w = w[i].reshape(1, 1, grow, gcol)                                     # [1, 1, grow, gcol]
            neg_phat_verti = phat[[1, 0]]                                                   # [2, grow, gcol]
            neg_phat_verti[1] = -neg_phat_verti[1]
            reshaped_neg_phat_verti = neg_phat_verti.reshape(1, 2, grow, gcol)              # [1, 2, grow, gcol]
            mul_left = np.concatenate((reshaped_phat, reshaped_neg_phat_verti), axis=0)     # [2, 2, grow, gcol]
            
            A = np.matmul((reshaped_w * mul_left).transpose(2, 3, 0, 1), 
                            reshaped_mul_right.transpose(2, 3, 0, 1))                       # [grow, gcol, 2, 2]

            qhat = reshaped_q[i] - qstar                                                    # [2, grow, gcol]
            reshaped_qhat = qhat.reshape(1, 2, grow, gcol).transpose(2, 3, 0, 1)            # [grow, gcol, 1, 2]

            # Get final image transfomer -- 3-D array
            temp += np.matmul(reshaped_qhat, A).reshape(grow, gcol, 2)                      # [grow, gcol, 2]

        temp = temp.transpose(2, 0, 1)                                                      # [2, grow, gcol]
        normed_temp = np.linalg.norm(temp, axis=0, keepdims=True)                           # [1, grow, gcol]
        normed_vpstar = np.linalg.norm(vpstar, axis=0, keepdims=True)                       # [1, grow, gcol]
        transformers = temp / normed_temp * normed_vpstar  + qstar                          # [2, grow, gcol]
        nan_mask = normed_temp[0] == 0

        # Replace nan values by interpolated values
        nan_mask_flat = np.flatnonzero(nan_mask)
        nan_mask_anti_flat = np.flatnonzero(~nan_mask)
        transformers[0][nan_mask] = np.interp(nan_mask_flat, nan_mask_anti_flat, transformers[0][~nan_mask])
        transformers[1][nan_mask] = np.interp(nan_mask_flat, nan_mask_anti_flat, transformers[1][~nan_mask])

        # Remove the points outside the border
        transformers[transformers < 0] = 0
        transformers[0][transformers[0] > grow - 1] = 0
        transformers[1][transformers[1] > gcol - 1] = 0
    
        return transformers.astype(np.int16)
    
        # ------------------ Return the rigid Deformation Image ---------------------------
    def demo_auto(p,q,image):  
        
        height, width,_= image.shape
        gridX = np.arange(width, dtype=np.int16)
        gridY = np.arange(height, dtype=np.int16)
        vy, vx = np.meshgrid(gridX, gridY)

        rigid = mls_rigid_deformation(vy, vx, p, q, alpha=1)
        aug3 = np.ones_like(image)
        aug3[vx, vy] = image[tuple(rigid)]
        return aug3
    # ------------------------ Function to get random coordinates with respect with given shift value -------------
    def RandMove(old_pnt,min_shift,max_shift):
        neg = [-1,1]

        #get the first point from the geometry object
        old_x = old_pnt[0]
        old_y = old_pnt[1]

        #calculate new coordinates
        new_x = old_x + (choice(neg) * randint(min_shift,max_shift))
        new_y = old_y + (choice(neg) * randint(min_shift,max_shift))
        
        return (new_x,new_y)
    
    # ------------------------------ Function to get random p and q control points -------------------------
    def check_p_q(coordinates,distance,control_points):
        p_coordinates = []
        q_coordinates = []
        while True:
            if (len(q_coordinates) == control_points):
                break
            else:
                x, y = random.choice(coordinates) 
                old_co = (x,y)
                new_co = RandMove(old_co,-distance,distance)
                # Check if the new coordinates are within the given list of coordinates
                if new_co in coordinates:
                    
                    p_coordinates.append(old_co)
                    q_coordinates.append(new_co)
                else:
                    pass
                    # print("no")
        return p_coordinates,q_coordinates
    
    #----------------------------------Function to find all the coordinates lie inside the boundary box ----------------
    def find_all_coordinates(x1,y1,x2,y2,x3,y3,x4,y4):
        # Create an empty list to hold the coordinates
        coordinates = []
        # Loop over the x values between the left and right edges of the rectangle
        for x in range(min(x1, x2, x3, x4), max(x1, x2, x3, x4) + 1):
            # Loop over the y values between the top and bottom edges of the rectangle
            for y in range(min(y1, y2, y3, y4), max(y1, y2, y3, y4) + 1):
                # Check if the current coordinate is inside the rectangle
                if (x2-x1)*(y-y1) - (y2-y1)*(x-x1) >= 0 and (x3-x2)*(y-y2) - (y3-y2)*(x-x2) >= 0 and (x4-x3)*(y-y3) - (y4-y3)*(x-x3) >= 0 and (x1-x4)*(y-y4) - (y1-y4)*(x-x4) >= 0:
                    # Append the current coordinate to the list
                    coordinates.append((x, y))               
        return coordinates
    
    def return_all_x_and_y(my_list):
        x1,y1 = int(my_list[0]),int(my_list[1])
        x2,y2 = int(my_list[2]),int(my_list[3])
        x3,y3 = int(my_list[4]),int(my_list[5])
        x4,y4 = int(my_list[6]),int(my_list[7])
        return x1,y1,x2,y2,x3,y3,x4,y4
    

    def return_from_to(path,x1,y1,x2,y2,x3,y3,x4,y4):
        im = Image.open(path)

        # Define the two points between which to find coordinates

        li = []
        # Create a new image with the same size as the original image
        new_im = Image.new('RGB', im.size, (255, 255, 255))

        # Draw a line between the two points on the new image
        draw1 = ImageDraw.Draw(new_im)
        draw1.line((x1, y1, x2, y2), fill='black')

        draw2 = ImageDraw.Draw(new_im)
        draw2.line((x2, y2, x3, y3), fill='black')

        draw3 = ImageDraw.Draw(new_im)
        draw3.line((x4, y4, x3, y3), fill='black')

        draw4 = ImageDraw.Draw(new_im)
        draw4.line((x1, y1, x4, y4), fill='black')

        # Iterate over all the pixels in the new image and print the coordinates of the black pixels
        for x in range(new_im.size[0]):
            for y in range(new_im.size[1]):
                if new_im.getpixel((x, y)) == (0, 0, 0):
                    li.append((x,y))

        select_control_points_no = int(len(li)/20)
        select_control_points = random.sample(li, select_control_points_no)
        return select_control_points

    # Open the file for reading
    path = dir
    img = dir
    
    img4=dir
    img3=Image.open(img4)
    img2 = cv2.cvtColor(np.array(img3), cv2.COLOR_RGB2BGR)
    bb=img4.replace('.jpg','.txt')
    
    my_list = []

    with open(bb, 'r') as file:
        lent = len(file.readlines())

    file.close()
    if type=='paddle':    
        for i in range(lent):
        # Open the file for reading
            with open(bb, 'r') as file:
                line = file.readlines()[i].split(',')[:-1]
                my_list.append(line)
    
    elif type=="yolo":
        f=open(bb,'r')
        x=(float(f.readlines()[0].split(" ")[1:][0]))
        f.close()

        f=open(bb,'r')
        y=(float(f.readlines()[0].split(" ")[1:][1]))
        f.close()

        f=open(bb,'r')
        w=(float(f.readlines()[0].split(" ")[1:][2]))
        f.close()

        f=open(bb,'r')
        h=(float(f.readlines()[0].split(" ")[1:][3]))
        f.close()

        image_w=img2.size[0]
        image_h=img2.size[1]

        w = w * image_w
        h = h * image_h
        x1 = ((2 * x * image_w) - w)/2
        y1 = ((2 * y * image_h) - h)/2
        x2 = x1 + w
        y2 = y1 + h

        xmin = round(x1)
        xmax = round(x2)
        ymin = round(y1)
        ymax = round(y2)
        
        my_list=[xmin, ymax, xmax, ymax, xmax, ymin, xmin, ymin]
    # distance= 10
    points = 10
    for i in range(len(my_list)):
        x1,y1,x2,y2,x3,y3,x4,y4 = return_all_x_and_y(my_list[i])
        all_coordinates = find_all_coordinates(x1,y1,x2,y2,x3,y3,x4,y4)
        select_control_points = return_from_to(path,x1,y1,x2,y2,x3,y3,x4,y4)
        P_Points,Q_Points = check_p_q(all_coordinates,value,points)
        #--------- new random points p and q
        points_in_p =  P_Points  + select_control_points
        points_in_q =  Q_Points + select_control_points
        #----- into array
        points_in_p = np.array(points_in_p)
        points_in_q = np.array(points_in_q)

        #------ points x,y into y,x-----
        for i in range(len(points_in_p)):
            # for p swap
            temp = points_in_p[i][0]
            points_in_p[i][0] = points_in_p[i][1]
            points_in_p[i][1] = temp

            #for q swap
            temp1 = points_in_q[i][0]
            points_in_q[i][0] = points_in_q[i][1]
            points_in_q[i][1] = temp1
        
        # ------------ Function called -------------
        img_deformation = demo_auto(points_in_p,points_in_q,img2)

        img_deformation = cv2.cvtColor(img_deformation,cv2.COLOR_RGB2BGR)
        img2 = img_deformation.copy()
    img5 = Image.fromarray(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
    
    img_name = os.path.basename(img)
    img5.save(outdir+img_name)
    text_path = os.path.basename(bb)
    shutil.move(bb,outdir+text_path)
    return img, bb


def crop_image(dir, outdir, crop_num):
    '''
    A function to generate crop images without crossing the bounding box and image of interest
    image_path: path to the present image 
    bounding_box_path: path to the bounding box of the image
    warning: please provide the respective bounding box of the image
    crop_num: the number of crop image you want to generate
    destination_path: the path where you want to store the generated image and bounding box 
    note: image and bbox file will be in the same folder given in the destination_path
    '''
    # import the image and labels
    # for filename in os.listdir(dir):
    #     img = os.path.join(dir,filename)
    img = dir
    image = cv2.imread(img)
    img_name = os.path.basename(img)
    bb = img.replace('.jpg','.txt')
    bb_name = os.path.basename(bb)
    bboxes = open(bb, 'r')
    original_image = image.copy()
    height, width, _ = image.shape
    image = np.zeros_like(image)
    # converting the yolo format data to voc format
    bboxes = bboxes.readlines()
    voc_bboxes = []                 # to store the bounding box information to include them in the cropped image later 
    for bbox in bboxes:
        yolo_bbox = [float(value) for value in bbox.strip('\n').split(' ')[1:]]
        voc_bbox = pybboxes.convert_bbox(yolo_bbox, from_type='yolo', to_type='voc', image_size=(width, height))
        # assigning 255 for the restricted area
        image[voc_bbox[1]: voc_bbox[3], :] = 255
        image[:, voc_bbox[0]: voc_bbox[2]] = 255
        voc_bboxes.append(voc_bbox)
    voc_bboxes = np.array(voc_bboxes) # converting to np for fast and easy calculation 
    
    # storing the unrestricted points -- where a line drawn won't cross the bounding boxes
    image = cv2.threshold(
        cv2.cvtColor(image, cv2.COLOR_BGR2GRAY),
        100, 255, cv2.THRESH_BINARY_INV)[1]
    
    x_center, y_center = image.shape[1]//2, image.shape[0]//2
    x_lower_bound = []
    y_lower_bound = []
    x_upper_bound = []
    y_upper_bound = []

    for x_index_value, x in enumerate(image[0, :]):
        if x == 255:
            if x_index_value <= x_center:
                x_lower_bound.append(x_index_value)
            else: 
                x_upper_bound.append(x_index_value)
    for y_index_value, y in enumerate(image[:, 0]):
        if y == 255:
            if y_index_value <= y_center :
                y_lower_bound.append(y_index_value)
            else :
                y_upper_bound.append(y_index_value)
    if x_lower_bound == []:
        x_lower_bound.append(0)
    if y_lower_bound == []:
        y_lower_bound.append(0)
    if x_upper_bound == []:
        x_upper_bound.append(width)
    if y_upper_bound == []:
        y_upper_bound.append(height)

    # write a for loop to do this operation for n times -- generates maximum of n images, some cropped images may be discarded due to size requirements 
    for i in range(crop_num):
        # randomly get the coordinate
        random_quarter = np.random.randint(0, 2)
        if random_quarter == 0:
            x1 = np.random.choice(x_lower_bound, size=1, replace=False)[0]
            y1 = np.random.choice(y_lower_bound, size=1, replace=False)[0]
            x2 = np.random.choice(x_upper_bound, size=1, replace=False)[0]
            y2 = np.random.choice(y_upper_bound, size=1, replace=False)[0]

        elif random_quarter == 1:
            x1 = np.random.choice(x_lower_bound, size=1, replace=False)[0]
            y1 = np.random.choice(y_upper_bound, size=1, replace=False)[0]
            x2 = np.random.choice(x_upper_bound, size=1, replace=False)[0]
            y2 = np.random.choice(y_lower_bound, size=1, replace=False)[0]
        
        # a statement to save the crop image and the bounding box inside the crop image 
        # swap the values if 1 is greater than 2 -- we need to pass as x-tl, y-tl, x-br, y-br
        if x1 > x2:
            x2, x1 = x1, x2
        if y1 > y2:
            y2, y1 = y1, y2 

        cropped_image = original_image[y1:y2, x1:x2,:]
        cropped_height, cropped_width,  _ = cropped_image.shape
        # condition to get the list of bounding box present in the cropped image
        cropped_voc_bboxes =  voc_bboxes[(voc_bboxes[:,0] >= x1) & (voc_bboxes[:, 1] >= y1) & (voc_bboxes[:,2] <= x2) & (voc_bboxes[:, 3] <= y2) ]
        # skip if there is no bounding box in the image
        if not np.any(cropped_voc_bboxes):
            # print(f'null cropped image bbox {i}')
            continue
        # skip if the cropped image is too small, change this if you want small cropped images 
        MINIMUM_CROP_IMAGE_SIZE = 10
        if ((x2 - x1) == MINIMUM_CROP_IMAGE_SIZE) or ((y2 - y1) == MINIMUM_CROP_IMAGE_SIZE):
            continue
        
        # convert the bboxes from voc to yolo
        cv2.imwrite(os.path.join(outdir,img_name), cropped_image)
        with open(os.path.join(outdir,bb_name.replace('.jpg','.txt')), 'w+') as cropped_file:
            for cropped_voc_bbox in cropped_voc_bboxes:
                cropped_voc_bbox = [cropped_voc_bbox[0] - x1, cropped_voc_bbox[1] - y1, cropped_voc_bbox[2] - x1, cropped_voc_bbox[3] - y1]
                cropped_yolo_bbox = pybboxes.convert_bbox(cropped_voc_bbox, from_type='voc', to_type='yolo', image_size=(cropped_width, cropped_height))
                cropped_file.write(f"{bbox[0]} {cropped_yolo_bbox[0]} {cropped_yolo_bbox[1]} {cropped_yolo_bbox[2]} {cropped_yolo_bbox[3]}\n")

    return img,bb
