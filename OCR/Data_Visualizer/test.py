import cv2
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os
import shutil
from augmentation import *

dict_aug = {}


def generate(target):
    for i in img_file:
        operations = random.sample(dict_aug.keys(), random.randint(1, len(dict_aug)))
        image = Image.open(i)
        s=image.size
        text = ""
        with open(i[:-4] + ".txt", 'r') as file:
            text = file.read()
        out_txt = f"{os.path.splitext(i)[0].split('/')[-1]}_{target}"
        for operation in operations:
            if operation == "Blur":
                if dict_aug["Blur"]:
                    out = blur_gen(image, value=random.randint(1, dict_aug['Blur']))
                    image = out
                    text = box_nochange(out_txt, text)

            if operation == "Rotation":
                if dict_aug["Rotation"]:
                    out, angle= rotation_gen(image, value=random.randint(-dict_aug['Rotation'], dict_aug['Rotation']))
                    image = out
                    text = rotate_box(i, image, out_txt, text, angle,s)

            if operation == "Shear":
                if dict_aug["Shear"]:
                    direc, out, val = shear_gen(image, value=random.randint(0, dict_aug["Shear"]))
                    image = out
                    text = shear_box(direc, out_txt, text, val)

            if operation == "Horizontal Flip":
                if dict_aug["Horizontal Flip"]:
                    out = horizontal_flip_gen(image)
                    image = out
                    text = hrFlip_box(out_txt, text)

            if operation == "Vertical Flip":
                if dict_aug["Vertical Flip"]:
                    out = vertical_flip_gen(image)
                    image = out
                    text = vrFlip_box(out_txt, text)

            if operation == "Brighten":
                if dict_aug["Brighten"]:
                    out = brighten_gen(image, value=random.randint(1, dict_aug["Brighten"]))
                    image = out
                    text = box_nochange(out_txt, text)
            if operation == "Darken":
                if dict_aug["Darken"]:
                    out = darken_gen(image=image, value=random.randint(1, dict_aug["Darken"]))
                    image = out
                    text = box_nochange(out_txt, text)

            if operation == "Noise":
                if dict_aug["Noise"]:
                    out = noise_gen(image, value=random.randint(1, dict_aug["Noise"]))
                    image = out
                    text = box_nochange(out_txt, text)

            if operation == "Saturation":
                if dict_aug["Saturation"]:
                    out = saturation_gen(image, value=random.randint(1, dict_aug["Saturation"]))
                    image = out
                    text = box_nochange(out_txt, text)

            if operation == "Grayscale":
                if dict_aug["Grayscale"]:
                    out = grayscale_gen(image)
                    image = out
                    text = box_nochange(out_txt, text)

            if operation == "Cutout":
                if dict_aug["Cutout"]:
                    out = cutout_gen(image)
                    image = out
                    text = box_nochange(out_txt, text)

            if operation == "BW":
                if dict_aug["BW"]:
                    out = bw_gen(image, value=dict_aug["BW"])
                    image = out
                    text = box_nochange(out_txt, text)
        dir_name = "Augmented"
        if not os.path.isdir(dir_name):
            os.mkdir(dir_name)
        os.chdir(os.getcwd() + "/" + dir_name)
        f=os.getcwd()
        image.save(f"{f+'/'+out_txt}{os.path.splitext(i)[1]}")
        g=os.getcwd()[:-10]
        shutil.move(g+'/'+out_txt+'.txt',f+'/'+out_txt+'.txt')
        os.chdir(g)

        
        
    


