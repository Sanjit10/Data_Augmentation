import os
import cv2

def convert_to_yolo8(lines_array):
    # Convert each line to a list of words
    lines_array = [line.split(',') for line in lines_array]
    # For each list of words, pop the last word, replace '\n' with whitespace, and insert it at the beginning
    for line in lines_array:
        last_word = line.pop().strip()
        last_word=last_word.replace('\n', '').replace('\\n', '').replace(' ', '').replace("'", '')
        line.insert(0, last_word)  # Replace '\n' with whitespace

    # Convert each list of words back into a string
    lines_array = [','.join(line) for line in lines_array]

    return lines_array

def normalize_yolo8(label, image_width, image_height):
    # Convert the label to a list of words
    for lab in label:
        lab = lab.split(',')

        # Normalize the coordinates
        ret_label = []  
        for lab in label:
            lab = lab.split(',')
            # Normalize the coordinates
            for ele in range(1,len(lab)):
                if(ele % 2 ==0): #y-coordinates
                    lab[ele] = str(float(lab[ele])/image_height)
                else: #x-coordinates
                    lab[ele] = str(float(lab[ele])/image_width)
            lab = ','.join(lab)
            ret_label.append(lab)
    return ret_label


def label_converter_main(txt_file, label_format):
    """
    Converts the labels in a text file to a specified format and writes the converted labels back to the file.

    Args:
        txt_file (str): The path to the text file containing the labels.
        label_format (str): The desired format for the labels. Valid options are 'YOLO5', 'OCR', or 'YOLO8'.

    Returns:
        None

    Raises:
        None
    """

    # Read the text file
    with open(txt_file, 'r') as file:
        lines = file.readlines()
    
    # Convert lines to lines_array
    lines_array = [line.strip() for line in lines]

    if label_format == 'YOLO8':
        converted_lines_array = convert_to_yolo8(lines_array)
    else:
        print("Invalid label format argument. Please specify YOLO5, OCR, or YOLO8.")
        return

    # Get the path of the image file (same path, different extension)
    img_file = os.path.splitext(txt_file)[0] + '.jpg'

    # Open the image file and get its dimensions
    img = cv2.imread(img_file)
    height, width, _ = img.shape

    converted_lines_array = normalize_yolo8(converted_lines_array, width, height)
    
    # Write converted lines_array to the original text file
    with open(txt_file, 'w') as file:
        for item in converted_lines_array:
            file.write(item + '\n')
