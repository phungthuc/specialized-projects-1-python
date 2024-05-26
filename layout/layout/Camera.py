import os
import sys
from PySide6 import QtGui
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import cv2 as cv
import numpy as np
import face_recognition
import time
import threading

class Camera(QWidget):
    def __init__(self):
        super(Camera, self).__init__()
        self.time_start = 5
        self.path = "../train_data"
        self.listPerson = os.listdir(self.path)
        self.setWindowTitle("Camera")
        self.resize(860, 680)
        self.setWindowIcon(QtGui.QIcon("../image/python_icon.png"))
        self.camera = cv.VideoCapture(0)
        self.layout = QHBoxLayout()

        self.widget_camera = QWidget()
        self.widget_camera.layout = QVBoxLayout()
        self.widget_camera.setLayout(self.widget_camera.layout)
        self.widget_camera.layout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.widget_camera)

        self.lb_camera = QLabel()
        self.widget_camera.layout.addWidget(self.lb_camera)

        self.btn_start = QPushButton("Start")
        self.btn_start.setObjectName("btn_start")
        self.btn_start.clicked.connect(self.start_to_detect)
        self.widget_camera.layout.addWidget(self.btn_start, alignment=Qt.AlignCenter)

        self.widget_hint = QWidget()
        self.widget_hint.layout = QVBoxLayout()
        self.widget_hint.setLayout(self.widget_hint.layout)
        self.widget_hint.setObjectName("object")
        self.layout.addWidget(self.widget_hint)

        self.lb_title = QLabel("Please put your face to the camera")
        self.lb_title.setObjectName("title")
        self.widget_hint.layout.addWidget(self.lb_title)

        self.lb_timer = QLabel("5")
        self.widget_hint.layout.addWidget(self.lb_timer, alignment=Qt.AlignCenter)
        self.lb_timer.setObjectName("lb_timer")

        self.btn_cancel = QPushButton("Cancel")
        self.widget_hint.layout.addWidget(self.btn_cancel)
        self.btn_cancel.setObjectName("btn_cancel")
        self.btn_cancel.clicked.connect(self.turn_off)

        self.setLayout(self.layout)

        sshFile = "qss/camera.qss"
        with open(sshFile, "r") as fh:
            self.setStyleSheet(fh.read())

        self.timer = QTimer()
        self.timer.setInterval(1)
        self.timer.timeout.connect(self.draw_camera)


    def start(self):
        self.timer.start()
        self.show()

    def show_warning(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowIcon(QtGui.QIcon("../image/error.png"))
        x = msg.exec_()

    def stop(self):
        self.timer.stop()
        self.camera.release()

    def draw_camera(self):
        b, frame = self.camera.read()
        image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        FlippedImage = cv.flip(image, 1)
        converttoQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0],
                                   QImage.Format_RGB888)
        pix = converttoQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
        self.lb_camera.setPixmap(QPixmap.fromImage(pix))

    def closeEvent(self, event):
        self.stop()
        return QWidget.closeEvent(self, event)

    def turn_off(self):
        self.stop()
        self.close()

    def start_to_detect(self):
        self.t = threading.Thread(target=self.thread_countdown)
        self.t.start()

    def thread_countdown(self):
        self.time_start = 5
        while (self.time_start >= 0):
            self.btn_start.hide()
            self.lb_timer.setText(str(self.time_start))
            self.lb_timer.repaint()
            time.sleep(1)
            self.time_start = self.time_start - 1
        self.btn_start.show()
        self.face_re()
        return;

    def check_face_in_picture(self, img):
        if (len(face_recognition.face_locations(img)) != 0):
            return True
        else:
            return False

    # caculation distance for image
    def calculation_distance(self, image_path, image_face_encoding):
        image = face_recognition.load_image_file(image_path)
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        face_encoding = face_recognition.face_encodings(image)[0]
        distance = face_recognition.face_distance([image_face_encoding], face_encoding)
        return distance

    # caculation average of each classname
    def average_distance(self, classname, image_face_encoding):
        folder_path = f'{self.path}/{classname}'
        folder = os.listdir(folder_path)
        count_image = len(folder)
        sum_distance = 0
        for img in folder:
            sum_distance += self.calculation_distance(f'{folder_path}/{img}', image_face_encoding)
        return sum_distance / count_image

    def face_recognition(self, image):
        temp_image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        listDistance = []
        name = "Unknown"
        y1, x2, y2, x1 = face_recognition.face_locations(temp_image)[0]
        image_encoding = face_recognition.face_encodings(temp_image)[0]
        for person in self.listPerson:
            distance = self.average_distance(person, image_encoding)
            listDistance.append(distance[0])
        minIndex = np.argmin(listDistance)
        if listDistance[minIndex] < 0.6:
            name = self.listPerson[minIndex]
        cv.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv.rectangle(image, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv.FILLED)
        cv.putText(image, name, (x1 + 6, y2 - 6), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        return image


    def face_re(self):
        b, frame = self.camera.read()
        image2 = cv.resize(frame, (640, 480), None, 0.25, 0.25)
        if (self.check_face_in_picture(image2)):
            image_show = self.face_recognition(image2)
            cv.imshow("User", image_show)
            cv.waitKey()
        else:
            # self.show_warning("Error", "Can not detect your face !! Try again")
            print("Can not detect your face")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Camera()
    window.start()
    sys.exit(app.exec_())