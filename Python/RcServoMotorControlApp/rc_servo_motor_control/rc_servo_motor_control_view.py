# --------------------------------------------------------------------------------
#   File        rc_servo_motor_control_view.py
#
#   Version     v0.1  2025.11.05  Tony Kwon
#                   Initial revision
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
#   Import
# --------------------------------------------------------------------------------
import json
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QGroupBox,
    QComboBox,
    QSlider
)
from PySide6.QtCore import Qt

from .rc_servo_motor_control_model import RcServoMotor, RcServoMotorControlModel

# --------------------------------------------------------------------------------
#   Class - RcServoMotorControlView
# --------------------------------------------------------------------------------
class RcServoMotorControlView(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model        
        self.motor_cnt = len(model.motors)

        self.line_edits = []
        self.plus_buttons = []
        self.minus_buttons = []
        self.ok_buttons = []
        self.sliders = []
        
        self.init_ui()        

        self.is_initialized = False

        # Init sliders
        for i in range(self.motor_cnt):
            self.line_edits[i].setText(str(self.model.motors[i].tick))
            self.sliders[i].setRange(self.model.motors[i].tick_min, self.model.motors[i].tick_max)
            self.sliders[i].setValue(self.model.motors[i].tick_init)
  
        self.is_initialized = True
    
    def init_ui(self):
        # ----------------------------------------
        # Set column layout
        # ----------------------------------------
        column_v_layout = QVBoxLayout()        
        
        # Set 'Setup' GroupBox
        self.setup_group_box = QGroupBox('Setup')
        setup_v_layout = QVBoxLayout()
        
        # Set 'Port' ComboBox
        port_h_layout = QHBoxLayout()
        port_label = QLabel('Port')
        self.port_combo_box = QComboBox()
        self.port_combo_box.addItems(['COM' + str(i) for i in range(1, 10)])
        self.port_combo_box.setCurrentText('COM5')
        port_h_layout.addWidget(port_label)
        port_h_layout.addWidget(self.port_combo_box)
        setup_v_layout.addLayout(port_h_layout)

        # Set 'Connect/Disconnect' PushButton
        connect_disconnect_h_layout = QHBoxLayout()
        self.connect_button = QPushButton('Connect')
        self.disconnect_button = QPushButton('Disconnect')
        connect_disconnect_h_layout.addWidget(self.connect_button)
        connect_disconnect_h_layout.addWidget(self.disconnect_button)
        setup_v_layout.addLayout(connect_disconnect_h_layout)
        
        self.connect_button.clicked.connect(self.on_connect_clicked)
        self.disconnect_button.clicked.connect(self.on_disconnect_clicked)
        
        # Set 'Init' PushButton and 'Step' LineEdit
        init_button_h_layout = QHBoxLayout()
        self.init_button = QPushButton('Init')

        step_controls_h_layout = QHBoxLayout()
        step_label = QLabel('Step')
        self.step_line_edit = QLineEdit()
        self.step_line_edit.setText('2')
        self.step_line_edit.setFixedWidth(50)

        step_controls_h_layout.addStretch(1)
        step_controls_h_layout.addWidget(step_label)
        step_controls_h_layout.addWidget(self.step_line_edit)

        init_button_h_layout.addWidget(self.init_button, 1)
        init_button_h_layout.addLayout(step_controls_h_layout, 1)
        setup_v_layout.addLayout(init_button_h_layout)
        
        self.init_button.clicked.connect(self.on_init_clicked)  

        # Setup GroupBox        
        self.setup_group_box.setLayout(setup_v_layout)

        initial_setup_width = self.setup_group_box.sizeHint().width()
        adjusted_width = int(initial_setup_width * 2.0)
        self.setup_group_box.setFixedWidth(adjusted_width)
        
        column_v_layout.addWidget(self.setup_group_box)

        # Set 'Motor' GroupBox
        for i in range(1, self.motor_cnt + 1):            
            group_box = QGroupBox(f'Motor {i}')
            group_box.setFixedHeight(100)
            group_box.setFixedWidth(adjusted_width)
            v_layout = QVBoxLayout()

            tick_angle_h_layout = QHBoxLayout()
            label = QLabel('Tick')
            line_edit = QLineEdit()
            line_edit.setText('0')
            plus_button = QPushButton('▲')
            minus_button = QPushButton('▼')
            ok_button = QPushButton('OK')
            
            tick_angle_h_layout.addWidget(label)
            tick_angle_h_layout.addWidget(line_edit)
            tick_angle_h_layout.addWidget(plus_button)
            tick_angle_h_layout.addWidget(minus_button)
            tick_angle_h_layout.addWidget(ok_button)
            
            slider = QSlider(Qt.Horizontal)
            slider.setRange(0, 0)
            slider.setValue(0)
            
            v_layout.addLayout(tick_angle_h_layout)
            v_layout.addWidget(slider)

            group_box.setLayout(v_layout)
            column_v_layout.addWidget(group_box)

            self.line_edits.append(line_edit)
            self.plus_buttons.append(plus_button)
            self.minus_buttons.append(minus_button)
            self.ok_buttons.append(ok_button)
            self.sliders.append(slider)

            plus_button.clicked.connect(lambda _, idx=i-1: self.on_motor_up_clicked(idx))
            minus_button.clicked.connect(lambda _, idx=i-1: self.on_motor_down_clicked(idx))
            ok_button.clicked.connect(lambda _, idx=i-1: self.on_motor_ok_clicked(idx))            
            slider.valueChanged.connect(lambda value, idx=i-1: self.on_slider_value_changed(idx, value))

        # ----------------------------------------
        # Set root layout
        # ----------------------------------------
        root_h_layout = QHBoxLayout()
        root_h_layout.addLayout(column_v_layout)
        self.setLayout(root_h_layout)

        fixed_width = root_h_layout.sizeHint().width() + 20
        fixed_height = root_h_layout.sizeHint().height() + 20
        self.setFixedSize(fixed_width, fixed_height)

    # ----------------------------------------
    # 'Setup' event
    # ----------------------------------------
    def on_connect_clicked(self):
        print('Connect')
        selected_port = self.port_combo_box.currentText()
        self.model.connect(selected_port, 115200)  
        
    def on_disconnect_clicked(self):
        print('Disconnect')
        self.model.disconnect()  
        
    def on_init_clicked(self):
        print("Init")        
        for i in range(self.motor_cnt):
            value = self.model.motors[i].tick_init
            self.model.set_tick(i, value)            
            self.line_edits[i].setText(str(value))
            self.sliders[i].setValue(value)
        self.model.rotate()

    # ----------------------------------------
    # 'Motor' event
    # ----------------------------------------        
    def on_motor_up_clicked(self, index):
        print('Motor' + str(index + 1)  + ' Up')
        value = int(self.line_edits[index].text())
        value = value + int(self.step_line_edit.text())       
        self.model.set_tick(index, value)
        self.line_edits[index].setText(str(value))
        self.sliders[index].setValue(value)

    def on_motor_down_clicked(self, index):
        print('Motor' + str(index + 1)  + ' Down')
        value = int(self.line_edits[index].text())
        value = value - int(self.step_line_edit.text())            
        self.model.set_tick(index, value)        
        self.line_edits[index].setText(str(value))
        self.sliders[index].setValue(value)

    def on_motor_ok_clicked(self, index):
        print('Motor' + str(index + 1)  + ' OK')
        value = int(self.line_edits[index].text())     
        self.model.set_tick(index, value)           
        self.sliders[index].setValue(value)
        
    def on_slider_value_changed(self, index, value):        
        if(self.is_initialized is True):
            print('Motor' + str(index + 1)  + ' Slider Value = ' + str(value))         
            self.line_edits[index].setText(str(value))    
            self.model.set_tick(index, value)
            self.model.rotate()
