from PySide6.QtWidgets import QWidget,QVBoxLayout,QTableWidget,QTableWidgetItem
from dao.order_dao import get_all_orders


class OrdersPage(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout(self)

        self.table = QTableWidget()

        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels(
            ["ID","Client","Service","Status"]
        )

        layout.addWidget(self.table)

        self.load_orders()


    def load_orders(self):

        orders = get_all_orders()

        self.table.setRowCount(len(orders))

        for row,order in enumerate(orders):

            self.table.setItem(row,0,QTableWidgetItem(str(order["id"])))
            self.table.setItem(row,1,QTableWidgetItem(str(order["client_id"])))
            self.table.setItem(row,2,QTableWidgetItem(str(order["service"])))
            self.table.setItem(row,3,QTableWidgetItem(str(order["status"])))