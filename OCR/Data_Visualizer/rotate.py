import cv2
import numpy as np

def rotateBox(image,angle,bbox,os):
# Load the image
    image=cv2.resize(image,os)
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
    return coordinates_text
