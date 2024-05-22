
It is important to train the text detection and recognition model with a variety of data to increase the robustness of the model. However it is difficult to collect all the possible variations 
of data in real time, hence data augmentation techniques will be used to generate data with many variations that mimic industrial real-time data.Every image is augmented with various augmentation 
techniques recursively and randomly. Augmentation techniques such as rotation, blur, contrast adjustment, flipping, elastic and rigid transformation are applied. For customization in augmentation, 
each technique is assigned with probability or weight value.

dir: Input directory of images and after augmetation is completed, a folder named "Detection_Dataset" is created and all the augmented images are stored there.
x is times
rotate should be multiple of 5
blur should be multiple of 3
contrast should be mutiple of 10
rigid value is directly proportional to the time.
Note: You can visualize the augmented images and it's bounding box by using https://github.com/lalchhabi/Data_Augmentation-/blob/master/OCR/Data_Visualizer/main_file.py file but before doing that you have to stop the process after augmentation.

To run this file :-
For Text Detection or OCR
python main.py --dir=/home/swordlord/crimson_tech/Data_Augmentation/good_tags --label_format=YOLO8  --n=10x --rotate=-10to10 --blur=3to15 --contrast=-15to15 --elastic=300to400 --rigid=0to5 --recursion_rate=0.5 --percent=70 

For Object Detection or YOLO
In YOLO to generate more variety on data, Image crop method is also applied randomly such that it preserves the data inside the bounding box.

python main.py --dir='/home/swordlord/crimson_tech/Data_Augmentation/good_tags' --n=30x --rotate=-10to10 --blur=2to10 --contrast=-15to15 --elastic=300to400 --rigid=15to35 --recursion_rate=0.4 --crop_no=3to5 --percent=70

<img alt = 'coding' width = "1000" height = "500" src = "https://github.com/lalchhabi/Data_Augmentation/blob/master/augmentation_process.jpg">

python check_annotation/main.py '/home/swordlord/crimson_tech/Data_Augmentation/tags_obb.v1i.yolov5-obb/test/images' '/home/swordlord/crimson_tech/Data_Augmentation/tags_obb.v1i.yolov5-obb/test/label' 