class Augmentation(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Augmentation")
        self.resize(400, 400)

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setGeometry(QRect(10, 90, 300, 300))
        self.verticalLayout.setAlignment(Qt.AlignCenter)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setGeometry(QRect(80, 25, 200, 20))
        self.lineEdit.setReadOnly(True)

        pushButton = QPushButton("OPEN", self)
        pushButton.setGeometry(QRect(280, 25, 60, 20))
        pushButton.clicked.connect(self.open)

        self.verticalSpacer = QSpacerItem(20, 40)
        self.verticalLayout.addSpacerItem(self.verticalSpacer)

        self.checkBox = QCheckBox("Blur", self)
        self.verticalLayout.addWidget(self.checkBox)
        self.checkBox.clicked.connect(self.blur)

        self.checkBox_2 = QCheckBox("Rotation", self)
        self.verticalLayout.addWidget(self.checkBox_2)
        self.checkBox_2.clicked.connect(self.rotation)

        # self.checkBox_3 = QCheckBox("Shear", self)
        # self.verticalLayout.addWidget(self.checkBox_3)
        # self.checkBox_3.clicked.connect(self.shear)

        # self.checkBox_4 = QCheckBox("Flip", self)
        # self.verticalLayout.addWidget(self.checkBox_4)
        # self.checkBox_4.clicked.connect(self.flip)

        self.checkBox_5 = QCheckBox("Brightness", self)
        self.verticalLayout.addWidget(self.checkBox_5)
        self.checkBox_5.clicked.connect(self.brightness)

        self.checkBox_6 = QCheckBox("Noise", self)
        self.verticalLayout.addWidget(self.checkBox_6)
        self.checkBox_6.clicked.connect(self.noise)

        self.checkBox_7 = QCheckBox("Saturation", self)
        self.verticalLayout.addWidget(self.checkBox_7)
        self.checkBox_7.clicked.connect(self.saturation)

        self.checkBox_8 = QCheckBox("GrayScale", self)
        self.verticalLayout.addWidget(self.checkBox_8)
        self.checkBox_8.clicked.connect(self.grayscale)

        # self.checkBox_9 = QCheckBox("Cutout", self)
        # self.verticalLayout.addWidget(self.checkBox_9)
        # self.checkBox_9.clicked.connect(self.cutout)

        # self.checkBox_10 = QCheckBox("Black n White", self)
        # self.verticalLayout.addWidget(self.checkBox_10)
        # self.checkBox_10.clicked.connect(self.blackwhite)

        self.verticalSpacer = QSpacerItem(20, 40)
        self.verticalLayout.addSpacerItem(self.verticalSpacer)

        self.comboBox = QComboBox(self)
        for i in range(1, 51):
            self.comboBox.addItem(f"{i} images ({i}x)")
        self.verticalLayout.addWidget(self.comboBox)

        self.generateButton = QPushButton("Generate", self)
        self.verticalLayout.addWidget(self.generateButton)
        self.generateButton.clicked.connect(self.gen)

        self.show()

    def open(self):
        global filename, img_file
        filename = QFileDialog.getExistingDirectory(caption='Select a directory')
        #filename = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                               #'Images (*.png *.jpeg *.jpg *.bmp *.gif)')[0]
        #path = os.path.dirname(filename)
        os.chdir(filename)
        

        dir_name = "Augmented"
        if not os.path.isdir(dir_name):
            os.mkdir(dir_name)
        os.chdir(os.getcwd() + "/" + dir_name)
        self.lineEdit.setText(filename)
        f=os.getcwd()
        new_path = f[:-10]
        #new_path = f
        os.chdir(new_path)
        img_file = []
        EXT = ['.jpeg','.png','.jpg']
        mydir = os.listdir(new_path)
        #mydir=os.listdir(new_path+'/'+dir_name)
        for i in mydir:
            k = os.path.splitext(i)
            if k[1] in EXT:
                img_file.append(k[0]+k[1])
  
    
    def blur(self):
        if self.checkBox.isChecked():
            blu = Blur().exec_()
            if blu == QDialog.Rejected:
                self.checkBox.setChecked(False)
        else:
            if "Blur" in dict_aug:
                del dict_aug["Blur"]

    def rotation(self):
        if self.checkBox_2.isChecked():
            rot = Rotation().exec_()
            if rot == QDialog.Rejected:
                self.checkBox_2.setChecked(False)
        else:
            if "Rotation" in dict_aug:
                del dict_aug["Rotation"]

    def shear(self):
        if self.checkBox_3.isChecked():
            sh = Shear().exec_()
            if sh == QDialog.Rejected:
                self.checkBox_3.setChecked(False)
        else:
            if "Shear" in dict_aug:
                del dict_aug["Shear"]

    def flip(self):
        if self.checkBox_4.isChecked():
            f = Flip().exec_()
            if f == QDialog.Rejected:
                self.checkBox_4.setChecked(False)
        else:
            if "Horizontal Flip" in dict_aug:
                del dict_aug["Horizontal Flip"]
            if "Vertical Flip" in dict_aug:
                del dict_aug["Vertical Flip"]

    def brightness(self):
        if self.checkBox_5.isChecked():
            b = Brightness().exec_()
            if b == QDialog.Rejected:
                self.checkBox_5.setChecked(False)
        else:
            if "Brighten" in dict_aug:
                del dict_aug["Brighten"]
            if "Darken" in dict_aug:
                del dict_aug["Darken"]

    def noise(self):
        if self.checkBox_6.isChecked():
            n = Noise().exec_()
            if n == QDialog.Rejected:
                self.checkBox_6.setChecked(False)
        else:
            if "Noise" in dict_aug:
                del dict_aug["Noise"]

    def saturation(self):
        if self.checkBox_7.isChecked():
            sat = Saturation().exec_()
            if sat == QDialog.Rejected:
                self.checkBox_7.setChecked(False)
        else:
            if "Saturation" in dict_aug:
                del dict_aug["Saturation"]

    def grayscale(self):
        if self.checkBox_8.isChecked():
            gray = Grayscale().exec_()
            if gray == QDialog.Rejected:
                self.checkBox_8.setChecked(False)
        else:
            if "Grayscale" in dict_aug:
                del dict_aug["Grayscale"]

    def cutout(self):
        if self.checkBox_9.isChecked():
            cut = Cutout().exec_()
            if cut == QDialog.Rejected:
                self.checkBox_9.setChecked(False)
        else:
            if "Cutout" in dict_aug:
                del dict_aug["Cutout"]

    def blackwhite(self):
        if self.checkBox_10.isChecked():
            bw = BlackWhite().exec_()
            if bw == QDialog.Rejected:
                self.checkBox_10.setChecked(False)
        else:
            if "BW" in dict_aug:
                del dict_aug["BW"]

    def gen(self):
        n = self.comboBox.currentText().split(" ")[0]
        for i in range(int(n)):
            generate(i + 1)


class Blur(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blur")

        self.gridLayout = QGridLayout(self)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Apply)
        self.buttonBox.setLayoutDirection(Qt.RightToLeft)
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 3)
        self.buttonBox.clicked.connect(self.action)

        self.original = QLabel(self)
        self.original.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.original, 0, 0)

        self.blur = QLabel(self)
        self.blur.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.blur, 1, 0)

        self.slider = QSlider(self)
        self.slider.setMaximum(60)
        self.slider.setOrientation(Qt.Vertical)
        self.slider.valueChanged.connect(self.updateLabel)
        self.slider.valueChanged[int].connect(self.changedValue)
        self.gridLayout.addWidget(self.slider, 0, 2, 2, 1)

        self.label = QLabel("0.0px", self)
        self.label.setFixedWidth(50)
        self.label.setAlignment(Qt.AlignHCenter)
        self.gridLayout.addWidget(self.label, 0, 1)
        for i in img_file:
            image = Image.open(i)
            image = image.resize((200, 200))

            self.org_image = image.convert("RGB")
            data = self.org_image.tobytes("raw", "RGB")
            qim = QImage(data, self.org_image.size[0], self.org_image.size[1], QImage.Format_RGB888)
            self.pix = QPixmap.fromImage(qim)
            self.original.setPixmap(self.pix)
            self.blur.setPixmap(self.pix)

            self.show()

    def updateLabel(self, value):
        self.label.setText(f"{value / 4}px")

    def changedValue(self, value):
        for i in img_file:
            image = Image.open(i)
            image = image.resize((200, 200))
            self.org_image = image.convert("RGB")
            blur_img = self.org_image
            blur_image = blur_img.filter(ImageFilter.GaussianBlur(value / 4))
            b_data = blur_image.tobytes("raw", "RGB")
            b_qim = QImage(b_data, blur_image.size[0], blur_image.size[1], QImage.Format_RGB888)
            blur_pix = QPixmap.fromImage(b_qim)
            self.blur.setPixmap(blur_pix)

    def action(self, button):
        btn = self.buttonBox.standardButton(button)
        if btn == QDialogButtonBox.Apply:
            dict_aug["Blur"] = self.slider.value()
            self.accept()
        else:
            self.reject()


