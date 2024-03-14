import cv2
import matplotlib.pyplot as plt
import os

# dir = os.path.join(os.getcwd(),'check')
dir = r'C:\Users\User\Desktop\Augmentation_Software\Yolo_Augmentation\pin_detection'
for filename in os.listdir(dir):
    if filename.endswith('.jpg' or '.png'):
        img_path = os.path.join(dir,filename)
        print("Image Name",filename)
        img = cv2.imread(img_path)
        img = cv2.resize(img,(500,500))
        dh, dw, _ = img.shape
        text_path = img_path.replace('.jpg','.txt')
        fl = open(text_path, 'r')
        data = fl.readlines()
        fl.close()

        for dt in data:
            _, x, y, w, h = map(float, dt.split(' '))
            l = int((x - w / 2) * dw)
            r = int((x + w / 2) * dw)
            t = int((y - h / 2) * dh)
            b = int((y + h / 2) * dh)
            
            if l < 0:
                l = 0
            if r > dw - 1:
                r = dw - 1
            if t < 0:
                t = 0
            if b > dh - 1:
                b = dh - 1

            cv2.rectangle(img, (l, t), (r, b), (0, 0, 255), 3)
            cv2.putText(img,str(_),(50,50),cv2.FONT_HERSHEY_SIMPLEX ,1,(255,0,255),2)

        cv2.imshow("Image",img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
