from PySide6.QtWidgets import QWidget,QVBoxLayout,QPushButton,QTableWidget,QTableWidgetItem,QInputDialog
from dao.brigade_dao import add_brigade,get_all_brigades


class BrigadesPage(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout(self)

        self.btn_add = QPushButton("Add Brigade")

        layout.addWidget(self.btn_add)

        self.table = QTableWidget()

        self.table.setColumnCount(1)
        self.table.setHorizontalHeaderLabels(["Brigade"])

        layout.addWidget(self.table)

        self.btn_add.clicked.connect(self.add)

        self.load()


    def load(self):

        brigades = get_all_brigades()

        self.table.setRowCount(len(brigades))

        for row,b in enumerate(brigades):

            self.table.setItem(row,0,QTableWidgetItem(b["name"]))


    def add(self):

        name,ok = QInputDialog.getText(self,"Add Brigade","Name")

        if ok and name:

            add_brigade(name)

            self.load()