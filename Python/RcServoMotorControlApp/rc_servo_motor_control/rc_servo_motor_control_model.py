# --------------------------------------------------------------------------------
#   File        rc_servo_motor_control_model.py
#
#   Version     v0.1  2025.11.05  Tony Kwon
#                   Initial revision
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
#   Import
# --------------------------------------------------------------------------------
import numpy as np
from .serial_comm import SerialComm

# --------------------------------------------------------------------------------
#   Class - RcServoMotor
# --------------------------------------------------------------------------------
class RcServoMotor:
    def __init__(self, ticks):
        self.tick = ticks[0]
        self.tick_init = ticks[0]
        self.tick_min = ticks[1]
        self.tick_max = ticks[2]
        
    def set_tick(self, tick):
        self.tick = tick        
        
    def get_tick(self):
        return self.tick
        
# --------------------------------------------------------------------------------
#   Class - RcServoMotorControlModel
# --------------------------------------------------------------------------------
class RcServoMotorControlModel:
    def __init__(self):
        # Comm        
        self.comm = SerialComm()
        self.connected = False

        # Motors
        self.motors = []        

    def add_motor(self, motor):
        self.motors.append(motor)

    def connect(self, port, baud):
        if self.comm.init(port, baud):
            self.connected = True
        else:
            self.connected = False

    def disconnect(self):
        self.comm.deinit()
        self.connected = False

    def set_tick(self, index, tick):
        self.motors[index].set_tick(tick)
            
    def get_tick(self, index):
        return self.motors[index].get_tick()       
    
    def rotate(self):
        # Set comm data
        data = [0xFF, 0xFF, len(self.motors)]
        for motor in self.motors:
            data.append(0xFF & (motor.tick >> 8))
            data.append(0xFF & motor.tick)

        # TX comm data
        if self.connected:
            self.comm.write(data)