class Rotation(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rotation")

        self.gridLayout = QGridLayout(self)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Apply)
        self.buttonBox.setLayoutDirection(Qt.RightToLeft)
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 4)
        self.buttonBox.clicked.connect(self.action)

        self.original = QLabel(self)
        self.original.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.original, 0, 0, 1, 2)

        self.negative = QLabel(self)
        self.negative.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.negative, 1, 0, 1, 1)

        self.positive = QLabel(self)
        self.positive.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.positive, 1, 1, 1, 1)

        self.slider = QSlider(self)
        self.slider.setMaximum(90)
        self.slider.setOrientation(Qt.Vertical)
        self.slider.valueChanged.connect(self.updateLabel)
        self.slider.valueChanged[int].connect(self.changedValue)
        self.gridLayout.addWidget(self.slider, 0, 3, 2, 1)

        self.label = QLabel("0˚", self)
        self.label.setFixedWidth(30)
        self.label.setAlignment(Qt.AlignHCenter)
        self.gridLayout.addWidget(self.label, 0, 2)
        for i in img_file:
            image = Image.open(i)
        
            image = image.resize((200, 200))

            self.org_image = image.convert("RGB")
            data = self.org_image.tobytes("raw", "RGB")
            qim = QImage(data, self.org_image.size[0], self.org_image.size[1], QImage.Format_RGB888)
            self.pix = QPixmap.fromImage(qim)
            self.original.setPixmap(self.pix)
            self.negative.setPixmap(self.pix)
            self.positive.setPixmap(self.pix)

            self.show()

    def updateLabel(self, value):
        self.label.setText(f"{value}˚")

    def changedValue(self, value):
        if value != 0:
            for i in img_file:
                image = Image.open(i)
                image = image.resize((200, 200))
                self.org_image = image.convert("RGB")
                img = self.org_image
                data = self.org_image.tobytes("raw", "RGB")
                qim = QImage(data, self.org_image.size[0], self.org_image.size[1], QImage.Format_RGB888)
                self.pix = QPixmap.fromImage(qim)
                self.original.setPixmap(self.pix)
                self.negative.setPixmap(self.pix)
                self.positive.setPixmap(self.pix)
                neg_rot_image = img.rotate(value, resample=Image.BICUBIC, expand=True)
                pos_rot_image = img.rotate(-value, resample=Image.BICUBIC, expand=True)
                neg_rot_image = neg_rot_image.resize((200, 200))
                pos_rot_image = pos_rot_image.resize((200, 200))
                neg_rot_image_data = neg_rot_image.tobytes("raw", "RGB")
                pos_rot_image_data = pos_rot_image.tobytes("raw", "RGB")
                neg_qim = QImage(neg_rot_image_data, img.size[0], img.size[1], QImage.Format_RGB888)
                pos_qim = QImage(pos_rot_image_data, img.size[0], img.size[1], QImage.Format_RGB888)
                neg_pix = QPixmap.fromImage(neg_qim)
                pos_pix = QPixmap.fromImage(pos_qim)
                self.negative.setPixmap(neg_pix)
                self.positive.setPixmap(pos_pix)
        else:
            for i in img_file:
                image = Image.open(i)
            
                image = image.resize((200, 200))

                self.org_image = image.convert("RGB")
                data = self.org_image.tobytes("raw", "RGB")
                qim = QImage(data, self.org_image.size[0], self.org_image.size[1], QImage.Format_RGB888)
                self.pix = QPixmap.fromImage(qim)
                self.original.setPixmap(self.pix)
                self.negative.setPixmap(self.pix)
                self.positive.setPixmap(self.pix)
                img = self.org_image

                self.negative.setPixmap(self.pix)
                self.positive.setPixmap(self.pix)

    def action(self, button):
        btn = self.buttonBox.standardButton(button)
        if btn == QDialogButtonBox.Apply:
            dict_aug["Rotation"] = self.slider.value()
            self.accept()
        else:
            self.reject()


# class Shear(QDialog):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Shear")

#         self.gridLayout = QGridLayout(self)

#         self.buttonBox = QDialogButtonBox(self)
#         self.buttonBox.setOrientation(Qt.Horizontal)
#         self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Apply)
#         self.buttonBox.setLayoutDirection(Qt.RightToLeft)
#         self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 4)
#         self.buttonBox.clicked.connect(self.action)

#         self.original = QLabel(self)
#         self.original.setAlignment(Qt.AlignCenter)
#         self.gridLayout.addWidget(self.original, 0, 0, 1, 2)

#         self.negative = QLabel(self)
#         self.negative.setAlignment(Qt.AlignCenter)
#         self.gridLayout.addWidget(self.negative, 1, 0, 1, 1)

#         self.positive = QLabel(self)
#         self.positive.setAlignment(Qt.AlignCenter)
#         self.gridLayout.addWidget(self.positive, 1, 1, 1, 1)

#         self.slider = QSlider(self)
#         self.slider.setMaximum(2)
#         self.slider.setOrientation(Qt.Vertical)
#         self.slider.valueChanged.connect(self.updateLabel)
#         self.slider.setMinimum(0)
#         self.slider.setMaximum(15)
#         self.slider.setValue(0)
#         self.slider.valueChanged[int].connect(self.changeShear)
#         self.gridLayout.addWidget(self.slider, 0, 3, 2, 1)

#         self.label = QLabel("0.0", self)
#         self.label.setFixedWidth(30)
#         self.label.setAlignment(Qt.AlignHCenter)
#         self.gridLayout.addWidget(self.label, 0, 2)
#         for i in img_file:
            
