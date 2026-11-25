import os
import sys
import subprocess
import matplotlib
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt
from PySide6.QtWidgets import (
    QWidget, QPushButton, QComboBox,
    QFileDialog, QVBoxLayout, QHBoxLayout
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT


class GraphWindow(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Graph Window")
        self.resize(650, 420)

        self.fig, self.ax = plt.subplots(1, 1)
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.style_axes()

        graph_layout = QVBoxLayout()
        graph_layout.addWidget(self.toolbar)
        graph_layout.addWidget(self.canvas)

        self.body_combo = QComboBox()
        self.body_combo.addItems(["Body 1", "Body 2"])

        self.draw_btn = QPushButton("Draw")
        self.draw_btn.clicked.connect(self.draw_clicked)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_clicked)

        self.export_btn = QPushButton("Export to CSV")
        self.export_btn.clicked.connect(self.export_csv)

        controls_layout = QVBoxLayout()
        controls_layout.addWidget(self.body_combo)
        controls_layout.addWidget(self.draw_btn)
        controls_layout.addWidget(self.clear_btn)
        controls_layout.addWidget(self.export_btn)
        controls_layout.addStretch()

        main_layout = QHBoxLayout()
        main_layout.addLayout(graph_layout)
        main_layout.addLayout(controls_layout)

        self.setLayout(main_layout)

    def style_axes(self):
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Temperature (°C)")
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)

    def draw_clicked(self):
        pass

    def clear_clicked(self):
        pass

    def export_csv(self):
        pass