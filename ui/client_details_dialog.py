from PySide6.QtWidgets import QDialog,QVBoxLayout,QLabel


class ClientDetailsDialog(QDialog):

    def __init__(self,name):

        super().__init__()

        self.setWindowTitle("Client Details")

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel(f"Client: {name}"))

        layout.addWidget(QLabel("Order history will appear here"))