#             self.image = Image.open(i)
#             self.image = self.image.resize((200, 200))

#             self.img = cv2.imread(i, cv2.IMREAD_COLOR)
#             self.img = cv2.resize(self.img, (200, 200), interpolation=cv2.INTER_AREA)
#             self.cols = self.img.shape[1]  # taking width of image
#             self.rows = self.img.shape[0]  # taking height of image
#             self.image = self.image.convert("RGB")
#             data = self.image.tobytes("raw")

#             qim = QImage(data, self.image.size[0], self.image.size[1], QImage.Format_RGB888)
#             self.pix = QPixmap.fromImage(qim)
#             self.original.setPixmap(self.pix)
#             self.negative.setPixmap(self.pix)
#             self.positive.setPixmap(self.pix)
#             self.show()

#     def updateLabel(self, value):
#         self.label.setText(f'{value / 10}')

#     def xshear(self, shearfactor):
#         M = np.float32([[1, shearfactor, 0], [0, 1, 0], [0, 0, 1]])  # transformation matrix for x shearing
#         factor = 1 + shearfactor  # factor for changing the size of image
#         for i in img_file:
#             self.image = Image.open(i)
#             self.image = self.image.resize((200, 200))

#             self.img = cv2.imread(i, cv2.IMREAD_COLOR)
#             self.img = cv2.imread(i, cv2.IMREAD_COLOR)
#             self.img = cv2.resize(self.img, (200, 200), interpolation=cv2.INTER_AREA)
#             self.cols = self.img.shape[1]  # taking width of image
#             self.rows = self.img.shape[0]  # taking height of image
#             self.image = self.image.convert("RGB")
            
            
#             sheared_img = cv2.warpPerspective(self.img, M, (int(self.cols * factor), int(self.rows)))  # x sheared image
#             sheared_img = cv2.resize(sheared_img, (200, 200), interpolation=cv2.INTER_AREA)
#             return sheared_img

#     def yshear(self, shearfactor):
#         M = np.float32([[1, 0, 0], [shearfactor, 1, 0], [0, 0, 1]])
#         factor = 1 + shearfactor
#         for i in img_file:
#             self.image = Image.open(i)
#             self.image = self.image.resize((200, 200))

#             self.img = cv2.imread(i, cv2.IMREAD_COLOR)
#             self.img = cv2.imread(i, cv2.IMREAD_COLOR)
#             self.img = cv2.resize(self.img, (200, 200), interpolation=cv2.INTER_AREA)
#             self.cols = self.img.shape[1]  # taking width of image
#             self.rows = self.img.shape[0]  # taking height of image
#             self.image = self.image.convert("RGB")
            
#             sheared_img = cv2.warpPerspective(self.img, M, (int(self.cols), int(self.rows * factor)))
#             sheared_img = cv2.resize(sheared_img, (200, 200), interpolation=cv2.INTER_AREA)
#             return sheared_img

#     def changeShear(self, value):
#         if value != 0:
#             for i in img_file:
#                 self.image = Image.open(i)
#                 self.image = self.image.resize((200, 200))

#                 self.img = cv2.imread(i, cv2.IMREAD_COLOR)
#                 self.img = cv2.imread(i, cv2.IMREAD_COLOR)
#                 self.img = cv2.resize(self.img, (200, 200), interpolation=cv2.INTER_AREA)
#                 self.cols = self.img.shape[1]  # taking width of image
#                 self.rows = self.img.shape[0]  # taking height of image
#                 self.image = self.image.convert("RGB")
#                 img = self.image
#                 neg_rot_image = self.xshear(value / 10)
#                 pos_rot_image = self.yshear(value / 10)
#                 aligned1 = cv2.resize(neg_rot_image, (img.size[1] // 4 * 4, img.size[0] // 4 * 4), fx=0, fy=0,
#                                     interpolation=cv2.INTER_NEAREST)
#                 rgb1 = cv2.cvtColor(aligned1, cv2.COLOR_BGR2RGB)
#                 aligned2 = cv2.resize(pos_rot_image, (img.size[1] // 4 * 4, img.size[0] // 4 * 4), fx=0, fy=0,
#                                     interpolation=cv2.INTER_NEAREST)
#                 rgb2 = cv2.cvtColor(aligned2, cv2.COLOR_BGR2RGB)
#                 neg_qim = QImage(rgb1.data, img.size[0], img.size[1], QImage.Format_RGB888)
#                 pos_qim = QImage(rgb2.data, img.size[0], img.size[1], QImage.Format_RGB888)
#                 neg_pix = QPixmap.fromImage(neg_qim)
#                 pos_pix = QPixmap.fromImage(pos_qim)
#                 self.negative.setPixmap(neg_pix)
#                 self.positive.setPixmap(pos_pix)
#         else:
#             for i in img_file:
#                 self.image = Image.open(i)
#                 self.image = self.image.resize((200, 200))

#                 self.img = cv2.imread(i, cv2.IMREAD_COLOR)
#                 self.img = cv2.imread(i, cv2.IMREAD_COLOR)
#                 self.img = cv2.resize(self.img, (200, 200), interpolation=cv2.INTER_AREA)
#                 self.cols = self.img.shape[1]  # taking width of image
#                 self.rows = self.img.shape[0]  # taking height of image
#                 self.image = self.image.convert("RGB")
#                 self.negative.clear()
#                 self.positive.clear()
#                 self.negative.setPixmap(self.pix)
#                 self.positive.setPixmap(self.pix)

#     def action(self, button):
#         btn = self.buttonBox.standardButton(button)
#         if btn == QDialogButtonBox.Apply:
#             dict_aug["Shear"] = self.slider.value()
#             self.accept()
#         else:
#             self.reject()


