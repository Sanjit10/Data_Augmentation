import cv2
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
#from PyQt5 import QtCore, QtGui
#from PyQt5.QtGui import QIcon, QFont, QPixmap, QStandardItemModel, QStandardItem
import os
from test import Augmentation
import numpy as np


frameWidth = 640
frameHeight = 480
EXT = [".jpg", ".png", ".jpeg"]

counter = 0
points = []
labels = []


def mouseClick(event, x, y, flags, param):
    global counter, points
    if event == cv2.EVENT_LBUTTONDOWN:
        points = [(x, y)]
        points.append((x, y))
        counter = 1
    if event == cv2.EVENT_LBUTTONUP:
        counter = 0
    if counter == 1 and event == cv2.EVENT_MOUSEMOVE:
        # points.append([x, y])
        points[1] = (x, y)
    return points


def box(window, image):
    # if counter == 1:
    #     cv2.rectangle(image, (points[0][0], points[0][1]), (points[-1][0], points[-1][1]), (0, 0, 255), 1)

    if counter == 0 and len(set(points)) > 1:
        cv2.rectangle(image, (points[0][0], points[0][1]), (points[1][0], points[1][1]), (0, 255, 0), 2)
        cv2.imshow(window, image)
        Window().labels_pop_up()
        points.clear()

    cv2.imshow(window, image)
    cv2.setMouseCallback(window, mouseClick)


class Dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Labels")
        self.resize(200, 320)
        layout = QVBoxLayout(self)

        self.line = QLineEdit(self)
        layout.addWidget(self.line)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.rejected.connect(self.cancel)
        self.buttonBox.accepted.connect(self.ok)
        layout.addWidget(self.buttonBox)

        self.listw = QListWidget(self)
        self.listw.itemClicked.connect(self.fill)
        self.listw.setSortingEnabled(True)
        layout.addWidget(self.listw)

    def fill(self, item):
        self.line.setText(item.text())

    def yolo_txt(self):
        x_min = points[0][0]
        x_max = points[-1][0]
        y_min = points[0][1]
        y_max = points[-1][1]
        x_center = float((x_min + x_max)) / 2 / shape[1]
        y_center = float((y_min + y_max)) / 2 / shape[0]
        w = float((x_max - x_min)) / shape[1]
        h = float((y_max - y_min)) / shape[0]
        label_index = labels.index(self.line.text())
        
        return label_index, x_center, y_center, w, h

        

    def ok(self):
        '''
        textboxVal = self.line.text()
        labels.append(textboxVal)
        '''
        label_index, x_center, y_center, w, h = self.yolo_txt()
        
        with open(os.path.splitext(item)[0] + ".txt", "a") as file:
            file.write("%d %.6f %.6f %.6f %.6f\n" % (label_index, x_center, y_center, w, h))
            
        self.close()
        
    def cancel(self):
        self.close()


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OCR Detection Augmentation Software")
        self.resize(850, 400)

        # logo

        label0 = QLabel(self)
        pixmap = QPixmap("main logo.png")
        pixmap=pixmap.scaled(int(pixmap.width()*0.12),int(pixmap.height()*0.12))
        label0.setPixmap(pixmap)
        label0.move(50, 50)
        # Label for Labels
        # label = QLabel("Enter a label", self)
        # label.setGeometry(QRect(100, 30, 200, 30))

        # LABEL for directory
        label2 = QLabel("Open directory", self)
        label2.setGeometry(QRect(500, 30, 200, 30))

        #LABEL for labels list
        # label3 = QLabel("Labels:", self)
        # label3.setGeometry(QRect(100, 60, 100, 100))

        # LABEL
        label4 = QLabel("Images:", self)
        label4.setGeometry(QRect(500, 60, 100, 100))

        # LIST WIDGET
        # self.list1 = QListWidget(self)
        # self.list1.setGeometry(QRect(100, 120, 200, 100))
        # self.list1.setSortingEnabled(True)

        # LIST WIDGET for Images
        self.list2 = QListWidget(self)
        self.list2.setGeometry(QRect(500, 120, 200, 100))
        self.list2.setSortingEnabled(True)
        self.list2.itemActivated.connect(self.open_selected)  # image can be opened by double click

        # TEXTBOX
        # self.textbox1 = QLineEdit(self)
        # self.textbox1.setGeometry(QRect(100, 60, 200, 30))
        # self.textbox1.setFocus()

        # TEXTBOX 2
        self.textbox2 = QLineEdit(self)
        self.textbox2.setGeometry(QRect(500, 60, 200, 30))
        self.textbox2.setReadOnly(True)

        # OK BUTTON
        # self.button1 = QPushButton("OK", self)
        # self.button1.setGeometry(QRect(300, 60, 45, 30))
        # self.button1.clicked.connect(self.ok_button)
        # self.button1.setShortcut("Return")

        # OPEN BUTTON
        button2 = QPushButton("OPEN", self)
        button2.setGeometry(QRect(700, 60, 60, 30))
        button2.clicked.connect(self.open)

        # REMOVE SELECTED BUTTON
        # button3 = QPushButton("Remove\nSelected", self)
        # button3.setToolTip('Click to remove selected label')
        # button3.setGeometry(QRect(100, 225, 100, 50))
        # button3.clicked.connect(self.remove_selected)

        # CLEAR ALL BUTTON
        # button4 = QPushButton("Clear ALL!", self)
        # button4.setToolTip('Click to remove all labels')
        # button4.setGeometry(QRect(200, 225, 100, 50))
        # button4.clicked.connect(self.clear_all)

        # OPEN SELECTED BUTTON
        button5 = QPushButton("Open\nSelected", self)
        button5.setToolTip('Click to open selected image')
        button5.setGeometry(QRect(500, 225, 100, 50))
        button5.clicked.connect(self.open_selected)

        # OPEN ALL BUTTON
        button6 = QPushButton("Open All", self)
        button6.setToolTip('Click to open all image')
        button6.setGeometry(QRect(600, 225, 100, 50))
        button6.clicked.connect(self.open_all)

        # START CAMERA BUTTON
        button7 = QPushButton("START CAMERA", self)
        button7.setToolTip('Click to open camera')
        button7.setStyleSheet("background-color: green")
        button7.setGeometry(QRect(200, 145, 100, 50))
        button7.clicked.connect(self.start_camera)

        # QUIT BUTTON
        button8 = QPushButton("QUIT", self)
        button8.setToolTip('Click to exit app')
        button8.setStyleSheet("background-color: red")
        button8.setGeometry(QRect(200, 215, 100, 50))
        button8.clicked.connect(self.quit)

        # AUGMENTATION BUTTON
        button9 = QPushButton("Augmentation", self)
        button9.setToolTip('Click to augment')
        button9.setStyleSheet("background-color: blue")
        button9.setGeometry(QRect(200, 75, 100, 50))
        button9.clicked.connect(self.augmentation)

    # ---------------------------------------------------------------------------------------------------------------#

    def quit(self):
        msg = QMessageBox()
        msg.setText("Are you sure you want to quit?")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        x = msg.exec_()
        if x == QMessageBox.Yes:
            cv2.destroyAllWindows()
            sys.exit(0)

    def ok_button(self):
        textboxVal = self.textbox1.text()
        print(textboxVal)
        if textboxVal not in labels:
            if len(textboxVal.strip()) != 0:
                labels.append(textboxVal)
                self.list1.addItem(textboxVal)
            else:
                msg = QMessageBox()
                msg.setText("Label can not be empty!\nPlease enter valid label.")
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()
        else:
            msg = QMessageBox()
            msg.setText(f"Label '{textboxVal}' already present!!!\nPlease enter New Label..")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
        self.textbox1.clear()

    def remove_selected(self):
        try:
            row = self.list1.currentRow()
            msg = QMessageBox()
            msg.setWindowTitle("Clear")
            msg.setText(f"Are you sure you want to delete '{self.list1.item(row).text()}'?")
            msg.setIcon(QMessageBox.Question)
            msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            x = msg.exec_()
            if x == QMessageBox.Yes:
                del labels[row]
                self.list1.takeItem(row)
        except AttributeError:
            msg = QMessageBox()
            msg.setText("Please select a label to delete.")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def clear_all(self):
        msg = QMessageBox()
        msg.setText("Are you sure you want to delete all labels?")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        x = msg.exec_()
        if x == QMessageBox.Yes:
            labels.clear()
            self.list1.clear()

    def open(self):
        try:
            global path
            self.list2.clear()
            path = QFileDialog.getExistingDirectory(caption='Select a directory')
            os.chdir(path)
            self.textbox2.setText(f"{path}")
            images = [img for img in os.listdir(path) if os.path.splitext(img)[1] in EXT]
            self.list2.addItems(images)
            labels.sort()
            # with open(os.path.join(path, "labels.txt"), "w") as f:
            #     for label in labels:
            #         f.write(f"{label}\n")
        
        except:
            msg = QMessageBox()
            msg.setText("Please select a directory")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def open_selected(self):
        try:
            global shape, item
            item = self.list2.currentItem().text()
            img_path = os.path.join(item)
            print("Image",image_path)
            img = cv2.imread(img_path)
            

            shape = img.shape

            while True:

                q = path + '\\' + img_path.replace(img_path[len(img_path) - 4:], ".txt")

                if img_path[len(img_path) - 5:] == '.jpeg':
                    q = path + '\\' + img_path.replace(img_path[len(img_path) - 5:], ".txt")
            
                if True == os.path.exists(q):
                    
                    if False ==(os.stat(q).st_size == 0):
                        g=open(q,'r')
                        noBoxes=len(g.readlines())
                        g.close()
                        
                        def putBB(r,img): 
                            
                            #f = f[a]
                            file = open(q, 'r')
                            
                        
                            f = file.readlines()[r].split(',')
                            pts = np.array([[int(f[0]), int(f[1])], [int(f[2]), int(f[3])], 
                            [int(f[4]), int(f[5])], [int(f[6]), int(f[7])], ],np.int32)
            
                            pts = pts.reshape((-1, 1, 2))
                            
                            isClosed = True
                            
                            color = (255, 0, 0)
                            
                            thickness = 2
                            
                            img = cv2.polylines(img, [pts], 
                                                isClosed, color, thickness)
                               
              
                        for r in range(0,noBoxes):
                            putBB(r,img)

                        box("Image", img)
                        
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                    
                    else:
                        box("Image", img)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break 

                else:

                    box("Image", img)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                
                    
                key = cv2.waitKey(1)

                if key==ord('z'):

                    if True == os.path.exists(q):

                        if img_path[len(img_path) - 5:] == '.jpeg':
                            f=open(img_path.replace(img_path[len(img_path) - 5:], ".txt"),'r+')
                            current_position = previous_position = f.tell()
                            while f.readline():
                                previous_position = current_position
                                current_position = f.tell()
                            f.truncate(previous_position)
                            f.close()
                        else:
                            
                            f=open(img_path.replace(img_path[len(img_path) - 4:], ".txt"),'r+')
                            current_position = previous_position = f.tell()
                            while f.readline():
                                previous_position = current_position
                                current_position = f.tell()
                            f.truncate(previous_position)
                            f.close()
                        
                        
                        msg = QMessageBox()
                        msg.setText("Last Label Deleted")
                        msg.setIcon(QMessageBox.Warning)
                        msg.exec_()
                        
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break

                    else:
                        msg = QMessageBox()
                        msg.setText("No label for this image")
                        msg.setIcon(QMessageBox.Warning)
                        msg.exec_()
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                             break
                    break
                    
                if key==ord('k'):


                    if True == os.path.exists(q):

                        if img_path[len(img_path) - 5:] == '.jpeg':
                            f=open(img_path.replace(img_path[len(img_path) - 5:], ".txt"),'r+')
                            f.truncate(0)
                            f.close()
                        else:

                            f=open(img_path.replace(img_path[len(img_path) - 4:], ".txt"),'r+')
                            f.truncate(0)
                            
                        msg = QMessageBox()
                        msg.setText("All Label(s) Deleted")
                        msg.setIcon(QMessageBox.Warning)
                        msg.exec_()
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                                    break


                    else:
                        msg = QMessageBox()
                        msg.setText("No label for this image")
                        msg.setIcon(QMessageBox.Warning)
                        msg.exec_()
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                                break

                    
                    break
            
            cv2.destroyAllWindows()
            

        except AttributeError:
            msg = QMessageBox()
            msg.setText("Please select an Image.")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()


    def open_all(self):
        global shape, item
        # items2 = [str(self.list2.item(i).text()) for i in range(self.list2.count())]
        all_images = [img for img in os.listdir() if os.path.splitext(img)[1] in EXT]
        all_images.sort()
        i=0
        while i < len(all_images):
    
            item = all_images[i]
            img_path=item
            img = cv2.imread(item)
            shape = img.shape
            print("Current Image Name: ",img_path)
            while True:

                
                q = path + '\\' + img_path.replace(img_path[len(img_path) - 4:], ".txt")

                if img_path[len(img_path) - 5:] == '.jpeg':
                    q = path + '\\' + img_path.replace(img_path[len(img_path) - 5:], ".txt")
                

                if True == os.path.exists(q):
                    
                    
                    if False ==(os.stat(q).st_size == 0):
                        g=open(q,'r')
                        noBoxes=len(g.readlines())
                        g.close()
                        
                        def putBB(r,img): 
                            
                            #f = f[a]
                            file = open(q, 'r')
                            
                        
                            f = file.readlines()[r].split(',')
                            pts = np.array([[int(f[0]), int(f[1])], [int(f[2]), int(f[3])], 
                            [int(f[4]), int(f[5])], [int(f[6]), int(f[7])], ],np.int32)
            
                            pts = pts.reshape((-1, 1, 2))
                            
                            isClosed = True
                            
                            color = (255, 0, 0)
                            
                            thickness = 2
                            
                            img = cv2.polylines(img, [pts], 
                                                isClosed, color, thickness)
                               
              
                        for r in range(0,noBoxes):
                            putBB(r,img)
                        
                        box("Image", img)

                        key =cv2.waitKey(1)
                        
                    
                    else:
                        box("Image", img)
                        key =cv2.waitKey(1)
                        

                else:

                    box("Image", img)
                    key =cv2.waitKey(1)

                
                if key & 0xFF == ord('q'):
                    
                    break

                if key == ord('a') and i != 0:
                    i -= 1
                    break

                if key == ord('d'):
                    i += 1
                    break

                if key==ord('k'):

                    
                    if True == os.path.exists(q):
                        if img_path[len(img_path) - 5:] == '.jpeg':
                            f=open(img_path.replace(img_path[len(img_path) - 5:], ".txt"),'r+')
                            f.truncate(0)
                            f.close()
                        else:
                            
                            f=open(img_path.replace(img_path[len(img_path) - 4:], ".txt"),'r+')
                            f.truncate(0)
                            f.close()
                        
                        msg = QMessageBox()
                        msg.setText("All Label(s) Deleted")
                        msg.setIcon(QMessageBox.Warning)
                        msg.exec_()
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                                    break

                        
                    else:
                        msg = QMessageBox()
                        msg.setText("No label for this image")
                        msg.setIcon(QMessageBox.Warning)
                        msg.exec_()
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                                    break
                       
                    
                    break
                if key==ord('z'):
             
                    if True == os.path.exists(q):

                        if img_path[len(img_path) - 5:] == '.jpeg':
                            f=open(img_path.replace(img_path[len(img_path) - 5:], ".txt"),'r+')
                            current_position = previous_position = f.tell()
                            while f.readline():
                                previous_position = current_position
                                current_position = f.tell()
                            f.truncate(previous_position)
                            f.close()
                        else:
            
                            f=open(img_path.replace(img_path[len(img_path) - 4:], ".txt"),'r+')
                            current_position = previous_position = f.tell()
                            while f.readline():
                                previous_position = current_position
                                current_position = f.tell()
                            f.truncate(previous_position)
                            f.close()
                            
                        
                        msg = QMessageBox()
                        msg.setText("Last Label Deleted")
                        msg.setIcon(QMessageBox.Warning)
                        msg.exec_()
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                                    break
                        
                    else:
                        msg = QMessageBox()
                        msg.setText("No label for this image")
                        msg.setIcon(QMessageBox.Warning)
                        msg.exec_()
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                                    break
                    
                      
                    break
           
            if key & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()

    def labels_pop_up(self):
        dlg = Dialog()
        dlg.move(points[-1][0], points[-1][1])
        dlg.listw.addItems(labels)


        # Auto Completer
        completer = QCompleter(labels)
        dlg.line.setCompleter(completer)
        dlg.exec_()


    def start_camera(self):
        cap = cv2.VideoCapture(0)
        cap.set(3, frameWidth)
        cap.set(4, frameHeight)
        while True:
            _, frame = cap.read()
            frame = cv2.flip(frame, 1)
            cv2.imshow("Frame", frame)
            box("Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

    def augmentation(self):
        self.new = Augmentation()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = Window()
    win.show()
    sys.exit(app.exec_())
