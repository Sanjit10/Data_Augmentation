import cv2
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import random
import numpy as np
import math
import rotate


def yoloFormattocv(x1, y1, x2, y2, H, W):
    bbox_width = x2 * W
    bbox_height = y2 * H
    center_x = x1 * W
    center_y = y1 * H
    voc = []
    voc.append(center_x - (bbox_width / 2))
    voc.append(center_y - (bbox_height / 2))
    voc.append(center_x + (bbox_width / 2))
    voc.append(center_y + (bbox_height / 2))

    return [int(v) for v in voc]


def cvFormattoYolo(corner, H, W):
    bbox_W = corner[3] - corner[1]
    bbox_H = corner[4] - corner[2]

    center_bbox_x = (corner[1] + corner[3]) / 2
    center_bbox_y = (corner[2] + corner[4]) / 2

    return corner[0], round(center_bbox_x / W, 6), round(center_bbox_y / H, 6), round(bbox_W / W, 6), round(bbox_H / H,
                                                                                                            6)


def box_nochange(file_num, text):
    with open(file_num + ".txt", 'w') as file:
        file.write(text)
    return text


def shear_box(direc, file_num, text, shearfactor):
    coordinates = []
    all = text.splitlines()
    for k in all:
        coordinates.append(k.split())

    for coordinate in coordinates:
        coordinate[0] = int(coordinate[0])
        for i in range(1, len(coordinate)):
            coordinate[i] = float(coordinate[i])

    if direc == 0:  # x - shearing
        for coordinate in coordinates:
            x_mid = coordinate[1] * 1 + coordinate[2] * (shearfactor // 2)
            y_mid = coordinate[2]
            width = coordinate[3] * (1 - shearfactor / 3)
            height = coordinate[4]
            coordinate[1], coordinate[2] = x_mid, y_mid
            coordinate[3], coordinate[4] = width, height
    else:  # y -shearing
        for coordinate in coordinates:
            x_mid = coordinate[1]
            y_mid = (coordinate[1] * (shearfactor // 2)) + coordinate[2] * 1
            width = (1 + shearfactor // 2) * coordinate[3]
            height = coordinate[4] * abs(1 - (coordinate[4] / shearfactor) / 2)
            coordinate[1], coordinate[2] = x_mid, y_mid
            coordinate[3], coordinate[4] = width, height

    with open(file_num+".txt", 'w') as file:
        coordinates_text = ""
        for coordinate in coordinates:
            coordinates_text += "%d %.6f %.6f %.6f %.6f\n" % (coordinate[0], coordinate[1], coordinate[2],
                                                              coordinate[3], coordinate[4])
        file.write(coordinates_text)
    return coordinates_text


def rotate_box(filename, image, file_num, text, angle,org_shape):

    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    height, width = image.shape[:2]
    image_center = (width / 2, height / 2)  # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape

    

    org_image = Image.open(filename)
    #rotation_angle = angle * np.pi / 180
    rotation_angle=angle
    # rot_matrix = np.array(
    #     [[np.cos(rotation_angle), -np.sin(rotation_angle)], [np.sin(rotation_angle), np.cos(rotation_angle)]])
    W, H = org_image.size[:2]
    image_center = (W/ 2, H / 2)  # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape
    

    bbox = []
    all = text.splitlines()
    for k in all:
        bbox.append(k.split(','))
    
    
    ab=[]
    for z in range(0,len(bbox)):    
        x1=int(bbox[z][0].replace(',',''))
        y1=int(bbox[z][1].replace(',',''))

        x2=int(bbox[z][2].replace(',',''))
        y2=int(bbox[z][3].replace(',',''))

        x3=int(bbox[z][4].replace(',',''))
        y3=int(bbox[z][5].replace(',',''))

        x4=int(bbox[z][6].replace(',',''))
        y4=int(bbox[z][7].replace(',',''))
        
        #coordinates_text=np.array([x1,y1,x2,y2,x3,y3,x4,y4])
        bobox = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], np.int32)
        
        coordinates_text=rotate.rotateBox(image,angle,bobox,org_shape)
        coordinates_text = np.array2string(coordinates_text, separator=',')
        coordinates_text=str(coordinates_text).replace('[','').replace(']','')+","+str((all[z].split(','))[8])
        ab.append(coordinates_text)

    abb = "\n".join(str(x) for x in ab)
    coordinates_text=abb
    with open(file_num + ".txt", 'w') as file:
        file.write(str(coordinates_text))
    
    return coordinates_text
    

def hrFlip_box(file_num, text):
    coordinates = []
    all = text.splitlines()
    for k in all:
        coordinates.append(k.split())

    for coordinate in coordinates:
        coordinate[0] = int(coordinate[0])
        for i in range(1, len(coordinate)):
            coordinate[i] = float(coordinate[i])
        coordinate[1] = abs(1 - coordinate[1])  # Changing only the x value of the center coordinate for hor. flip.

    with open(file_num + ".txt", 'w') as file:
        coordinates_text = ""
        for coordinate in coordinates:
            coordinates_text += "%d %.6f %.6f %.6f %.6f\n" % (coordinate[0], coordinate[1], coordinate[2],
                                                              coordinate[3], coordinate[4])
        file.write(coordinates_text)

    return coordinates_text


def vrFlip_box(file_num, text):
    coordinates = []
    all = text.splitlines()
    for k in all:
        coordinates.append(k.split())

    for coordinate in coordinates:
        coordinate[0] = int(coordinate[0])
        for i in range(1, len(coordinate)):
            coordinate[i] = float(coordinate[i])
        coordinate[2] = abs(1 - coordinate[2])      # Changing only the y value of the center coordinate for ver. flip.

    with open(file_num+".txt", 'w') as file:
        coordinates_text = ""
        for coordinate in coordinates:
            coordinates_text += "%d %.6f %.6f %.6f %.6f\n" % (coordinate[0], coordinate[1], coordinate[2],
                                                              coordinate[3], coordinate[4])
        file.write(coordinates_text)
    return coordinates_text


def blur_gen(image, value):
    return image.filter(ImageFilter.GaussianBlur(value / 4))


def rotation_gen(image, value):
    
    
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    height, width = image.shape[:2]
    image_center = (width / 2, height / 2)  # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape

    rotation_mat = cv2.getRotationMatrix2D(image_center, value, 1.)

    # rotation calculates the cos and sin, taking absolutes of those.
    abs_cos = abs(rotation_mat[0, 0])
    abs_sin = abs(rotation_mat[0, 1])

    # find the new width and height bounds
    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)

    # subtract old image center (bringing image back to origin) and adding the new image center coordinates
    rotation_mat[0, 2] += bound_w / 2 - image_center[0]
    rotation_mat[1, 2] += bound_h / 2 - image_center[1]

    # rotate image with the new bounds and translated rotation matrix
    rotated_mat = cv2.warpAffine(image, rotation_mat, (bound_w, bound_h))
    rgb = cv2.cvtColor(rotated_mat, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb), value


def shear_gen(image, value):
    l = []
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    x_m = np.float32([[1, value / 10, 0], [0, 1, 0], [0, 0, 1]])  # transformation matrix for x shearing
    x_factor = 1 + value / 10 # factor for changing the size of image
    x_sheared_img = cv2.warpPerspective(cv_image, x_m, (int(cv_image.shape[1] * x_factor), int(cv_image.shape[0])))
    y_m = np.float32([[1, 0, 0], [value / 10, 1, 0], [0, 0, 1]])
    y_factor = 1 + value / 10
    y_sheared_img = cv2.warpPerspective(cv_image, y_m, (int(cv_image.shape[1]), int(cv_image.shape[0] * y_factor)))
    x_rgb = cv2.cvtColor(x_sheared_img, cv2.COLOR_BGR2RGB)
    y_rgb = cv2.cvtColor(y_sheared_img, cv2.COLOR_BGR2RGB)
    x_img_pil = Image.fromarray(x_rgb)
    y_img_pil = Image.fromarray(y_rgb)
    l.extend([x_img_pil, y_img_pil])
    res = random.choice(l)
    return l.index(res), res, (1+(value/10))


def horizontal_flip_gen(image):
    return image.transpose(Image.FLIP_LEFT_RIGHT)


def vertical_flip_gen(image):
    return image.transpose(Image.FLIP_TOP_BOTTOM)


def darken_gen(image, value):
    return ImageEnhance.Brightness(image).enhance(1.0 - value / 100)


def brighten_gen(image, value):
    return ImageEnhance.Brightness(image).enhance(1.0 + value / 30)


def noise_gen(image, value):
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    rows, columns, channels = img.shape
    output = np.zeros(img.shape, np.uint8)

    value = value / 100
    threshold = 1 - value
    for i in range(rows):
        for j in range(columns):
            r = random.random()
            if r < value:
                output[i][j] = [0, 0, 0]
            elif r > threshold:
                output[i][j] = [255, 255, 255]
            else:
                output[i][j] = img[i][j]
    rgb1 = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(rgb1)
    return img_pil


def saturation_gen(image, value):
    l = []
    converter = ImageEnhance.Color(image)
    neg = converter.enhance(1.0 - value / 100)
    pos = converter.enhance(1.0 + value / 20)
    l.extend([neg, pos])
    return random.choice(l)


def grayscale_gen(image):
    return ImageOps.grayscale(image)


def cutout_gen(image):
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    x = random.randint(0, 125)
    y = random.randint(0, 125)
    w = random.randint(0, 50)
    h = random.randint(0, 50)
    for i in range(x, x + w):
        for j in range(y, y + h):
            cv_image[i][j] = 0
    img = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img)
    return img_pil


def bw_gen(image, value):
    return ImageOps.grayscale(image).point(lambda x: 0 if x < value else 255, '1')
