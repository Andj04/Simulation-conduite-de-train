from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QPainter, QBrush, QPen, QFont, QColor, QLinearGradient
from PyQt5.QtCore import Qt, QTimer
import sys
import os
from PyQt5.QtMultimedia import QSound

class TrainSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Train Simulator")
        self.setGeometry(100, 100, 940, 600)
        self.setStyleSheet("background-color: #001f3f;")  # Dark blue background

        # Main widget and layout
        main_widget = QWidget()
        main_layout = QHBoxLayout()

        # Variables
        self.speed = 0  # Simulated speed
        self.is_braking = False
        self.alarm_active = False

        # Left zone: Speed Control
        self.left_zone = self.create_speed_control()
        main_layout.addWidget(self.left_zone)

        # Center zone: Train position
        self.center_zone = TrainPositionWidget()
        main_layout.addWidget(self.center_zone)

        # Right zone: Alarm system
        self.right_zone = self.create_alarm_zone()
        main_layout.addWidget(self.right_zone)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Timer for simulation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(100)  # Update every 100ms

        # Timer for alarm sound
        self.alarm_sound_timer = QTimer(self)
        self.alarm_sound_timer.timeout.connect(self.play_alarm_sound)

    def create_speed_control(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Style général des boutons
        button_style = """
            QPushButton {
                background-color: #003f5f;
                color: #00aaff;
                padding: 10px;
                border-radius: 10px;
                border: 2px solid #003f7f;
            }
            QPushButton:hover {
                background-color: #0077cc;
            }
            QPushButton:pressed {
                background-color: #004f7f;
            }
        """

        self.speed_label = QLabel("Speed: 0 km/h")
        self.speed_label.setFont(QFont("Roboto", 18))
        self.speed_label.setStyleSheet("color: #00aaff; background-color: #003f5f; padding: 10px; border-radius: 10px; border: 2px solid #005f7f;")
        layout.addWidget(self.speed_label)

        accelerate_btn = QPushButton("Accelerate")
        accelerate_btn.setFont(QFont("Roboto", 16))
        accelerate_btn.setStyleSheet(button_style)
        accelerate_btn.pressed.connect(self.start_acceleration)
        accelerate_btn.released.connect(self.stop_acceleration)
        layout.addWidget(accelerate_btn)

        brake_btn = QPushButton("Brake")
        brake_btn.setFont(QFont("Roboto", 16))
        brake_btn.setStyleSheet(button_style)
        brake_btn.pressed.connect(self.start_braking)
        brake_btn.released.connect(self.stop_braking)
        layout.addWidget(brake_btn)

        stop_btn = QPushButton("Stop")
        stop_btn.setFont(QFont("Roboto", 16))
        stop_btn.setStyleSheet(button_style)
        stop_btn.clicked.connect(self.slow_to_stop)
        layout.addWidget(stop_btn)

        widget.setLayout(layout)
        return widget


    def create_alarm_zone(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.alarm_label = QLabel("Alarm: OFF")
        self.alarm_label.setFont(QFont("Roboto", 20))
        self.alarm_label.setStyleSheet("background-color: green; color: white; font-size: 20px; padding: 10px; border-radius: 10px;")
        layout.addWidget(self.alarm_label)

        widget.setLayout(layout)
        return widget

    def update_simulation(self):
        # Update speed display
        self.speed_label.setText(f"Speed: {self.speed} km/h")

        # Update alarm based on speed
        if self.speed > 300:
            if not self.alarm_active:
                self.alarm_active = True
                self.alarm_label.setText("Alarm: ON")
                self.alarm_label.setStyleSheet("background-color: red; color: white; font-size: 20px; padding: 10px; border-radius: 10px;")
                self.alarm_sound_timer.start(1500)  # Play alarm sound every 1.5 seconds
        else:
            self.alarm_active = False
            self.alarm_label.setText("Alarm: OFF")
            self.alarm_label.setStyleSheet("background-color: green; color: white; font-size: 20px; padding: 10px; border-radius: 10px;")
            self.alarm_sound_timer.stop()

        # Apply braking if active
        if self.is_braking and self.speed > 0:
            self.speed = max(0, self.speed - 2)

        # Update train position
        self.center_zone.update_position(self.speed)

    def accelerate(self):
        if not self.is_braking:
            self.speed += 10

    def brake(self):
        self.is_braking = True

    def stop(self):
        self.speed = 0
        self.is_braking = False

    def start_acceleration(self):
        self.acceleration_timer = QTimer(self)
        self.acceleration_timer.timeout.connect(self.accelerate)
        self.acceleration_timer.start(200)

    def stop_acceleration(self):
        if hasattr(self, 'acceleration_timer'):
            self.acceleration_timer.stop()

    def start_braking(self):
        self.is_braking = True

    def stop_braking(self):
        self.is_braking = False

    def slow_to_stop(self):
        self.is_braking = True
        QTimer.singleShot(2000, self.stop)  # Stop after 2 seconds

    def play_alarm_sound(self):
        if self.alarm_active:
            QSound.play("alarm.wav")  # Path to alarm sound file

class TrainPositionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.train_position = 200
        self.rail_offset = 0

    def update_position(self, speed):
        self.rail_offset += speed * 0.1  # Adjust offset based on speed
        if self.rail_offset > 300:
            self.rail_offset -= 300  # Reset offset to create loop effect
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        # Draw ground with a gradient to simulate terrain
        gradient = QLinearGradient(50, 50, 350, 250)
        gradient.setColorAt(0.0, QColor(160, 82, 45))  # SaddleBrown (terre)
        gradient.setColorAt(0.5, QColor(205, 133, 63))  # Peru (plus clair)
        gradient.setColorAt(1.0, QColor(139, 69, 19))  # Sienna (ombré)

        painter.setBrush(QBrush(gradient))
        painter.drawRect(50, 50, 300, 300)

        # Draw rails (two vertical lines) with realistic proportions
        painter.setPen(QPen(Qt.darkGray, 2, Qt.SolidLine))
        painter.drawLine(100, 50, 100, 350)  # Left rail
        painter.drawLine(250, 50, 250, 350)  # Right rail

        # Add cross-ties for the rails
        painter.setBrush(QBrush(Qt.gray, Qt.SolidPattern))
        for i in range(0, 300, 50):  # Adjust spacing for ties
            tie_y = 50 + (i + self.rail_offset) % 300
            painter.drawRect(85, int(tie_y), 180, 10)  # Draw tie (adjust width and height for appearance)

        # Draw train body
        train_x = 125  # Centered horizontally
        train_y = 150  # Positioned above the rails
        painter.setBrush(QBrush(QColor(70, 130, 180), Qt.SolidPattern))  # Light blue for train body
        painter.drawRoundedRect(train_x, train_y, 100, 50, 10, 10)  # Rounded rectangle for train body

        # Add train windows
        painter.setBrush(QBrush(Qt.white, Qt.SolidPattern))
        painter.drawRect(train_x + 15, train_y + 10, 20, 20)  # Left window
        painter.drawRect(train_x + 65, train_y + 10, 20, 20)  # Right window

        # Add train wheels
        painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
        painter.drawEllipse(train_x + 15, train_y + 40, 15, 15)  # Left wheel
        painter.drawEllipse(train_x + 70, train_y + 40, 15, 15)  # Right wheel

        # Add front light
        painter.setBrush(QBrush(Qt.yellow, Qt.SolidPattern))
        painter.drawEllipse(train_x + 40, train_y - 10, 20, 20)  # Centered front light




if __name__ == "__main__":
    app = QApplication(sys.argv)
    simulator = TrainSimulator()
    simulator.show()
    sys.exit(app.exec_())
