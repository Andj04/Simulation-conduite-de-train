from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog
from PyQt5.QtGui import QPainter, QBrush, QPen, QFont, QColor, QLinearGradient
from PyQt5.QtCore import Qt, QTimer, QDateTime

import sys
import os
import csv
from PyQt5.QtMultimedia import QSound

class TrainSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Train Simulator")
        self.setGeometry(100, 100, 1080, 600)
        self.setStyleSheet("background-color: #001f3f;")  # Dark blue background

        # Main widget and layout
        main_widget = QWidget()
        main_layout = QHBoxLayout()

        # Variables
        self.speed = 0  # Simulated speed
        self.is_braking = False
        self.alarm_active = False
        self.doors_open = False
        self.deadman_timer_value = 30  # Time in seconds before deadman triggers
        self.warning_threshold = 10  # Time for warning before full emergency stop
        self.remaining_time = self.deadman_timer_value  # Remaining time for the deadman system

        # Station-related variables
        self.stations = [5, 10, 15, 20, 25]  # Distances to stations in km
        self.current_station_index = 0  # Index of the current station
        self.distance_to_next_station = self.stations[self.current_station_index]  # Distance to the next station

        # Reaction time recording
        self.reaction_times = []  # List to store reaction times
        self.last_action_time = QDateTime.currentDateTime() 

        # Left zone: Speed Control
        self.left_zone = self.create_speed_control()
        main_layout.addWidget(self.left_zone)

        # Center zone: Train position
        self.center_zone = self.create_train_zone()
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

        # Deadman Timer
        self.deadman_timer = QTimer(self)
        self.deadman_timer.timeout.connect(self.update_deadman_timer)
        self.deadman_timer.start(1000)  # Decrease every second

        # Timer for alarm sound
        self.alarm_sound_timer = QTimer(self)
        self.alarm_sound_timer.timeout.connect(self.play_alarm_sound)

    def play_alarm_sound(self):
        if self.alarm_active:
            QSound.play("alarm.wav")  # Path to alarm sound file

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

        self.distance_label = QLabel(f"Distance to next station: {self.distance_to_next_station:.2f} km")
        self.distance_label.setFont(QFont("Roboto", 18))
        self.distance_label.setStyleSheet("color: #00aaff; background-color: #003f5f; padding: 10px; border-radius: 10px; border: 2px solid #005f7f;")
        layout.addWidget(self.distance_label)

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

        save_btn = QPushButton("Save Reaction Times")
        save_btn.setFont(QFont("Roboto", 16))
        save_btn.setStyleSheet(button_style)
        save_btn.clicked.connect(self.save_reaction_times)
        layout.addWidget(save_btn)

        widget.setLayout(layout)
        return widget

    def create_alarm_zone(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Speed alarm
        self.alarm_label = QLabel("Alarm: OFF")
        self.alarm_label.setFont(QFont("Roboto", 20))
        self.alarm_label.setStyleSheet("background-color: green; color: white; font-size: 20px; padding: 10px; border-radius: 10px;")
        layout.addWidget(self.alarm_label)

        # Door alarm
        self.door_alarm_label = QLabel("Doors: CLOSED")
        self.door_alarm_label.setFont(QFont("Roboto", 20))
        self.door_alarm_label.setStyleSheet("background-color: red; color: white; font-size: 20px; padding: 10px; border-radius: 10px;")
        layout.addWidget(self.door_alarm_label)

        # Deadman Timer display
        self.deadman_label = QLabel(f"Deadman Timer: {self.remaining_time}s")
        self.deadman_label.setFont(QFont("Roboto", 20))
        self.deadman_label.setStyleSheet("background-color: green; color: white; font-size: 20px; padding: 10px; border-radius: 10px;")
        layout.addWidget(self.deadman_label)

        # Reset Deadman Button
        reset_btn = QPushButton("Reset Deadman")
        reset_btn.setFont(QFont("Roboto", 16))
        reset_btn.setStyleSheet("""
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
        """)
        reset_btn.clicked.connect(self.reset_deadman_timer)
        layout.addWidget(reset_btn)

        widget.setLayout(layout)
        return widget

    def create_train_zone(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.train_position_widget = TrainPositionWidget()
        layout.addWidget(self.train_position_widget)

        # Door control buttons
        door_control_layout = QVBoxLayout()
        open_button = QPushButton("Open Doors")
        close_button = QPushButton("Close Doors")

        button_style = """
            QPushButton {
                background-color: #003f5f;
                color: #00aaff;
                padding: 15px;
                border-radius: 10px;
                border: 2px solid #003f7f;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #0077cc;
            }
            QPushButton:pressed {
                background-color: #004f7f;
            }
        """
        open_button.setStyleSheet(button_style)
        close_button.setStyleSheet(button_style)

        open_button.clicked.connect(self.open_doors)
        close_button.clicked.connect(self.close_doors)

        door_control_layout.addWidget(open_button)
        door_control_layout.addWidget(close_button)
        layout.addLayout(door_control_layout)

        widget.setLayout(layout)
        return widget

    
    def record_reaction_time(self, action: str):
        now = QDateTime.currentDateTime()
        elapsed_time = self.last_action_time.msecsTo(now) / 1000  # Reaction time in seconds
        self.reaction_times.append((action, elapsed_time))
        self.last_action_time = now

    def save_reaction_times(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Reaction Times", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_path:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Action", "Reaction Time (s)"])
                writer.writerows(self.reaction_times)


    def update_simulation(self):
        # Update speed display
        self.speed_label.setText(f"Speed: {self.speed} km/h")

        # Apply braking if active
        if self.is_braking and self.speed > 0:
            self.speed = max(0, self.speed - 2)

        # Update train position
        self.train_position_widget.update_position(self.speed)

        # Update distance to next station
        if self.speed > 0 and self.current_station_index < len(self.stations):
            self.distance_to_next_station -= (self.speed / 3600) * 0.1  # Convert speed to km per 100ms

            # Check for critical distance
            if self.distance_to_next_station <= 0.5:
                self.alarm_label.setText("Alarm: Slow down!")
                self.alarm_label.setStyleSheet("background-color: orange; color: white; font-size: 20px; padding: 10px; border-radius: 10px;")
                if not self.alarm_active:
                    self.alarm_active = True
                    self.play_alarm_sound()

            # Check if the station is reached
            if self.distance_to_next_station <= 0:
                self.current_station_index += 1
                if self.current_station_index < len(self.stations):
                    self.distance_to_next_station = self.stations[self.current_station_index] - self.stations[self.current_station_index - 1]
                    self.alarm_label.setText("Alarm: OFF")
                    self.alarm_label.setStyleSheet("background-color: green; color: white; font-size: 20px; padding: 10px; border-radius: 10px;")
                    self.alarm_active = False
                else:
                    self.distance_to_next_station = 0
                    self.speed = 0
                    self.alarm_label.setText("End of journey")
                    self.alarm_label.setStyleSheet("background-color: red; color: white; font-size: 20px; padding: 10px; border-radius: 10px;")

        self.distance_label.setText(f"Distance to next station: {self.distance_to_next_station:.2f} km")

    def update_deadman_timer(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.deadman_label.setText(f"Deadman Timer: {self.remaining_time}s")

            if self.remaining_time <= self.warning_threshold:
                self.deadman_label.setStyleSheet("background-color: orange; color: white; font-size: 20px; padding: 10px; border-radius: 10px;")
                QSound.play("alarm.wav")

            if self.remaining_time == 0:
                self.trigger_emergency_stop()
        else:
            self.trigger_emergency_stop()

    def trigger_emergency_stop(self):
        self.slow_to_stop()
        self.deadman_label.setText("EMERGENCY STOP")
        self.deadman_label.setStyleSheet("background-color: red; color: white; font-size: 20px; padding: 10px; border-radius: 10px;")
        QSound.play("alarm.wav")

    def reset_deadman_timer(self):
        self.remaining_time = self.deadman_timer_value
        self.deadman_label.setText(f"Deadman Timer: {self.remaining_time}s")
        self.deadman_label.setStyleSheet("background-color: green; color: white; font-size: 20px; padding: 10px; border-radius: 10px;")

    def open_doors(self):
        self.record_reaction_time("Start Braking")
        self.deadman_timer_value = 30
        self.remaining_time = self.deadman_timer_value
        self.deadman_label.setStyleSheet("background-color: green; color: white; font-size: 20px; padding: 10px; border-radius: 10px;")
        if self.speed == 0 and not self.doors_open:
            self.doors_open = True
            self.door_alarm_label.setText("Doors: OPEN")
            self.door_alarm_label.setStyleSheet("background-color: green; color: white; font-size: 20px; padding: 10px; border-radius: 10px;")
            QSound.play("alarm.wav")

    def close_doors(self):
        self.record_reaction_time("Start Braking")
        self.deadman_timer_value = 30
        self.remaining_time = self.deadman_timer_value
        self.deadman_label.setStyleSheet("background-color: green; color: white; font-size: 20px; padding: 10px; border-radius: 10px;")
        if self.doors_open:
            self.doors_open = False
            self.door_alarm_label.setText("Doors: CLOSED")
            self.door_alarm_label.setStyleSheet("background-color: red; color: white; font-size: 20px; padding: 10px; border-radius: 10px;")
            QSound.play("alarm.wav")

    def start_acceleration(self):
        self.record_reaction_time("Start Acceleration")
        self.remaining_time = self.deadman_timer_value  # Reset the deadman timer
        self.deadman_label.setStyleSheet("background-color: green; color: white; font-size: 20px; padding: 10px; border-radius: 10px;")
        self.acceleration_timer = QTimer(self)
        self.acceleration_timer.timeout.connect(self.accelerate)
        self.acceleration_timer.start(200)

    def stop_acceleration(self):
        self.record_reaction_time("Stop Acceleration")
        if hasattr(self, 'acceleration_timer'):
            self.acceleration_timer.stop()
        if self.alarm_active:
            self.alarm_active = False
            self.alarm_label.setText("Alarm: OFF")
            self.alarm_label.setStyleSheet("background-color: green; color: white; font-size: 20px; padding: 10px; border-radius: 10px;")
            self.alarm_sound_timer.stop()

    def accelerate(self):
            if self.doors_open:
                self.alarm_label.setText("Alarm: DOORS OPEN")
                self.alarm_label.setStyleSheet("background-color: red; color: white; font-size: 20px; padding: 10px; border-radius: 10px;")
                QSound.play("alarm.wav")
            elif self.speed < 300:
                self.speed += 10
            else:
                if not self.alarm_active:
                    self.alarm_active = True
                    self.alarm_label.setText("Alarm: MAX SPEED")
                    self.alarm_label.setStyleSheet("background-color: red; color: white; font-size: 20px; padding: 10px; border-radius: 10px;")
                    self.alarm_sound_timer.start(1500)

    def start_braking(self):
        self.record_reaction_time("Start Braking")
        self.deadman_timer_value = 30
        self.is_braking = True
        self.remaining_time = self.deadman_timer_value  # Reset the deadman timer
        self.deadman_label.setStyleSheet("background-color: green; color: white; font-size: 20px; padding: 10px; border-radius: 10px;")

    def stop_braking(self):
        self.record_reaction_time("Start Braking")
        self.is_braking = False

    def slow_to_stop(self):
        self.is_braking = True
        time = self.speed * 15000 / 300  # Calculate stopping time based on speed
        QTimer.singleShot(int(time), self.stop)  # Stop after calculated time

    def stop(self):
        self.deadman_timer_value = 30
        self.speed = 0
        self.is_braking = False

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

