from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QStackedWidget, QLabel
from ui.dashboard_page import DashboardPage
from ui.clients_page import ClientsPage
from ui.orders_page import OrdersPage
from ui.brigades_page import BrigadesPage


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("CRM")
        self.resize(1200, 700)

        main_layout = QHBoxLayout(self)

        sidebar = QVBoxLayout()

        title = QLabel("CRM")
        sidebar.addWidget(title)

        self.btn_dashboard = QPushButton("Dashboard")
        self.btn_clients = QPushButton("Clients")
        self.btn_orders = QPushButton("Orders")
        self.btn_brigades = QPushButton("Brigades")

        sidebar.addWidget(self.btn_dashboard)
        sidebar.addWidget(self.btn_clients)
        sidebar.addWidget(self.btn_orders)
        sidebar.addWidget(self.btn_brigades)
        sidebar.addStretch()

        main_layout.addLayout(sidebar)

        self.stack = QStackedWidget()

        self.dashboard_page = DashboardPage()
        self.clients_page = ClientsPage()
        self.orders_page = OrdersPage()
        self.brigades_page = BrigadesPage()

        self.stack.addWidget(self.dashboard_page)
        self.stack.addWidget(self.clients_page)
        self.stack.addWidget(self.orders_page)
        self.stack.addWidget(self.brigades_page)

        main_layout.addWidget(self.stack)

        self.btn_dashboard.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.btn_clients.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.btn_orders.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        self.btn_brigades.clicked.connect(lambda: self.stack.setCurrentIndex(3))