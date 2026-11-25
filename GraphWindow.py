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
        if self.main_window is None:
            return
        if len(self.main_window.time_history) == 0:
            return

        selected_body = self.body_combo.currentText()
        if selected_body == "Body 1":
            self.ax.plot(
                self.main_window.time_history,
                self.main_window.body1_temp_history,
                color="red",
                label="Body 1"
            )
        else:
            self.ax.plot(
                self.main_window.time_history,
                self.main_window.body2_temp_history,
                color="blue",
                label="Body 2"
            )

        self.ax.legend()
        self.canvas.draw()

    def clear_clicked(self):
        self.ax.clear()
        self.style_axes()
        self.canvas.draw()

    def export_csv(self):
        if self.main_window is None:
            return
        if len(self.main_window.time_history) == 0:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Simulation Results", "heat_conduction.csv", "CSV Files (*.csv)"
        )
        if file_path != "":
            with open(file_path, "w") as f:
                f.write("Time (s),Body 1 Temperature (C),Body 2 Temperature (C)\n")
                for i in range(len(self.main_window.time_history)):
                    t = self.main_window.time_history[i]
                    t1 = self.main_window.body1_temp_history[i]
                    t2 = self.main_window.body2_temp_history[i]
                    f.write(f"{t},{t1:.2f},{t2:.2f}\n")

            if sys.platform == "win32":
                os.startfile(file_path)
            elif sys.platform == "darwin":
                subprocess.run(["open", file_path])
            else:
                subprocess.run(["xdg-open", file_path])