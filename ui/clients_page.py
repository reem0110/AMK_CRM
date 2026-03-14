from PySide6.QtWidgets import QWidget,QVBoxLayout,QLineEdit,QTableWidget,QTableWidgetItem
from dao.client_dao import get_all_clients, search_clients
from ui.client_details_dialog import ClientDetailsDialog


class ClientsPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search client...")
        layout.addWidget(self.search)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Name","Phone","Address"])

        layout.addWidget(self.table)

        self.search.textChanged.connect(self.load_clients)
        self.table.cellDoubleClicked.connect(self.open_client)

        self.load_clients()


    def load_clients(self):

        keyword = self.search.text()

        if keyword:
            clients = search_clients(keyword)
        else:
            clients = get_all_clients()

        self.table.setRowCount(len(clients))

        for row,client in enumerate(clients):

            self.table.setItem(row,0,QTableWidgetItem(client["name"]))
            self.table.setItem(row,1,QTableWidgetItem(client["phone"]))
            self.table.setItem(row,2,QTableWidgetItem(client["address"]))

            self.table.setRowHeight(row,40)


    def open_client(self,row,col):

        name = self.table.item(row,0).text()

        dialog = ClientDetailsDialog(name)

        dialog.exec()