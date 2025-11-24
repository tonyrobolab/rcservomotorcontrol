# --------------------------------------------------------------------------------
#   File        rc_servo_motor_control_app.py
#
#   Version     v0.1  2025.11.05  Tony Kwon
#                   Initial revision
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
#   Import
# --------------------------------------------------------------------------------
import sys
from PySide6.QtWidgets import (
    QApplication,
)
from rc_servo_motor_control.rc_servo_motor_control import RcServoMotorControl    

# --------------------------------------------------------------------------------
#   Run
# --------------------------------------------------------------------------------
if __name__ == '__main__':
    # Set configuration data
    motor_cnt = 3
    motor_ticks = [
        #Init   Min     Max
        [300,   100,    500],    
        [300,   100,    500],    
        [300,   100,    500]     
    ]
    
    # Init application
    app = QApplication(sys.argv)
    control = RcServoMotorControl(motor_cnt, motor_ticks)
    control.show()
    sys.exit(app.exec())
