import os
import cv2

def convert_and_normalize_yolo8(label_lines, image_width, image_height):
    converted_labels = []
    for line in label_lines:
        # Split the line by comma
        words = line.split(',')
        # Pop the last word, strip whitespace and '\n', and insert it at the beginning
        last_word = words.pop().strip()
        last_word = last_word.replace('\n', '').replace('\\n', '').replace(' ', '').replace("'", '')
        words.insert(0, last_word)
        # Normalize the coordinates
        for i in range(1, len(words)):
            words[i] = str(float(words[i]) / image_width) if i % 2 != 0 else str(float(words[i]) / image_height)
        # Join the words back into a line
        converted_labels.append(' '.join(words))
    return converted_labels

def label_converter_main(txt_file, label_format):
    valid_formats = ['YOLO5', 'OCR', 'YOLO8']
    if label_format not in valid_formats:
        print("Invalid label format argument. Please specify YOLO5, OCR, or YOLO8.")
        return

    # Read the text file
    with open(txt_file, 'r') as file:
        lines = file.readlines()

    # Get the path of the image file (same path, different extension)
    img_file = os.path.splitext(txt_file)[0] + '.jpg'

    # Check if image file exists
    if not os.path.isfile(img_file):
        print("Image file not found:", img_file)
        return

    # Open the image file and get its dimensions
    img = cv2.imread(img_file)
    if img is None:
        print("Error: Unable to read image file.")
        return
    height, width, _ = img.shape

    converted_labels = convert_and_normalize_yolo8(lines, width, height)

    # Write converted labels to the original text file
    with open(txt_file, 'w') as file:
        for label in converted_labels:
            file.write(label + '\n')

