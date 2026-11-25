from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QSlider,
    QDoubleSpinBox, QAbstractSpinBox, QVBoxLayout, QHBoxLayout, QGridLayout
)
from PySide6.QtCore import Qt, QTimer
from Body import Body
from About import About
from GraphWindow import GraphWindow


class HeatTransfer(QWidget):
    def __init__(self):
        super().__init__()
        self.graph_window = GraphWindow(self)
        self.about_window = About()

        self.body1 = None
        self.body2 = None
        self.current_time = 0.0
        self.time_history = []
        self.body1_temp_history = []
        self.body2_temp_history = []

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timer_method)

        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Heat Transfer Simulation")
        self.resize(620, 430)


        self.left_slider = QSlider(Qt.Vertical)
        self.left_slider.setRange(0, 200)
        self.left_slider.setValue(200)
        self.left_slider.valueChanged.connect(self.left_temperature_changed)

        self.left_body_box = QLabel()
        self.left_body_box.setFixedSize(110, 160)
        self.update_body_color(self.left_body_box, 200)


        self.cond_label = QLabel("Conductivity")
        self.cond_spin = QDoubleSpinBox()
        self.cond_spin.setRange(0.01, 100.0)
        self.cond_spin.setValue(1.00)
        self.cond_spin.setSuffix(" J/s*C")

        self.bridge_bar = QLabel()
        self.bridge_bar.setFixedSize(150, 24)
        self.bridge_bar.setStyleSheet("background-color: darkgray;")

        bridge_layout = QVBoxLayout()
        bridge_layout.addStretch()
        bridge_layout.addWidget(self.cond_label, alignment=Qt.AlignCenter)
        bridge_layout.addWidget(self.cond_spin, alignment=Qt.AlignCenter)
        bridge_layout.addWidget(self.bridge_bar)
        bridge_layout.addStretch()


        self.right_body_box = QLabel()
        self.right_body_box.setFixedSize(110, 160)
        self.update_body_color(self.right_body_box, 0)

        self.right_slider = QSlider(Qt.Vertical)
        self.right_slider.setRange(0, 200)
        self.right_slider.setValue(0)
        self.right_slider.valueChanged.connect(self.right_temperature_changed)

        top_visual_layout = QHBoxLayout()
        top_visual_layout.addStretch()
        top_visual_layout.addWidget(self.left_slider)
        top_visual_layout.addWidget(self.left_body_box)
        top_visual_layout.addLayout(bridge_layout)
        top_visual_layout.addWidget(self.right_body_box)
        top_visual_layout.addWidget(self.right_slider)
        top_visual_layout.addStretch()


        self.left_temp_spin = QDoubleSpinBox()
        self.left_temp_spin.setRange(0.0, 200.0)
        self.left_temp_spin.setDecimals(1)
        self.left_temp_spin.setValue(200.0)
        self.left_temp_spin.setSuffix(" °C")
        self.left_temp_spin.setReadOnly(True)
        self.left_temp_spin.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.left_mass_spin = QDoubleSpinBox()
        self.left_mass_spin.setRange(0.1, 1000.0)
        self.left_mass_spin.setValue(10.00)
        self.left_mass_spin.setSuffix(" kg")

        self.left_cap_spin = QDoubleSpinBox()
        self.left_cap_spin.setRange(0.01, 100.0)
        self.left_cap_spin.setValue(0.40)
        self.left_cap_spin.setSuffix(" J/kg*C")

        left_grid = QGridLayout()
        left_grid.addWidget(QLabel("Temp."), 0, 0)
        left_grid.addWidget(self.left_temp_spin, 0, 1)
        left_grid.addWidget(QLabel("Mass"), 1, 0)
        left_grid.addWidget(self.left_mass_spin, 1, 1)
        left_grid.addWidget(QLabel("H. Cap."), 2, 0)
        left_grid.addWidget(self.left_cap_spin, 2, 1)


        self.start_btn = QPushButton("Start")
        self.start_btn.setObjectName("start_btn")
        self.start_btn.setCheckable(True)
        self.start_btn.clicked.connect(self.start_stop_button_method)

        self.graphs_btn = QPushButton("Graphs")
        self.graphs_btn.clicked.connect(self.open_graphs)

        self.about_btn = QPushButton("About")
        self.about_btn.setObjectName("about_btn")
        self.about_btn.clicked.connect(self.open_about)

        center_btns_layout = QVBoxLayout()
        center_btns_layout.addWidget(self.start_btn)
        center_btns_layout.addWidget(self.graphs_btn)
        center_btns_layout.addWidget(self.about_btn)


        self.right_temp_spin = QDoubleSpinBox()
        self.right_temp_spin.setRange(0.0, 200.0)
        self.right_temp_spin.setDecimals(1)
        self.right_temp_spin.setValue(0.0)
        self.right_temp_spin.setSuffix(" °C")
        self.right_temp_spin.setReadOnly(True)
        self.right_temp_spin.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.right_mass_spin = QDoubleSpinBox()
        self.right_mass_spin.setRange(0.1, 1000.0)
        self.right_mass_spin.setValue(10.00)
        self.right_mass_spin.setSuffix(" kg")

        self.right_cap_spin = QDoubleSpinBox()
        self.right_cap_spin.setRange(0.01, 100.0)
        self.right_cap_spin.setValue(0.40)
        self.right_cap_spin.setSuffix(" J/kg*C")

        right_grid = QGridLayout()
        right_grid.addWidget(self.right_temp_spin, 0, 0)
        right_grid.addWidget(QLabel("Temp."), 0, 1)
        right_grid.addWidget(self.right_mass_spin, 1, 0)
        right_grid.addWidget(QLabel("Mass"), 1, 1)
        right_grid.addWidget(self.right_cap_spin, 2, 0)
        right_grid.addWidget(QLabel("H. Cap."), 2, 1)

        bottom_controls_layout = QHBoxLayout()
        bottom_controls_layout.addStretch()
        bottom_controls_layout.addLayout(left_grid)
        bottom_controls_layout.addSpacing(20)
        bottom_controls_layout.addLayout(center_btns_layout)
        bottom_controls_layout.addSpacing(20)
        bottom_controls_layout.addLayout(right_grid)
        bottom_controls_layout.addStretch()

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_visual_layout)
        main_layout.addSpacing(15)
        main_layout.addLayout(bottom_controls_layout)

        self.setLayout(main_layout)

    def update_body_color(self, widget, temp):
        red = int((temp / 200.0) * 255)
        if red > 255:
            red = 255
        if red < 0:
            red = 0
        widget.setStyleSheet(f"background-color: rgb({red}, 0, 0); border: 1px solid gray;")

    def left_temperature_changed(self):
       pass

    def right_temperature_changed(self):
        pass

    def start_stop_button_method(self):
        pass

    def timer_method(self):
        pass

    def open_graphs(self):
        self.graph_window.show()

    def open_about(self):
        self.about_window.show()

    def closeEvent(self, event):
        self.graph_window.close()
        self.about_window.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication()

    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = HeatTransfer()
    window.show()
    app.exec()