# --------------------------------------------------------------------------------
#   File        rc_servo_motor_control.py
#
#   Version     v0.1  2025.11.05  Tony Kwon
#                   Initial revision
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
#   Import
# --------------------------------------------------------------------------------
import sys
from PySide6.QtWidgets import QMainWindow

from .rc_servo_motor_control_model import RcServoMotor, RcServoMotorControlModel
from .rc_servo_motor_control_view import RcServoMotorControlView

# --------------------------------------------------------------------------------
#   Class - RcServoMotorControl
# --------------------------------------------------------------------------------
class RcServoMotorControl(QMainWindow):
    def __init__(self, motor_cnt, motor_ticks):     
        super().__init__()
        
        # Set model
        self.model = RcServoMotorControlModel()
        for i in range(motor_cnt):
            self.model.add_motor(RcServoMotor(motor_ticks[i]))

        # Set view
        self.view = RcServoMotorControlView(self.model)        
        
        # Set window
        self.setWindowTitle('RC Servo Motor Control')
        
        # Set main widget
        self.setCentralWidget(self.view)  
        
    def get_view(self):
        return self.view

        
    