class Flip(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flip")

        self.gridLayout = QGridLayout(self)

        self.original = QLabel(self)
        self.original.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.original, 0, 0, 1, 2)

        self.horizontal = QLabel(self)
        self.horizontal.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.horizontal, 1, 0, 1, 1)

        self.vertical = QLabel(self)
        self.vertical.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.vertical, 1, 1, 1, 1)

        self.verticalLayout = QVBoxLayout()

        self.h_checkbox = QCheckBox("Horizontal", self)
        self.h_checkbox.stateChanged.connect(self.h_connect)
        self.verticalLayout.addWidget(self.h_checkbox)

        self.v_checkbox = QCheckBox("Vertical", self)
        self.v_checkbox.stateChanged.connect(self.v_connect)
        self.verticalLayout.addWidget(self.v_checkbox)

        self.verticalLayout.addStretch()
        self.gridLayout.addLayout(self.verticalLayout, 0, 2)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Apply)
        self.buttonBox.setLayoutDirection(Qt.RightToLeft)
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 3)
        self.buttonBox.clicked.connect(self.action)
        for i in img_file:
                
            self.image = Image.open(i)
            self.image = self.image.resize((200, 200))
            self.image = self.image.convert("RGB")
            data = self.image.tobytes("raw", "RGB")
            qim = QImage(data, self.image.size[0], self.image.size[1], QImage.Format_RGB888)
            self.pix = QPixmap.fromImage(qim)
            self.original.setPixmap(self.pix)
            self.show()

    def h_connect(self):
        if self.h_checkbox.isChecked():
            for i in img_file:
                
                self.image = Image.open(i)
                self.image = self.image.resize((200, 200))
                self.image = self.image.convert("RGB")
                data = self.image.tobytes("raw", "RGB")
                qim = QImage(data, self.image.size[0], self.image.size[1], QImage.Format_RGB888)
                self.pix = QPixmap.fromImage(qim)
                self.original.setPixmap(self.pix)
                h = self.image.transpose(Image.FLIP_LEFT_RIGHT)
                h_data = h.tobytes("raw", "RGB")
                qim = QImage(h_data, h.size[0], h.size[1], QImage.Format_RGB888)
                h_pix = QPixmap.fromImage(qim)
                self.horizontal.setPixmap(h_pix)
        else:
            for i in img_file:
                
                self.image = Image.open(i)
                self.image = self.image.resize((200, 200))
                self.image = self.image.convert("RGB")
                data = self.image.tobytes("raw", "RGB")
                qim = QImage(data, self.image.size[0], self.image.size[1], QImage.Format_RGB888)
                self.pix = QPixmap.fromImage(qim)
                self.original.setPixmap(self.pix)
                h = self.image.transpose(Image.FLIP_LEFT_RIGHT)
                h_data = h.tobytes("raw", "RGB")
                qim = QImage(h_data, h.size[0], h.size[1], QImage.Format_RGB888)
                h_pix = QPixmap.fromImage(qim)
                self.horizontal.setPixmap(h_pix)
                self.horizontal.clear()

    def v_connect(self):
        if self.v_checkbox.isChecked():
            for i in img_file:
                
                self.image = Image.open(i)
                self.image = self.image.resize((200, 200))
                self.image = self.image.convert("RGB")
                data = self.image.tobytes("raw", "RGB")
                qim = QImage(data, self.image.size[0], self.image.size[1], QImage.Format_RGB888)
                self.pix = QPixmap.fromImage(qim)
                self.original.setPixmap(self.pix)
                v = self.image.transpose(Image.FLIP_TOP_BOTTOM)
                v_data = v.tobytes("raw", "RGB")
                qim = QImage(v_data, v.size[0], v.size[1], QImage.Format_RGB888)
                v_pix = QPixmap.fromImage(qim)
                self.vertical.setPixmap(v_pix)
        else:
            for i in img_file:
                
                self.image = Image.open(i)
                self.image = self.image.resize((200, 200))
                self.image = self.image.convert("RGB")
                data = self.image.tobytes("raw", "RGB")
                qim = QImage(data, self.image.size[0], self.image.size[1], QImage.Format_RGB888)
                self.pix = QPixmap.fromImage(qim)
                self.original.setPixmap(self.pix)
                v = self.image.transpose(Image.FLIP_TOP_BOTTOM)
                v_data = v.tobytes("raw", "RGB")
                qim = QImage(v_data, v.size[0], v.size[1], QImage.Format_RGB888)
                v_pix = QPixmap.fromImage(qim)
                self.vertical.setPixmap(v_pix)
                self.vertical.clear()

    def action(self, button):
        btn = self.buttonBox.standardButton(button)
        if btn == QDialogButtonBox.Apply:
            if self.h_checkbox.isChecked():
                dict_aug["Horizontal Flip"] = True
            if self.v_checkbox.isChecked():
                dict_aug["Vertical Flip"] = True
            self.accept()
        else:
            self.reject()


