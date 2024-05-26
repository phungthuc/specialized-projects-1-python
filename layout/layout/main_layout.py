import os, sys, stat
import shutil
import cv2
import face_recognition

import numpy as np
from PySide6 import QtGui
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from option_layout import option
from Camera import Camera


class main_layout(QWidget):
    def __init__(self):
        super().__init__()
        self.last_filter = None
        self.last_img = None
        self.last_temp_img = None
        self.x_start = 0
        self.x_end = 0
        self.y_start = 0
        self.x_end = 0
        self.cropping = False
        self.processed_image = None
        self.original_image = None
        self.pix = None
        self.canny = False
        self.canny_min = 100
        self.canny_max = 255
        self.image_canny = None
        self.mask_canny = None
        self.kernel = np.ones((7, 7), np.uint8)
        self.path = "../train_data"
        self.listPerson = os.listdir(self.path)
        self.popups = []
        self.way_insert_data = 0
        self.setWindowTitle("Image Processing")
        self.resize(860, 680)
        self.setWindowIcon(QtGui.QIcon("../image/python_icon.png"))
        self.layout = QVBoxLayout()
        self.top_frame = QFrame(self)
        self.top_frame.setFrameShape(QFrame.StyledPanel)
        self.top_frame.setObjectName("frame1")

        # button open file
        self.btn_openfile = QPushButton("Open file")
        self.btn_openfile.setIcon(QIcon("../image/openfile.png"))
        self.btn_openfile.setObjectName("btn_openfile")
        self.btn_openfile.clicked.connect(self.openfile)

        # button save image
        self.btn_saveimage = QPushButton("Save image")
        self.btn_saveimage.setIcon(QIcon("../image/savefile.png"))
        self.btn_saveimage.setObjectName("btn_savefile")
        self.btn_saveimage.pressed.connect(self.on_save_pressed)

        # add widget to top frame
        self.top_frame.layout =QHBoxLayout()
        self.top_frame.layout.addWidget(self.btn_openfile)
        self.top_frame.layout.addWidget(self.btn_saveimage)
        self.top_frame.setLayout(self.top_frame.layout)

        # create main frame to show image
        self.main_frame = QFrame(self)
        self.main_frame.setContentsMargins(0,0,0,0)
        self.main_frame.setFrameShape(QFrame.StyledPanel)
        self.main_frame.setObjectName("frame2")

        # Label to show original image
        self.ori_image = QLabel()
        self.ori_image.setText("Original Image")
        self.ori_image.setAlignment(Qt.AlignCenter)
        self.ori_image.setObjectName("ori_image")
        # self.ori_image.setScaledContents(True)

        # Label to show handle image
        self.lb_process_image = QLabel()
        self.lb_process_image.setText("Process Image")
        self.lb_process_image.setAlignment(Qt.AlignCenter)
        self.lb_process_image.setObjectName("process_image")
        self.lb_process_image.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        # self.lb_process_image.setScaledContents(True)

        self.main_frame.layout = QHBoxLayout()
        self.main_frame.layout.addWidget(self.ori_image)
        self.main_frame.layout.addWidget(self.lb_process_image)
        self.main_frame.setLayout(self.main_frame.layout)

        self.option_frame = QFrame(self)
        self.option_frame.setFrameShape(QFrame.StyledPanel)
        self.option_frame.setObjectName("frame3")
        self.option_frame.layout = QHBoxLayout()
        self.option_frame.setLayout(self.option_frame.layout)
        self.option_layout = option(self)
        self.option_layout.btn_cropImage.clicked.connect(self.crop_image)
        self.option_frame.layout.addWidget(self.option_layout)

        self.layout.addWidget(self.top_frame)
        self.layout.addWidget(self.main_frame)
        self.layout.addWidget(self.option_frame)
        self.setLayout(self.layout)
        # add file qss
        sshFile = "qss/design.qss"
        with open(sshFile, "r") as fh:
            self.setStyleSheet(fh.read())

    def show_warning(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowIcon(QtGui.QIcon("../image/error.png"))
        x = msg.exec_()

    def openfile(self):
        path_image = QFileDialog.getOpenFileName(self, "Image file")
        path = path_image[0]
        image = QImage(path)
        if path:
            if path.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                self.processed_image = cv2.imread(path)
                self.original_image = cv2.imread(path)
                self.ori_image.setPixmap(QPixmap(path))
                self.pix = QPixmap.fromImage(image)
                self.ori_image.setPixmap(self.pix.scaled(self.ori_image.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.lb_process_image.setPixmap(self.pix.scaled(self.lb_process_image.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.on_reset_pressed()
            else:
                self.show_warning("Error", "Your file is not image")
    def on_save_pressed(self):
        if(self.processed_image is not None):
            path_image = QFileDialog.getSaveFileUrl(self, "Save as")
            if(path_image[0] is not None):
                path = path_image[0]
                filename = os.path.basename(path.toString())
                dir = path.toString()[:len(path.toString()) - len(filename) - 1].replace("file:///", "")
                path_to_save = f'{dir}/{filename}.jpg'
                if self.canny == True:
                    cv2.imwrite(path_to_save, self.image_canny)
                else:
                    cv2.imwrite(path_to_save, self.last_img)

    # check image exits
    def exist_image(self):
        if self.ori_image.pixmap():
            return True
        else:
            return False
    # convert opencv image to Qpixmap
    @staticmethod
    def convert_cvImg_2_qImg(cvImg, c_width=0, c_height=0):
        if len(cvImg.shape) < 3:
            height, width = cvImg.shape
        else:
            height, width, channel = cvImg.shape
        bytesPerLine = 3 * width
        qImg = QtGui.QImage(cvImg.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888).rgbSwapped()
        qPixmap = QPixmap(qImg)
        if c_width != 0:
            qPixmap = qPixmap.scaledToWidth(c_width)
        if c_height != 0:
            qPixmap = qPixmap.scaledToHeight(c_height)
        return qPixmap

    #set image for label process
    def set_imageprocess(self, img):
        show_image = self.convert_cvImg_2_qImg(img)
        self.lb_process_image.setPixmap(
            show_image.scaled(self.lb_process_image.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
    # crop image
    def on_reset_pressed(self):
        self.option_layout.sld_blur.setValue(1)
        self.option_layout.sld_hue.setValue(0)
        self.option_layout.sld_brightness.setValue(0)
        self.option_layout.sld_saturation.setValue(0)
        self.option_layout.sld_constrast.setValue(10)
        self.option_layout.canny_detect.setChecked(False)
        self.processed_image = self.original_image
        self.last_img = self.original_image
        self.last_temp_img = self.original_image
        self.set_imageprocess(self.original_image)

    def crop_image(self):
        if self.exist_image():
            cv2.namedWindow("image")
            cv2.imshow("image", self.last_img)
            cv2.setMouseCallback("image", self.mouse_crop)
            while True:
                i = self.last_img.copy()
                if self.cropping:
                    cv2.rectangle(i, (self.x_start, self.y_start), (self.x_end, self.y_end), (255, 0, 0), 2)
                    cv2.imshow("image", i)
                cv2.waitKey(1)
        else:
            self.show_warning("Error", "Photo does not exist")

    def mouse_crop(self,event, x, y, flags, param):
        if self.exist_image():
            i = self.last_img.copy()
            if event == cv2.EVENT_LBUTTONDOWN:
                self.x_start, self.y_start, self.x_end, self.y_end = x, y, x, y
                self.cropping = True
            elif event == cv2.EVENT_MOUSEMOVE:
                if self.cropping == True:
                    self.x_end, self.y_end = x, y
            elif event == cv2.EVENT_LBUTTONUP:
                # record the ending (x, y) coordinates
                self.x_end, self.y_end = x, y
                self.cropping = False  # cropping is finished
                refPoint = [(self.x_start, self.y_start), (self.x_end, self.y_end)]
                # print(str(self.x_start) + "-" + str(self.x_end) + "-" + str(self.y_start) + "-" + str(self.y_end))
                cv2.rectangle(i, (self.x_start, self.y_start), (self.x_end, self.y_end), (255, 0, 0), 1)
                new_img = np.array(i[self.y_start-1:self.y_end-1, self.x_start-1:self.x_end-1])
                self.processed_image = new_img
                self.last_img = new_img
                self.last_temp_img = new_img
                self.last_filter = "cropping"
                self.set_imageprocess(new_img)
                cv2.destroyAllWindows()
        else:
            self.show_warning("Error", "Photo does not exist")

    # tranform logarit
    @staticmethod
    def tranform_logarit(img, c):
        return float(c) * cv2.log(1.0 + img)

    def tranform_logarit(img, c):
        return float(c) * cv2.log(1.0 + img)

    def on_constrast_released(self):
        self.last_filter = "constrast"
        self.last_img = self.last_temp_img
        # self.processed_image = self.last_img

    def on_blur_released(self):
        self.last_filter = "blur"
        self.last_img = self.last_temp_img
        # self.processed_image = self.last_img

    def on_brightness_released(self):
        self.last_filter = "brightness"
        self.last_img = self.last_temp_img
        # self.processed_image = self.last_img

    def on_hue_released(self):
        self.last_filter = "hue"
        self.last_img = self.last_temp_img
        # self.processed_image = self.last_img

    def on_saturation_released(self):
        self.last_filter = "saturation"
        self.last_img = self.last_temp_img
        # self.processed_image = self.last_img

    def transform_brightness(self, img, value=30):
        if(self.last_filter !="brightness" and self.last_img is not None):
            img = self.last_img
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        if value >= 0:
            lim = 255 - value
            v[v > lim] = 255
            v[v <= lim] += value
        else:
            value = int(-value)
            lim = 0 + value
            v[v < lim] = 0
            v[v >= lim] -= value
        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        self.last_temp_img = img
        return img

    def transform_hue(self, img, value=1):
        if (self.last_filter != "hue" and self.last_img is not None):
            img = self.last_img
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        if value >= 0:
            lim = 255 - value
            h[h > lim] = 255
            h[h <= lim] += value
        else:
            value = int(-value)
            lim = 0 + value
            h[h < lim] = 0
            h[h >= lim] -= value

        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        self.last_temp_img = img
        return img

    def transform_saturation(self, img, value=30):
        if (self.last_filter != "saturation" and self.last_img is not None):
            img = self.last_img
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        if value >= 0:
            lim = 255 - value
            s[s > lim] = 255
            s[s <= lim] += value
        else:
            value = int(-value)
            lim = 0 + value
            s[s < lim] = 0
            s[s >= lim] -= value

        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        self.last_temp_img = img
        return img

    def tranform_constrast(self, img, gamma=0.5): # using transform gamma
        if (self.last_filter != "constrast" and self.last_img is not None):
            img = self.last_img
        image = np.power(img, gamma)
        max_val = np.max(image.ravel()) # find max value in image
        image = image / max_val * 255
        image = image.astype(np.uint8)
        self.last_temp_img = image
        return image

    # insert image to label
    def insert_image(self, img2):
        norm_img = np.zeros((800, 800))
        final_img = cv2.normalize(img2, norm_img, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)  # cv2.CV_8u 0-255
        process_image = self.convert_cvImg_2_qImg(final_img)
        self.lb_process.setPixmap(process_image.scaled(self.lb_process.size(),Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def on_brightness_change(self, value):
        if self.exist_image():
            self.brightness = value
            img2 = self.transform_brightness(self.processed_image, value)
            self.set_imageprocess(img2)

    def on_hue_change(self, value):
        if self.exist_image():
            img2 = self.transform_hue(self.processed_image, value)
            self.set_imageprocess(img2)

    def on_saturation_change(self, value):
        if self.exist_image():
            img2 = self.transform_saturation(self.processed_image, value)
            self.set_imageprocess(img2)

    def on_constrast_change(self, value):
        if self.exist_image():
            img2 = self.tranform_constrast(self.processed_image, gamma=(41-value)/10)
            self.set_imageprocess(img2)

    def on_blur_change(self, value):
        if self.exist_image():
            img2 = self.transform_blur(self.processed_image, value)
            self.set_imageprocess(img2)

    def generateMatrix(self, size):
        k = np.ones((size, size), np.float32) / (size ** 2)
        return k

    def transform_blur(self, image, level):
        if (self.last_filter != "blur" and self.last_img is not None):
            image = self.last_img
        image = np.array(image)
        h, w, d = image.shape
        temp = np.zeros((h, w, d))
        matrix = self.generateMatrix(level)
        img = cv2.filter2D(image, -1 , matrix)
        self.last_temp_img = img
        return img

    def on_edges_detetion(self, state):
        if self.exist_image():
            if self.last_img is None:
                image = self.original_image
            else:
                image = self.last_img
            if state == Qt.Checked:
                self.canny_min = 100
                self.canny_max = 255
                img_show = self.canny_detection()
                self.set_imageprocess(img_show)
                self.option_layout.sld_canny_min.setValue(100)
                self.option_layout.sld_canny_max.setValue(255)
                self.canny = True
            else:
                self.set_imageprocess(image)
                self.canny = False

    def canny_detection(self):
        image = self.original_image.copy()
        img_gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.Canny(img_gray, self.canny_min, self.canny_max)
        closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, self.kernel)
        contours = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]
        mask = np.zeros_like(image)
        self.mask_canny = mask
        cv2.drawContours(mask, contours, -1, (255, 255, 255), -1)
        image[mask == 0] = 0
        self.image_canny = image
        return image

    def on_canny_min_change(self, value):
       if self.original_image is not None and self.canny == True:
           self.canny_min = value
           img_show = self.canny_detection()
           self.set_imageprocess(img_show)

    def on_canny_max_change(self, value):
        if self.original_image is not None and self.canny == True:
            self.canny_max = value
            img_show = self.canny_detection()
            self.set_imageprocess(img_show)

    def change_background(self):
        if self.canny == True:
            path_image = QFileDialog.getOpenFileName(self, "Image file")
            path_background = path_image[0]
            if self.exist_image():
                if path_background.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                    background = cv2.imread(path_background)
                    width = self.original_image.shape[1]
                    height = self.original_image.shape[0]
                    dim = (width, height)
                    background_resize = cv2.resize(background, dim, interpolation=cv2.INTER_AREA)
                    image_change_background = np.where(self.mask_canny > 0, self.original_image, background_resize)
                    self.image_canny = image_change_background
                    self.set_imageprocess(image_change_background)
                else:
                    self.show_warning("Error", "Your file is not image")
        else:
            self.show_warning("Error", "You haven't used canny detection")

    # caculation distance for image
    def calculation_distance(self, image_path, image_face_encoding):
        image = face_recognition.load_image_file(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        face_encoding = face_recognition.face_encodings(image)[0]
        distance = face_recognition.face_distance([image_face_encoding], face_encoding)
        print(distance)
        return distance

    # caculation average of each classname
    def average_distance(self, classname, image_face_encoding):
        folder_path = f'{self.path}/{classname}'
        folder = os.listdir(folder_path)
        print(folder)
        count_image = len(folder)
        sum_distance = 0
        for img in folder:
            sum_distance += self.calculation_distance(f'{folder_path}/{img}', image_face_encoding)
        return sum_distance / count_image

    # check face in the picture
    def check_face_in_picture(self, img):
        if (len(face_recognition.face_locations(img)) != 0):
            return True
        else:
            return False

    #open file to detect
    def openfile_to_detect(self):
        path_image = QFileDialog.getOpenFileName(self, "Image file")
        path = path_image[0]
        if path:
            if path.lower().endswith(('.png', '.jpg', '.jpeg')):
                listDistance = []
                name = "Unknown"
                imageDetect =face_recognition.load_image_file(path)
                imageDetect = cv2.cvtColor(imageDetect, cv2.COLOR_BGR2RGB)
                if (self.check_face_in_picture(imageDetect)):
                    y1, x2, y2, x1 = face_recognition.face_locations(imageDetect)[0]
                    image_encoding = face_recognition.face_encodings(imageDetect)[0]
                    for person in self.listPerson:
                        distance = self.average_distance(person, image_encoding)
                        listDistance.append(distance[0])
                    minIndex = np.argmin(listDistance)
                    if listDistance[minIndex] < 0.6:
                        name = self.listPerson[minIndex]
                    cv2.rectangle(imageDetect, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(imageDetect, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(imageDetect, name, (x1+6, y2-6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    cv2.imshow("Face to detect", imageDetect)
                else:
                    self.show_warning("Error", "Can not detect face in this picture")
            else:
                self.show_warning("Error", "Can not read this file")

    def open_camera(self):
        camera = Camera()
        camera.start()
        self.popups.append(camera)

    def choose_way_insert_data(self, value):
        self.way_insert_data = value

    def isNotBlank(self, string):
        if string and string.strip():
            return True
        return False

    def check_exist_folder(self, folder_name):
        if os.path.exists(folder_name):
            return False
        return True

    def insert_data(self):
        if self.way_insert_data == 0:
            name, done = QInputDialog.getText(self, "Name", "Enter your name: ")
            if done:
                if (self.isNotBlank(name)):
                    path = f'{self.path}/{name}'
                    if self.check_exist_folder(path):
                        os.mkdir(path)
                        self.camera_insert_data(path, name)
                    else:
                        self.show_warning("Error", "This name is already exist")
                else:
                    self.show_warning("Error", "Name is required")
        else:
            print("open folder")



    def camera_insert_data(self, path, name):
        video = cv2.VideoCapture(0)
        count_image = 0
        delay_frame = 0
        while(True):
            ret, frame = video.read()
            image = cv2.resize(frame, (640, 480), None, 0.25, 0.25)
            if (self.check_face_in_picture(image)):
                if count_image < 2:
                    cv2.imwrite(os.path.join(path, name+str(count_image)+".jpg"), image)
                    count_image = count_image + 1
            else:
                cv2.putText(frame, "Can not detect face!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if delay_frame == 30:
                break
            delay_frame = delay_frame + 1
            cv2.imshow('Camera', frame)
        if count_image >= 2:
            mbox = QMessageBox.information(self, "Message", "Successfully")
        else:
            print("Can not detect your face. Try again !!")
            path_to_delete = os.path.join(self.path, name)
            shutil.rmtree(path_to_delete)
        video.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = main_layout()
    window.show()
    sys.exit(app.exec())

