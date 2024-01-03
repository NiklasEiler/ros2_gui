import sys
import rclpy
import time
import sys
from threading import Thread
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from std_msgs.msg import String
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QPushButton


class GuiNode(Node):
    def __init__(self):
        super().__init__("simple_gui_node")
        self.counter_    = 0
        self.button1_publisher_  = self.create_publisher(String, '/gui/button_1', 10)
        self.button2_publisher_  = self.create_publisher(String, '/gui/button_2', 10)


    def button_1_publisher_callback_(self):
        self.counter_ = self.counter_ + 1
        msg = String()
        msg.data = "Button 1 pressed"
        self.button1_publisher_.publish(msg)

    def button_2_publisher_callback_(self):
        self.counter_ = self.counter_ + 1
        msg = String()
        msg.data = "Button 2 pressed"
        self.button2_publisher_.publish(msg)

    def button_3_publisher_callback_(self):
        self.counter_ = self.counter_ + 1
        msg = String()
        msg.data = "Button 3 pressed"
        self.button2_publisher_.publish(msg)

    def subscriber_callback_(self, msg):
        self.get_logger().info("Button clicked, " + msg.data)


    
    


    
    


def main(args=None):
    rclpy.init(args=args)
    ros_node=GuiNode()
    app = QApplication(sys.argv)
    executor = MultiThreadedExecutor()        
    print("HMI preparation start")
    try:
        gui = QMainWindow()

        gui.setWindowTitle("Test ROS2 GUI")
        gui.setGeometry(100, 100, 240, 240)
        #gui.move(100, 100)

        value_label = 'Value'
        button1 = QPushButton("Pointcloud", parent=gui)
        button1.move(60, 10)
        button1.clicked.connect(ros_node.button_1_publisher_callback_)

        button2 = QPushButton("Rechtes Bild", parent=gui)
        button2.move(60, 60)
        button2.clicked.connect(ros_node.button_2_publisher_callback_)

        button2 = QPushButton("Linkes Bild", parent=gui)
        button2.move(60, 110)
        button2.clicked.connect(ros_node.button_3_publisher_callback_)

        gui.show()
        print("HMI preparation complete")
        #rclpy.spin(ros_node_point)
        sys.exit(app.exec())


    finally:
        ros_node.get_logger().info("Shutting down")
        ros_node.destroy_node()
        executor.shutdown()
    
if __name__ == '__main__':
    main()