class Brightness(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Brightness")

        self.gridLayout = QGridLayout(self)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Apply)
        self.buttonBox.setLayoutDirection(Qt.RightToLeft)
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 4)
        self.buttonBox.clicked.connect(self.action)

        self.original = QLabel(self)
        self.original.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.original, 0, 0, 1, 2)

        self.darken = QLabel(self)
        self.darken.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.darken, 1, 0, 1, 1)

        self.brighten = QLabel(self)
        self.brighten.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.brighten, 1, 1, 1, 1)

        self.verticalLayout = QVBoxLayout()

        self.label = QLabel("0%", self)
        self.label.setFixedWidth(30)
        self.verticalLayout.addWidget(self.label)

        self.slider = QSlider(self)
        self.slider.setMaximum(99)
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.valueChanged.connect(self.updateLabel)
        self.slider.valueChanged[int].connect(self.changedValue)
        self.verticalLayout.addWidget(self.slider)

        self.d_checkbox = QCheckBox("Darken", self)
        self.d_checkbox.stateChanged.connect(self.changedValue)
        self.verticalLayout.addWidget(self.d_checkbox)

        self.b_checkbox = QCheckBox("Brighten", self)
        self.b_checkbox.stateChanged.connect(self.changedValue)
        self.verticalLayout.addWidget(self.b_checkbox)

        self.verticalLayout.addStretch()
        self.gridLayout.addLayout(self.verticalLayout, 0, 2)
        for i in img_file:
            self.image = Image.open(i)
            self.image = self.image.resize((200, 200))
            self.image = self.image.convert("RGB")
            data = self.image.tobytes("raw", "RGB")
            qim = QImage(data, self.image.size[0], self.image.size[1], QImage.Format_RGB888)
            self.pix = QPixmap.fromImage(qim)
            self.original.setPixmap(self.pix)

            self.show()

    def updateLabel(self, value):
        self.label.setText(f"{value}%")

    def changedValue(self):
        if self.d_checkbox.isChecked():
            for i in img_file:
                self.image = Image.open(i)
                self.image = self.image.resize((200, 200))
                self.image = self.image.convert("RGB")
                data = self.image.tobytes("raw", "RGB")
                qim = QImage(data, self.image.size[0], self.image.size[1], QImage.Format_RGB888)
                self.pix = QPixmap.fromImage(qim)
                self.original.setPixmap(self.pix)
                d = ImageEnhance.Brightness(self.image).enhance(1.0 - self.slider.value() / 100)
                d_data = d.tobytes("raw", "RGB")
                qim = QImage(d_data, d.size[0], d.size[1], QImage.Format_RGB888)
                d_pix = QPixmap.fromImage(qim)
                self.darken.setPixmap(d_pix)

        if self.b_checkbox.isChecked():
            for i in img_file:
                self.image = Image.open(i)
                self.image = self.image.resize((200, 200))
                self.image = self.image.convert("RGB")
                data = self.image.tobytes("raw", "RGB")
                qim = QImage(data, self.image.size[0], self.image.size[1], QImage.Format_RGB888)
                self.pix = QPixmap.fromImage(qim)
                self.original.setPixmap(self.pix)
                b = ImageEnhance.Brightness(self.image).enhance(1.0 + self.slider.value() / 30)
                b_data = b.tobytes("raw", "RGB")
                qim = QImage(b_data, b.size[0], b.size[1], QImage.Format_RGB888)
                b_pix = QPixmap.fromImage(qim)
                self.brighten.setPixmap(b_pix)

        if not self.d_checkbox.isChecked():
            for i in img_file:
                self.image = Image.open(i)
                self.image = self.image.resize((200, 200))
                self.image = self.image.convert("RGB")
                data = self.image.tobytes("raw", "RGB")
                qim = QImage(data, self.image.size[0], self.image.size[1], QImage.Format_RGB888)
                self.pix = QPixmap.fromImage(qim)
                self.original.setPixmap(self.pix)
                d = ImageEnhance.Brightness(self.image).enhance(1.0 - self.slider.value() / 100)
                d_data = d.tobytes("raw", "RGB")
                qim = QImage(d_data, d.size[0], d.size[1], QImage.Format_RGB888)
                d_pix = QPixmap.fromImage(qim)
                self.darken.setPixmap(d_pix)
                self.darken.clear()

        if not self.b_checkbox.isChecked():
            for i in img_file:
                self.image = Image.open(i)
                self.image = self.image.resize((200, 200))
                self.image = self.image.convert("RGB")
                data = self.image.tobytes("raw", "RGB")
                qim = QImage(data, self.image.size[0], self.image.size[1], QImage.Format_RGB888)
                self.pix = QPixmap.fromImage(qim)
                self.original.setPixmap(self.pix)
                b = ImageEnhance.Brightness(self.image).enhance(1.0 + self.slider.value() / 30)
                b_data = b.tobytes("raw", "RGB")
                qim = QImage(b_data, b.size[0], b.size[1], QImage.Format_RGB888)
                b_pix = QPixmap.fromImage(qim)
                self.brighten.setPixmap(b_pix)
                self.brighten.clear()

    def action(self, button):
        btn = self.buttonBox.standardButton(button)
        if btn == QDialogButtonBox.Apply:
            if self.d_checkbox.isChecked():
                dict_aug["Darken"] = self.slider.value()
            if self.b_checkbox.isChecked():
                dict_aug["Brighten"] = self.slider.value()
            self.accept()
        else:
            self.reject()


