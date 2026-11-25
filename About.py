from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class About(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("About - Heat Conduction")
        self.resize(360, 420)

        self.title_label = QLabel("Heat Conduction Simulation")
        self.title_label.setObjectName("title")

        self.image_label = QLabel()
        self.image_label.setFixedSize(140, 140)
        pixmap = QPixmap("my_photo.jpg")
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)

        self.name_label = QLabel("Name: Shaked Shabtay")
        self.email_label = QLabel("Email: Shaked789@gmail.com")

        self.linkedin_label = QLabel('<a href="https://www.linkedin.com/in/shaked-shabtay">My LinkedIn Profile</a>')
        self.linkedin_label.setOpenExternalLinks(True)

        self.github_label = QLabel('<a href="https://github.com/ShakedShabtay/heat-conduction">GitHub Repository</a>')
        self.github_label.setOpenExternalLinks(True)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.title_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.name_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.email_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.linkedin_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.github_label, alignment=Qt.AlignCenter)
        layout.addStretch()

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication()
    window = About()
    window.show()
    app.exec()