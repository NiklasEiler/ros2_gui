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
        self.speicher_button_publisher_  = self.create_publisher(String, '/gui/speichern', 10)
        


    def speichern_publisher_callback_(self):
        self.counter_ = self.counter_ + 1
        msg = String()
        msg.data = "speichern"
        self.speicher_button_publisher_.publish(msg)
        print('##save##')

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
        button1 = QPushButton("speichern", parent=gui)
        button1.move(60, 10)
        button1.clicked.connect(ros_node.speichern_publisher_callback_)

        gui.show()
        print("HMI preparation complete")
        #rclpy.spin(ros_node)
        sys.exit(app.exec())


    finally:
        ros_node.get_logger().info("Shutting down")
        ros_node.destroy_node()
        executor.shutdown()
    
if __name__ == '__main__':
    main()