class Noise(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Noise")

        self.gridLayout = QGridLayout(self)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Apply)
        self.buttonBox.setLayoutDirection(Qt.RightToLeft)
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 4)
        self.buttonBox.clicked.connect(self.action)

        self.original = QLabel(self)
        self.original.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.original, 0, 0, 1, 2)

        self.negative = QLabel(self)
        self.negative.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.negative, 1, 0, 1, 1)

        self.slider = QSlider(self)
        self.slider.setOrientation(Qt.Vertical)
        self.slider.valueChanged.connect(self.updateLabel)
        self.slider.setMinimum(0)
        self.slider.setMaximum(20)
        self.slider.setValue(0)
        self.slider.valueChanged[int].connect(self.changed_noise)
        self.gridLayout.addWidget(self.slider, 0, 3, 2, 1)

        self.label = QLabel("0%", self)
        self.label.setFixedWidth(30)
        self.label.setAlignment(Qt.AlignHCenter)
        self.gridLayout.addWidget(self.label, 0, 2)
        for i in img_file:
            self.image = Image.open(i)
            self.image = self.image.resize((200, 200))
            self.image = self.image.convert("RGB")
            data = self.image.tobytes("raw", "RGB")
            qim = QImage(data, self.image.size[0], self.image.size[1], QImage.Format_RGB888)
            self.pix = QPixmap.fromImage(qim)
            self.original.setPixmap(self.pix)
            self.img = cv2.imread(i)
            self.img = cv2.resize(self.img, (200, 200), interpolation=cv2.INTER_AREA)
            self.changed_noise()
            self.show()

    def updateLabel(self, value):
        self.label.setText(f"{value}%")

    def noise(self, p):
        for i in img_file:
            self.image = Image.open(i)
            self.image = self.image.resize((200, 200))
            self.image = self.image.convert("RGB")
            data = self.image.tobytes("raw", "RGB")
            qim = QImage(data, self.image.size[0], self.image.size[1], QImage.Format_RGB888)
            self.pix = QPixmap.fromImage(qim)
            self.original.setPixmap(self.pix)
            self.img = cv2.imread(i)
            self.img = cv2.resize(self.img, (200, 200), interpolation=cv2.INTER_AREA)
            rows, columns, channels = self.img.shape
            output = np.zeros(self.img.shape, np.uint8)

            p = p / 100
            threshold = 1 - p
            for i in range(rows):
                for j in range(columns):
                    r = random.random()
                    if r < p:
                        output[i][j] = [0, 0, 0]
                    elif r > threshold:
                        output[i][j] = [255, 255, 255]
                    else:
                        output[i][j] = self.img[i][j]
            output = cv2.resize(output, (200, 200), interpolation=cv2.INTER_AREA)
            return output

    def changed_noise(self):
        for i in img_file:
            self.image = Image.open(i)
            self.image = self.image.resize((200, 200))
            self.image = self.image.convert("RGB")
            data = self.image.tobytes("raw", "RGB")
            qim = QImage(data, self.image.size[0], self.image.size[1], QImage.Format_RGB888)
            self.pix = QPixmap.fromImage(qim)
            self.original.setPixmap(self.pix)
            self.img = cv2.imread(i)
            self.img = cv2.resize(self.img, (200, 200), interpolation=cv2.INTER_AREA)
            img = self.image
            noise_image = self.noise(self.slider.value())
            aligned1 = cv2.resize(noise_image, (img.size[1] // 4 * 4, img.size[0] // 4 * 4), fx=0, fy=0,
                                interpolation=cv2.INTER_NEAREST)
            rgb1 = cv2.cvtColor(aligned1, cv2.COLOR_BGR2RGB)
            noise_qim = QImage(rgb1.data, img.size[0], img.size[1], QImage.Format_RGB888)
            noise_pix = QPixmap.fromImage(noise_qim)
            self.negative.setPixmap(noise_pix)

    def action(self, button):
        btn = self.buttonBox.standardButton(button)
        if btn == QDialogButtonBox.Apply:
            dict_aug["Noise"] = self.slider.value()
            self.accept()
        else:
            self.reject()


class Saturation(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Saturation")

        self.gridLayout = QGridLayout(self)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Apply)
        self.buttonBox.setLayoutDirection(Qt.RightToLeft)
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 4)
        self.buttonBox.clicked.connect(self.action)

        self.original = QLabel(self)
        self.original.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.original, 0, 0, 1, 2)

        self.negative = QLabel(self)
        self.negative.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.negative, 1, 0, 1, 1)

        self.positive = QLabel(self)
        self.positive.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.positive, 1, 1, 1, 1)

        self.slider = QSlider(self)
        self.slider.setOrientation(Qt.Vertical)
        self.slider.valueChanged.connect(self.updateLabel)
        self.slider.valueChanged[int].connect(self.changedValue)
        self.gridLayout.addWidget(self.slider, 0, 3, 2, 1)

        self.label = QLabel("0%", self)
        self.label.setFixedWidth(30)
        self.label.setAlignment(Qt.AlignHCenter)
        self.gridLayout.addWidget(self.label, 0, 2)
        for i in img_file:

            self.image = Image.open(i)
            self.image = self.image.resize((200, 200))
            self.image = self.image.convert("RGB")
            data = self.image.tobytes("raw", "RGB")
            qim = QImage(data, self.image.size[0], self.image.size[1], QImage.Format_RGB888)
            self.converter = ImageEnhance.Color(self.image)
            self.pix = QPixmap.fromImage(qim)
            self.original.setPixmap(self.pix)
            self.negative.setPixmap(self.pix)
            self.positive.setPixmap(self.pix)

            self.show()

    def updateLabel(self, value):
        self.label.setText(f"{value}%")

    def changedValue(self, value):
        if value != 0:
            for i in img_file:

                self.image = Image.open(i)
                self.image = self.image.resize((200, 200))
                self.image = self.image.convert("RGB")
                data = self.image.tobytes("raw", "RGB")
                qim = QImage(data, self.image.size[0], self.image.size[1], QImage.Format_RGB888)
                self.converter = ImageEnhance.Color(self.image)
                self.pix = QPixmap.fromImage(qim)
                self.original.setPixmap(self.pix)
                self.negative.setPixmap(self.pix)
                self.positive.setPixmap(self.pix)
                negative_image = self.converter.enhance(1.0 - value / 100)
                negative_image = negative_image.convert("RGB")
                negative_data = negative_image.tobytes("raw", "RGB")
                negative_qim = QImage(negative_data, negative_image.size[0], negative_image.size[1], QImage.Format_RGB888)
                negative_pix = QPixmap.fromImage(negative_qim)
                self.negative.setPixmap(negative_pix)
                positive_image = self.converter.enhance(1.0 + value / 20)
                positive_image = positive_image.convert("RGB")
                positive_data = positive_image.tobytes("raw", "RGB")
                positive_qim = QImage(positive_data, positive_image.size[0], positive_image.size[1], QImage.Format_RGB888)
                positive_pix = QPixmap.fromImage(positive_qim)
                self.positive.setPixmap(positive_pix)

    def action(self, button):
        btn = self.buttonBox.standardButton(button)
        if btn == QDialogButtonBox.Apply:
            dict_aug["Saturation"] = self.slider.value()
            self.accept()
        else:
            self.reject()


class Grayscale(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grayscale")

        self.gridLayout = QGridLayout(self)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Apply)
        self.buttonBox.setLayoutDirection(Qt.RightToLeft)
        self.gridLayout.addWidget(self.buttonBox, 2, 0)
        self.buttonBox.clicked.connect(self.action)

        self.original = QLabel(self)
        self.original.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.original, 0, 0)

        self.gray = QLabel(self)
        self.gray.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.gray, 1, 0)
        for i in img_file:

            image = Image.open(i)
            image = image.resize((200, 200))

            org_image = image.convert("RGB")
            data = org_image.tobytes("raw", "RGB")
            qim = QImage(data, org_image.size[0], org_image.size[1], QImage.Format_RGB888)
            pix = QPixmap.fromImage(qim)
            self.original.setPixmap(pix)

            gray_img = ImageOps.grayscale(org_image)
            gray_image = gray_img.convert("RGB")
            g_data = gray_image.tobytes("raw", "RGB")
            g_qim = QImage(g_data, gray_image.size[0], gray_image.size[1], QImage.Format_RGB888)
            gray_pix = QPixmap.fromImage(g_qim)
            self.gray.setPixmap(gray_pix)
            self.show()

    def action(self, button):
        btn = self.buttonBox.standardButton(button)
        if btn == QDialogButtonBox.Apply:
            dict_aug["Grayscale"] = True
            self.accept()
        else:
            self.reject()


