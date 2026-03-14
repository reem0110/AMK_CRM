from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class DashboardPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("Dashboard")
        layout.addWidget(title)

        layout.addWidget(QLabel("Statistics will be displayed here"))