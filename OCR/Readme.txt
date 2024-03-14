This repository is about the augmentation of images that can used in object detection and recognition.

python main.py --dir=C:/Users/User/Desktop/Augmentation_Software/Data_Augmentation/OCR/samples/ --n=3x --rotate=-10to10 --blur=2to10 --contrast=-15to15 --elastic=300to400 --rigid=15to35 --recursion_rate=0.3 --percent=70 

dir: Input directory of images and after augmetation is completed, a folder named "Detection_Dataset" is created and all the augmented images are stored there.
x is times
rotate should be multiple of 5
blur should be multiple of 3
contrast should be mutiple of 10

Note: You can visualize the augmented images and it's bounding box by using https://github.com/lalchhabi/Data_Augmentation-/blob/master/OCR/Data_Visualizer/main_file.py file but before doing that you have to stop the process after augmentation.