class Cutout(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cutout")

        self.gridLayout = QGridLayout(self)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Apply)
        self.buttonBox.setLayoutDirection(Qt.RightToLeft)
        self.gridLayout.addWidget(self.buttonBox, 2, 0)
        self.buttonBox.clicked.connect(self.action)

        self.original = QLabel(self)
        self.original.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.original, 0, 0)

        self.negative = QLabel(self)
        self.negative.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.negative, 1, 0)
        for i in img_file:
            self.image = Image.open(i)
            self.image = self.image.resize((200, 200))
            self.image = self.image.convert("RGB")
            data = self.image.tobytes("raw", "RGB")
            qim = QImage(data, self.image.size[0], self.image.size[1], QImage.Format_RGB888)
            self.pix = QPixmap.fromImage(qim)
            self.original.setPixmap(self.pix)

            self.img = cv2.imread(i)
            self.img = cv2.resize(self.img, (200, 200), interpolation=cv2.INTER_AREA)
            #self.changedValue()
            self.show()

    def cut_image(self):
        for i in img_file:
            self.image = Image.open(i)
            self.image = self.image.resize((200, 200))
            self.image = self.image.convert("RGB")
            data = self.image.tobytes("raw", "RGB")
            qim = QImage(data, self.image.size[0], self.image.size[1], QImage.Format_RGB888)
            self.pix = QPixmap.fromImage(qim)
            self.original.setPixmap(self.pix)
            self.img = cv2.imread(i)
            self.img = cv2.resize(self.img, (200, 200), interpolation=cv2.INTER_AREA)

            x = random.randint(0, 125)
            y = random.randint(0, 125)
            w = random.randint(0, 50)
            h = random.randint(0, 50)
            for i in range(x, x + w):
                for j in range(y, y + h):
                    self.img[i][j] = 0
            return self.img

    def changedValue(self):
        for i in img:
            self.image = Image.open(i)
            self.image = self.image.resize((200, 200))
            self.image = self.image.convert("RGB")
            data = self.image.tobytes("raw", "RGB")
            qim = QImage(data, self.image.size[0], self.image.size[1], QImage.Format_RGB888)
            self.pix = QPixmap.fromImage(qim)
            self.original.setPixmap(self.pix)

            self.img = cv2.imread(i)
            self.img = cv2.resize(self.img, (200, 200), interpolation=cv2.INTER_AREA)
            img = self.image
            cutout = self.cut_image()
            aligned1 = cv2.resize(cutout, (img.size[1] // 4 * 4, img.size[0] // 4 * 4), fx=0, fy=0,
                                interpolation=cv2.INTER_NEAREST)
            rgb1 = cv2.cvtColor(aligned1, cv2.COLOR_BGR2RGB)
            cutout_qim = QImage(rgb1.data, img.size[0], img.size[1], QImage.Format_RGB888)
            cutout_pix = QPixmap.fromImage(cutout_qim)
            self.negative.setPixmap(cutout_pix)

    def action(self, button):
        btn = self.buttonBox.standardButton(button)
        if btn == QDialogButtonBox.Apply:
            dict_aug["Cutout"] = True
            self.accept()
        else:
            self.reject()


class BlackWhite(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Black & White")

        self.gridLayout = QGridLayout(self)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Apply)
        self.buttonBox.setLayoutDirection(Qt.RightToLeft)
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 3)
        self.buttonBox.clicked.connect(self.action)

        self.original = QLabel(self)
        self.original.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.original, 0, 0)

        self.black_white_image = QLabel(self)
        self.black_white_image.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.black_white_image, 1, 0)

        self.slider = QSlider(self)
        self.slider.setMaximum(255)
        self.slider.setOrientation(Qt.Vertical)
        self.slider.valueChanged.connect(self.updateLabel)
        self.slider.valueChanged[int].connect(self.changedValue)
        self.gridLayout.addWidget(self.slider, 0, 2, 2, 1)

        self.label = QLabel("0", self)
        self.label.setFixedWidth(40)
        self.label.setAlignment(Qt.AlignHCenter)
        self.gridLayout.addWidget(self.label, 0, 1)
        for i in img_file:
            image = Image.open(i)
            image = image.resize((200, 200))

            self.org_image = image.convert("RGB")
            data = self.org_image.tobytes("raw", "RGB")
            qim = QImage(data, self.org_image.size[0], self.org_image.size[1], QImage.Format_RGB888)
            pix = QPixmap.fromImage(qim)
            self.original.setPixmap(pix)
            self.changedValue()
            self.show()

    def updateLabel(self, value):
        self.label.setText(f"{value}")

    def changedValue(self):
        for i in img_file:
            image = Image.open(i)
            image = image.resize((200, 200))

            self.org_image = image.convert("RGB")
            temp = ImageOps.grayscale(self.org_image).point(lambda x: 0 if x < self.slider.value() else 255, '1')
            temp = temp.convert("RGB")
            data = temp.tobytes("raw", "RGB")
            qim = QImage(data, temp.size[0], temp.size[1], QImage.Format_RGB888)
            pix = QPixmap.fromImage(qim)
            self.black_white_image.setPixmap(pix)

    def action(self, button):
        btn = self.buttonBox.standardButton(button)
        if btn == QDialogButtonBox.Apply:
            dict_aug["BW"] = self.slider.value()
            self.accept()
        else:
            self.reject()