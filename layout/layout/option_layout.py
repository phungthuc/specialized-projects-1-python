import sys
import cv2 as cv
from PySide6 import QtGui
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class option(QWidget):
    def __init__(self, parent):
        super(option, self).__init__(parent)
        self.layout = QHBoxLayout(self)
        self.widget_general = QWidget()
        self.widget_general.layout = QGridLayout()
        self.widget_general.setLayout(self.widget_general.layout)
        self.widget_general.setObjectName("frame_general")

        self.lb_brightness = QLabel("Brightness")
        self.sld_brightness = QSlider(Qt.Horizontal, self)
        self.sld_brightness.setRange(-150, 150)
        self.sld_brightness.setValue(0)
        self.sld_brightness.setFocusPolicy(Qt.NoFocus)
        self.sld_brightness.valueChanged.connect(parent.on_brightness_change)
        self.sld_brightness.sliderReleased.connect(parent.on_brightness_released)

        self.widget_general.layout.addWidget(self.lb_brightness, 0, 0)
        self.widget_general.layout.addWidget(self.sld_brightness, 0, 1)

        self.lb_constrast = QLabel("Constrast")
        self.sld_constrast = QSlider(Qt.Horizontal, self)
        self.sld_constrast.setRange(0, 40)
        self.sld_constrast.setValue(10)
        self.sld_constrast.setFocusPolicy(Qt.NoFocus)
        self.sld_constrast.valueChanged.connect(parent.on_constrast_change)
        self.sld_constrast.sliderReleased.connect(parent.on_constrast_released)

        self.widget_general.layout.addWidget(self.lb_constrast, 1, 0)
        self.widget_general.layout.addWidget(self.sld_constrast, 1, 1)

        self.lb_blur = QLabel("Blur")
        self.sld_blur = QSlider(Qt.Horizontal, self)
        self.sld_blur.setRange(1, 50)
        self.sld_blur.setFocusPolicy(Qt.NoFocus)
        self.sld_blur.valueChanged.connect(parent.on_blur_change)
        self.sld_blur.sliderReleased.connect(parent.on_blur_released)

        self.widget_general.layout.addWidget(self.lb_blur, 2, 0)
        self.widget_general.layout.addWidget(self.sld_blur, 2, 1)

        self.lb_hue = QLabel("Hue")
        self.sld_hue = QSlider(Qt.Horizontal, self)
        self.sld_hue.setRange(-150, 150)
        self.sld_hue.setValue(0)
        self.sld_hue.setFocusPolicy(Qt.NoFocus)
        self.sld_hue.valueChanged.connect(parent.on_hue_change)
        self.sld_hue.sliderReleased.connect(parent.on_hue_released)

        self.widget_general.layout.addWidget(self.lb_hue, 3, 0)
        self.widget_general.layout.addWidget(self.sld_hue, 3, 1)

        self.lb_saturation = QLabel("Saturation")
        self.sld_saturation = QSlider(Qt.Horizontal, self)
        self.sld_saturation.setRange(-150, 150)
        self.sld_saturation.setValue(0)
        self.sld_saturation.setFocusPolicy(Qt.NoFocus)
        self.sld_saturation.valueChanged.connect(parent.on_saturation_change)
        self.sld_saturation.sliderReleased.connect(parent.on_saturation_released)

        self.widget_general.layout.addWidget(self.lb_saturation, 4, 0)
        self.widget_general.layout.addWidget(self.sld_saturation, 4, 1)

        self.widget_canny = QWidget()
        self.widget_canny.layout = QVBoxLayout()
        self.widget_canny.setLayout(self.widget_canny.layout)
        self.widget_canny.setObjectName("frame_general")

        self.canny_detect = QCheckBox("Canny Detection", self)
        self.canny_detect.stateChanged.connect(parent.on_edges_detetion)
        self.widget_canny.layout.addWidget(self.canny_detect)

        self.canny_min_widget = QWidget()
        self.canny_min_widget.layout = QHBoxLayout()
        self.canny_min_widget.setLayout(self.canny_min_widget.layout)
        self.widget_canny.layout.addWidget(self.canny_min_widget)

        self.lb_canny_min = QLabel("Canny min")
        self.sld_canny_min = QSlider(Qt.Horizontal, self)
        self.sld_canny_min.valueChanged.connect(parent.on_canny_min_change)
        self.sld_canny_min.setRange(0, 255)
        self.sld_canny_min.setValue(100)
        self.canny_min_widget.layout.addWidget(self.lb_canny_min)
        self.canny_min_widget.layout.addWidget(self.sld_canny_min)

        self.canny_max_widget = QWidget()
        self.canny_max_widget.layout = QHBoxLayout()
        self.canny_max_widget.setLayout(self.canny_max_widget.layout)
        self.widget_canny.layout.addWidget(self.canny_max_widget)

        self.lb_canny_max = QLabel("Canny max")
        self.sld_canny_max = QSlider(Qt.Horizontal, self)
        self.sld_canny_max.valueChanged.connect(parent.on_canny_max_change)
        self.sld_canny_max.setRange(0, 255)
        self.sld_canny_max.setValue(255)
        self.canny_max_widget.layout.addWidget(self.lb_canny_max)
        self.canny_max_widget.layout.addWidget(self.sld_canny_max)

        self.change_background_widget = QWidget()
        self.change_background_widget.layout = QHBoxLayout()
        self.change_background_widget.setLayout(self.change_background_widget.layout)
        self.widget_canny.layout.addWidget(self.change_background_widget)

        self.btn_change_background = QPushButton()
        self.btn_change_background.setIcon(QIcon('../image/background_16.png'))
        self.btn_change_background.setFixedSize(32, 32)
        self.btn_change_background.clicked.connect(parent.change_background)
        self.change_background_widget.layout.addWidget(self.btn_change_background)

        self.lb_change_background = QLabel("Change background")
        self.change_background_widget.layout.addWidget(self.lb_change_background)

        self.widget_face_recognition = QWidget()
        self.widget_face_recognition.layout = QVBoxLayout()
        self.widget_face_recognition.setLayout(self.widget_face_recognition.layout)
        self.widget_face_recognition.setObjectName("frame_general")

        self.lb_face_recognition = QLabel("Face recognition")
        self.widget_face_recognition.layout.addWidget(self.lb_face_recognition)

        self.widget_choose_image = QWidget()
        self.widget_choose_image.layout = QHBoxLayout()
        self.widget_choose_image.setLayout(self.widget_choose_image.layout)
        self.widget_face_recognition.layout.addWidget(self.widget_choose_image)

        self.btn_choose_file = QPushButton("Choose file")
        self.widget_choose_image.layout.addWidget(self.btn_choose_file)
        self.btn_choose_file.setObjectName("pushbutton")
        self.btn_choose_file.clicked.connect(parent.openfile_to_detect)

        self.btn_open_camera = QPushButton("Open camera")
        self.btn_open_camera.clicked.connect(parent.open_camera)
        self.widget_choose_image.layout.addWidget(self.btn_open_camera)
        self.btn_open_camera.setObjectName("pushbutton")

        self.lb_insert_data = QLabel("Insert data")
        self.widget_face_recognition.layout.addWidget(self.lb_insert_data)

        self.widget_insert_data = QWidget()
        self.widget_insert_data.layout = QHBoxLayout()
        self.widget_insert_data.setLayout(self.widget_insert_data.layout)
        self.widget_face_recognition.layout.addWidget(self.widget_insert_data)

        self.option_insert_data = QComboBox()
        self.option_insert_data.addItem("From your camera")
        self.widget_insert_data.layout.addWidget(self.option_insert_data)
        self.option_insert_data.currentIndexChanged.connect(parent.choose_way_insert_data)

        self.btn_insert_data = QPushButton("Insert")
        self.widget_insert_data.layout.addWidget(self.btn_insert_data)
        self.btn_insert_data.setObjectName("pushbutton")
        self.btn_insert_data.clicked.connect(parent.insert_data)

        self.widget_other = QWidget()
        self.widget_other.layout = QVBoxLayout()
        self.widget_other.setLayout(self.widget_other.layout)

        self.btn_cropImage = QPushButton("Crop image")
        self.btn_cropImage.setIcon(QPixmap("../image/crop.png"))
        self.btn_cropImage.setMinimumSize(100, 30)
        self.btn_reset = QPushButton("Reset")
        self.btn_reset.setIcon(QPixmap("../image/reset.png"))
        self.btn_reset.setMinimumSize(100, 30)
        self.btn_reset.pressed.connect(parent.on_reset_pressed)
        self.widget_other.layout.addWidget(self.btn_cropImage)
        self.widget_other.layout.addWidget(self.btn_reset)

        self.layout.addWidget(self.widget_general)
        self.layout.addWidget(self.widget_canny)
        self.layout.addWidget(self.widget_face_recognition)
        self.layout.addWidget(self.widget_other)
        self.setLayout(self.layout)
        sshFile = "qss/option_layout.qss"
        with open(sshFile, "r") as fh:
            self.setStyleSheet(fh.read())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = option()
    window.show()
    sys.exit(app.exec_())