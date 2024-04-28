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
import torch
import pybboxes
from interp_torch import interp
import time

device = torch.device("cuda:0" if torch.cuda.is_available() else 'cpu') 
print(device)

def show_image(name,image):
    cv2.imshow(name,image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def rotate(dir,angle,outdir,n):  
    '''
    A function that generates augmented images by rotating the images in random multiple degrees.

    Parameters:
    dir (str): The path of the input directory.
    Angle (int): The angle of rotation.
    outdir (str): The path of the output directory.
    n (int): The number of times the image should be augmented.
    '''
    img=dir
    img2=Image.open(img)
    bb=img.replace('.jpg','.txt')
    f=open(bb,'r')
    l=len(f.readlines())
    f.close()
    def rotateBox(image,angle,bbox):
    # Load the image
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
    bbox_coordinates = []
    for i in range(0,l):
        f=open(bb,'r')
        x1, y1, x2, y2, x3, y3, x4, y4, label = f.readlines()[i].split(',')
        bobox = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], np.int32)
        imgo,cor=rotateBox(img2,angle,bobox)
        bbox_coordinates.append(cor.tolist() + [label])
        
    imgo.save(img)

    with open(bb,'w') as g :
        for cor in bbox_coordinates:
            g.write(str(str(cor) ).replace(']','').replace('[','') + '\n')
    
    return img, bb
    
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

    for bbox in bounding_boxes:
        bbox = bbox.strip().split(',')
        # Check if there are enough values (8) for valid annotation
        if len(bbox) != 9:
            print(f"Skipping invalid annotation: {bbox}")
            continue
        x1, y1, x2, y2, x3, y3, x4, y4, label = map(str.strip, bbox)
        x1, y1, x2, y2, x3, y3, x4, y4 = map(int, [x1, y1, x2, y2, x3, y3, x4, y4])

        # Rotate the bounding box points if the image was rotated
        if angle != 0:
            center_x = (x1 + x2 + x3 + x4) // 4
            center_y = (y1 + y2 + y3 + y4) // 4
            rotated_points = [
                rotate_point((x1, y1), (center_x, center_y), angle_radians),
                rotate_point((x2, y2), (center_x, center_y), angle_radians),
                rotate_point((x3, y3), (center_x, center_y), angle_radians),
                rotate_point((x4, y4), (center_x, center_y), angle_radians)
            ]
        else:
            rotated_points = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]

        # Adjust bounding box coordinates based on flip method
        if transform_methods[random_index] == Image.FLIP_LEFT_RIGHT:
            adjusted_bbox = [(image.width - x, y) for x, y in rotated_points]
        else:  # Image.FLIP_TOP_BOTTOM
            adjusted_bbox = [(x, image.height - y) for x, y in rotated_points]

        adjusted_bbox = [str(x) for point in adjusted_bbox for x in point]  # Flatten the list
        adjusted_bbox = ','.join(adjusted_bbox)
        adjusted_bounding_boxes.append(f"{adjusted_bbox},{label}")
  
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
    st = time.time()
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

    def mls_rigid_deformation_cpu(vy, vx, p, q, alpha=1.0, eps=1e-8):
        """ Rigid deformation
        
        Parameters
        ----------
        vx, vy: ndarray
            coordinate grid, generated by np.meshgrid(gridX, gridY)
        p: ndarray
            an array with size [n, 2], original control points, in (y, x) formats
        q: ndarray
            an array with size [n, 2], final control points, in (y, x) formats
        alpha: float
            parameter used by weights
        eps: float
            epsilon
        
        Return
        ------
            A deformed image.
        """
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

    def mls_rigid_deformation_gpu(vy, vx, p, q, alpha=1.0, eps=1e-8):
        """ Rigid deformation
        
        Parameters
        ----------
        vx, vy: torch.Tensor
            coordinate grid, generated by torch.meshgrid(gridX, gridY)
        p: torch.Tensor
            an array with size [n, 2], original control points, in (y, x) formats
        q: torch.Tensor
            an array with size [n, 2], final control points, in (y, x) formats
        alpha: float
            parameter used by weights
        eps: float
            epsilon
        
        Return
        ------
            A deformed image.
        """
        device = q.device
        q = q.short()
        p = p.short()

        # Exchange p and q and hence we transform destination pixels to the corresponding source pixels.
        p, q = q, p

        grow = vx.shape[0]  # grid rows
        gcol = vx.shape[1]  # grid cols
        ctrls = p.shape[0]  # control points

        # Compute
        reshaped_p = p.reshape(ctrls, 2, 1, 1)                                              # [ctrls, 2, 1, 1]
        reshaped_v = torch.cat((vx.reshape(1, grow, gcol), vy.reshape(1, grow, gcol)), dim=0)      # [2, grow, gcol]
        
        w = 1.0 / (torch.sum((reshaped_p - reshaped_v).float() ** 2, dim=1) + eps) ** alpha    # [ctrls, grow, gcol]
        w /= torch.sum(w, dim=0, keepdim=True)                                               # [ctrls, grow, gcol]
        
        pstar = torch.zeros((2, grow, gcol), dtype=torch.float32).to(device)
        for i in range(ctrls):
            pstar += w[i] * reshaped_p[i]                                                   # [2, grow, gcol]

        vpstar = reshaped_v - pstar                                                         # [2, grow, gcol]
        reshaped_vpstar = vpstar.reshape(2, 1, grow, gcol)                                  # [2, 1, grow, gcol]
        neg_vpstar_verti = vpstar[[1, 0],...]                                               # [2, grow, gcol]
        neg_vpstar_verti[1,...] = -neg_vpstar_verti[1,...]                                  
        reshaped_neg_vpstar_verti = neg_vpstar_verti.reshape(2, 1, grow, gcol)              # [2, 1, grow, gcol]
        mul_right = torch.cat((reshaped_vpstar, reshaped_neg_vpstar_verti), dim=1)    # [2, 2, grow, gcol]
        reshaped_mul_right = mul_right.reshape(2, 2, grow, gcol)                            # [2, 2, grow, gcol]

        # Calculate q
        reshaped_q = q.reshape((ctrls, 2, 1, 1))                                            # [ctrls, 2, 1, 1]
        qstar = torch.zeros((2, grow, gcol), dtype=torch.float32).to(device)
        for i in range(ctrls):
            qstar += w[i] * reshaped_q[i]                                                   # [2, grow, gcol]
        
        temp = torch.zeros((grow, gcol, 2), dtype=torch.float32).to(device)
        for i in range(ctrls):
            phat = reshaped_p[i] - pstar                                                    # [2, grow, gcol]
            reshaped_phat = phat.reshape(1, 2, grow, gcol)                                  # [1, 2, grow, gcol]
            reshaped_w = w[i].reshape(1, 1, grow, gcol)                                     # [1, 1, grow, gcol]
            neg_phat_verti = phat[[1, 0]]                                                   # [2, grow, gcol]
            neg_phat_verti[1] = -neg_phat_verti[1]
            reshaped_neg_phat_verti = neg_phat_verti.reshape(1, 2, grow, gcol)              # [1, 2, grow, gcol]
            mul_left = torch.cat((reshaped_phat, reshaped_neg_phat_verti), dim=0)     # [2, 2, grow, gcol]
            
            A = torch.matmul((reshaped_w * mul_left).permute(2, 3, 0, 1), 
                            reshaped_mul_right.permute(2, 3, 0, 1))                       # [grow, gcol, 2, 2]

            qhat = reshaped_q[i] - qstar                                                    # [2, grow, gcol]
            reshaped_qhat = qhat.reshape(1, 2, grow, gcol).permute(2, 3, 0, 1)            # [grow, gcol, 1, 2]

            # Get final image transfomer -- 3-D array
            temp += torch.matmul(reshaped_qhat, A).reshape(grow, gcol, 2)                      # [grow, gcol, 2]

        temp = temp.permute(2, 0, 1)                                                      # [2, grow, gcol]
        normed_temp = torch.norm(temp, dim=0, keepdim=True)                           # [1, grow, gcol]
        normed_vpstar = torch.norm(vpstar, dim=0, keepdim=True)                       # [1, grow, gcol]
        transformers = temp / normed_temp * normed_vpstar  + qstar                          # [2, grow, gcol]
        nan_mask = normed_temp[0] == 0

        # Replace nan values by interpolated values
        nan_mask_flat = torch.nonzero(nan_mask.view(-1), as_tuple=True)[0]
        nan_mask_anti_flat = torch.nonzero(~nan_mask.view(-1), as_tuple=True)[0]
        transformers[0][nan_mask] = interp(nan_mask_flat, nan_mask_anti_flat, transformers[0][~nan_mask])
        transformers[1][nan_mask] = interp(nan_mask_flat, nan_mask_anti_flat, transformers[1][~nan_mask])

        # Remove the points outside the border
        transformers[transformers < 0] = 0
        transformers[0][transformers[0] > grow - 1] = 0
        transformers[1][transformers[1] > gcol - 1] = 0
        
        return transformers.long()
        
        # ------------------ Return the rigid Deformation Image ---------------------------
    def demo_auto_cpu(p,q,image):  
        
        height, width,_= image.shape
        gridX = np.arange(width, dtype=np.int16)
        gridY = np.arange(height, dtype=np.int16)
        vy, vx = np.meshgrid(gridX, gridY)

        rigid = mls_rigid_deformation_cpu(vy, vx, p, q, alpha=1)
        aug3 = np.ones_like(image)
        aug3[vx, vy] = image[tuple(rigid)]
        return aug3
    
    def demo_auto_gpu(p,q,image):
        p = torch.tensor(p).to(device)
        q = torch.tensor(q).to(device)

        image_ = image.copy()
        image = torch.tensor(image_).to(device)
        
        height, width, _ = image.shape
        gridX = torch.arange(width, dtype=torch.int16).to(device)
        gridY = torch.arange(height, dtype=torch.int16).to(device)
        vy, vx = torch.meshgrid(gridX, gridY)
        # !!! Pay attention !!!: the shape of returned tensors are different between numpy.meshgrid and torch.meshgrid
        vy, vx = vy.transpose(0, 1), vx.transpose(0, 1)
        
        
        rigid = mls_rigid_deformation_gpu(vy, vx, p, q, alpha=1)
        aug3 = torch.ones_like(image).to(device)
        aug3[vx.long(), vy.long()] = image[tuple(rigid)]

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
        if coordinates == []:

            return [],[]
        else:
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
    
    def tensor_to_cpu_image(tensor):
        # Move tensor to CPU and convert to NumPy array
        image_np_1 = tensor.cpu().numpy()
        # print("shape",image_np.shape)
        # show_image("deform",image_np)

        # Convert from CHW to HWC (assuming tensor is in CHW format)
        image_np = np.transpose(image_np_1, (1, 2, 0))
        # Convert to uint8 (assuming image is in float format)
        image_np_after_transpose = (image_np * 255).astype(np.uint8)
        return image_np_1,image_np_after_transpose
    

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
    img2_copy = img2.copy()
    new_blank_image = np.zeros_like(img2,dtype='uint8')
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

    else:
        for i in range(lent):
        # Open the file for reading
            with open(bb, 'r') as file:
                line = file.readlines()[i].split(',')[:-1]
                my_list.append(line)
    # distance= 10
    points = value
    # an = time.time()
    for i in range(len(my_list)):
        x1,y1,x2,y2,x3,y3,x4,y4 = return_all_x_and_y(my_list[i])
        all_coordinates = find_all_coordinates(x1,y1,x2,y2,x3,y3,x4,y4)
        select_control_points = return_from_to(path,x1,y1,x2,y2,x3,y3,x4,y4)
        P_Points,Q_Points = check_p_q(all_coordinates,value,points)
        # print("Analy
        # sis",time.time() - an)
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
        # if device == 'cuda:0':
        ans = time.time()
        img_deformation = demo_auto_gpu(points_in_p,points_in_q,img2_copy)
        img_deformation,image_np_after_transpose = tensor_to_cpu_image(img_deformation)
        
        img2_copy = img_deformation.copy()

    img5 = Image.fromarray(img2_copy)
    
    img_name = os.path.basename(img)
    img5.save(outdir+img_name)
    text_path = os.path.basename(bb)
    shutil.move(bb,outdir+text_path)
    # print("Rigid TIme:",time.time()-st)
    return img, bb
