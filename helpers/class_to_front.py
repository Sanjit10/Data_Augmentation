import os

def process_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    modified_lines = []
    for line in lines:
        parts = line.strip().split(',')
        # Move the last element to the front
        modified_line = ','.join([parts[-1]] + parts[:-1])
        modified_lines.append(modified_line)
    
    with open(file_path, 'w') as file:
        for line in modified_lines:
            file.write(line + '\n')

def process_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            process_file(file_path)

if __name__ == '__main__':
    folder_path = '/home/swordlord/crimson_tech/Data_Augmentation/Dataset'  # Replace with the path to your folder
    process_folder(folder_path)
