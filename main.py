import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, 
                               QScrollArea, QDialog, QFormLayout, QMessageBox, QHBoxLayout, QStackedLayout, QFrame)
from PySide6.QtCore import Qt
from client_dao import add_client, get_all_clients, search_clients, delete_client
from order_dao import get_all_orders

# ---------------- CLIENT CARD ----------------
class ClientCard(QWidget):
    def __init__(self, client, refresh_callback):
        super().__init__()
        self.client = client
        self.refresh_callback = refresh_callback
        self.expanded = False

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setStyleSheet("background-color: #F3F4F6; color: black; border-radius: 10px; padding: 10px;")

        # Main visible info
        self.title = QLabel(f"{client['name']}")
        self.title.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(self.title)

        # Expandable details
        self.details = QWidget()
        details_layout = QVBoxLayout()
        self.details.setLayout(details_layout)
        self.details.setVisible(False)

        details_layout.addWidget(QLabel(f"Phone: {client['phone']}"))
        details_layout.addWidget(QLabel(f"Address: {client['address']}"))
        self.layout.addWidget(self.details)

        # Buttons
        btn_layout = QHBoxLayout()
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setStyleSheet("background-color: #EF4444; color: white; border-radius: 5px; padding: 5px;")
        self.delete_btn.clicked.connect(self.confirm_delete)
        btn_layout.addWidget(self.delete_btn)

        self.expand_btn = QPushButton("Expand")
        self.expand_btn.setStyleSheet("background-color: #6366F1; color: white; border-radius: 5px; padding: 5px;")
        self.expand_btn.clicked.connect(self.toggle_expand)
        btn_layout.addWidget(self.expand_btn)

        self.layout.addLayout(btn_layout)

    def toggle_expand(self):
        self.expanded = not self.expanded
        self.details.setVisible(self.expanded)
        self.expand_btn.setText("Collapse" if self.expanded else "Expand")

    def confirm_delete(self):
        reply = QMessageBox.question(self, "Confirm Delete", f"Delete client {self.client['name']}?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            delete_client(self.client['id'])
            self.refresh_callback()

# ---------------- ADD CLIENT DIALOG ----------------
class AddClientDialog(QDialog):
    def __init__(self, refresh_callback):
        super().__init__()
        self.refresh_callback = refresh_callback
        self.setWindowTitle("Add New Client")
        self.setStyleSheet("background-color: #FFFFFF; color: black;")
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.address_input = QLineEdit()

        self.layout.addRow("Name:", self.name_input)
        self.layout.addRow("Phone:", self.phone_input)
        self.layout.addRow("Address:", self.address_input)

        self.add_btn = QPushButton("Add")
        self.add_btn.setStyleSheet("background-color: #10B981; color: white; padding: 5px; border-radius: 5px;")
        self.add_btn.clicked.connect(self.add_client)
        self.layout.addWidget(self.add_btn)

    def add_client(self):
        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        address = self.address_input.text().strip()
        if name and phone and address:
            add_client(name, phone, address)
            self.refresh_callback()
            self.accept()
        else:
            QMessageBox.warning(self, "Warning", "Please fill all fields!")

# ---------------- MAIN WINDOW ----------------
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AMK CRM")
        self.resize(1000, 650)
        self.setStyleSheet("background-color: #FFFFFF; color: black;")

        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # ---------------- SIDEBAR ----------------
        sidebar = QFrame()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("background-color: #F3F4F6;")
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(10, 20, 10, 10)
        sidebar_layout.setSpacing(20)
        sidebar.setLayout(sidebar_layout)

        logo = QLabel("AMK CRM")
        logo.setStyleSheet("font-size: 22px; font-weight: bold;")
        sidebar_layout.addWidget(logo)

        self.clients_btn = QPushButton("Clients")
        self.orders_btn = QPushButton("Orders")
        for btn in [self.clients_btn, self.orders_btn]:
            btn.setStyleSheet("padding: 10px; text-align: left; border-radius: 5px; background-color: #E5E7EB;")
        self.clients_btn.clicked.connect(lambda: self.switch_view("clients"))
        self.orders_btn.clicked.connect(lambda: self.switch_view("orders"))
        sidebar_layout.addWidget(self.clients_btn)
        sidebar_layout.addWidget(self.orders_btn)
        sidebar_layout.addStretch()

        main_layout.addWidget(sidebar)

        # ---------------- STACKED LAYOUT ----------------
        self.stack = QStackedLayout()
        main_layout.addLayout(self.stack)

        # Clients view
        self.clients_widget = QWidget()
        clients_layout = QVBoxLayout()
        self.clients_widget.setLayout(clients_layout)

        # Search
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search clients...")
        self.search_input.textChanged.connect(self.refresh_clients)
        self.search_input.setStyleSheet("padding: 5px; border-radius: 5px;")
        clients_layout.addWidget(self.search_input)

        # Scroll area for cards
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)
        clients_layout.addWidget(self.scroll_area)

        # Add client button
        self.add_btn = QPushButton("Add Client")
        self.add_btn.setStyleSheet("background-color: #10B981; color: white; padding: 10px; border-radius: 5px;")
        self.add_btn.clicked.connect(self.open_add_client)
        clients_layout.addWidget(self.add_btn)

        self.stack.addWidget(self.clients_widget)

        # Orders view placeholder
        self.orders_widget = QWidget()
        orders_layout = QVBoxLayout()
        self.orders_widget.setLayout(orders_layout)
        orders_layout.addWidget(QLabel("Orders view coming soon..."))
        self.stack.addWidget(self.orders_widget)

        # Default view
        self.switch_view("clients")

    def refresh_clients(self):
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        keyword = self.search_input.text().strip()
        clients = search_clients(keyword) if keyword else get_all_clients()
        for client in clients:
            card = ClientCard(client, self.refresh_clients)
            self.scroll_layout.addWidget(card)

    def open_add_client(self):
        dialog = AddClientDialog(self.refresh_clients)
        dialog.exec()

    def switch_view(self, view):
        if view == "clients":
            self.stack.setCurrentWidget(self.clients_widget)
            self.clients_btn.setStyleSheet("padding: 10px; text-align: left; border-radius: 5px; background-color: #6366F1; color:white;")
            self.orders_btn.setStyleSheet("padding: 10px; text-align: left; border-radius: 5px; background-color: #E5E7EB; color:black;")
        else:
            self.stack.setCurrentWidget(self.orders_widget)
            self.orders_btn.setStyleSheet("padding: 10px; text-align: left; border-radius: 5px; background-color: #6366F1; color:white;")
            self.clients_btn.setStyleSheet("padding: 10px; text-align: left; border-radius: 5px; background-color: #E5E7EB; color:black;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())