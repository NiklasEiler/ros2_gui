#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTabWidget, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import rclpy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class MyGuiNode(QWidget):

    def __init__(self):
        super().__init__()

        # ROS setup
        self.node = rclpy.create_node('my_gui_node')
        self.image_sub = self.node.create_subscription(Image, '/image_topic', self.image_callback, 10)
        self.bridge = CvBridge()

        # GUI setup
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('ROS 2 GUI Node')

        layout = QVBoxLayout(self)

        # Buttons
        button1 = QPushButton('Button 1', self)
        button2 = QPushButton('Button 2', self)

        layout.addWidget(button1)
        layout.addWidget(button2)

        # Tabs
        tabs = QTabWidget()

        tab1 = QWidget()
        tab2 = QWidget()

        tabs.addTab(tab1, 'Tab 1')
        tabs.addTab(tab2, 'Tab 2')

        # Labels for displaying values
        label_tab1 = QLabel('Value in Tab 1', self)
        label_tab2 = QLabel('Value in Tab 2', self)

        tab1_layout = QVBoxLayout(tab1)
        tab1_layout.addWidget(label_tab1)

        tab2_layout = QVBoxLayout(tab2)
        tab2_layout.addWidget(label_tab2)

        # Image display
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)  # Center-align the image
        layout.addWidget(tabs)
        layout.addWidget(self.image_label)

        self.setLayout(layout)
        self.show()

    def image_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        height, width, channel = cv_image.shape
        bytes_per_line = 3 * width
        q_image = QImage(cv_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(q_image))

def main(args=None):
    rclpy.init(args=args)

    app = QApplication(sys.argv)
    gui_node = MyGuiNode()

    try:
        sys.exit(app.exec_())
    finally:
        gui_node.node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
