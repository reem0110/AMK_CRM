import sys
import mysql.connector
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt


# ---------------- DATABASE ----------------

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="probroyoyo2020",
        database="crm_amk"
    )


# ---------------- CLIENT PROFILE ----------------

class ClientProfile(QDialog):

    def __init__(self, client_id):
        super().__init__()

        self.client_id = client_id
        self.setWindowTitle("Client Orders")
        self.resize(700,500)

        layout = QVBoxLayout(self)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["ID","Service","Area","Price","Status"]
        )

        layout.addWidget(self.table)

        self.load_orders()

    def load_orders(self):

        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("""
        SELECT id,service,area,price,status
        FROM orders
        WHERE client_id=%s
        """,(self.client_id,))

        data = cur.fetchall()

        self.table.setRowCount(len(data))

        for r,o in enumerate(data):
            self.table.setItem(r,0,QTableWidgetItem(str(o["id"])))
            self.table.setItem(r,1,QTableWidgetItem(o["service"]))
            self.table.setItem(r,2,QTableWidgetItem(str(o["area"])))
            self.table.setItem(r,3,QTableWidgetItem(str(o["price"])))
            self.table.setItem(r,4,QTableWidgetItem(o["status"]))

        conn.close()


# ---------------- MAIN WINDOW ----------------

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("AMK CRM")
        self.resize(1200,700)

        self.setStyleSheet("""

        QWidget{
            background:#F4F6F9;
            color:#1F2933;
            font-size:14px;
        }

        QFrame{
            background:white;
            border:1px solid #E5E7EB;
            border-radius:8px;
        }

        QPushButton{
            background:#2F6FED;
            color:white;
            border:none;
            padding:8px;
            border-radius:6px;
        }

        QPushButton:hover{
            background:#1f4fbf;
        }

        QLineEdit, QComboBox{
            background:white;
            border:1px solid #D1D5DB;
            padding:6px;
            border-radius:6px;
        }

        QTableWidget{
            background:white;
            gridline-color:#E5E7EB;
        }

        """)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout(main_widget)

        # -------- SIDEBAR --------

        sidebar_layout = QVBoxLayout()

        title = QLabel("AMK CRM")
        title.setStyleSheet("font-size:22px;font-weight:bold")

        sidebar_layout.addWidget(title)

        self.btn_dashboard = QPushButton("Dashboard")
        self.btn_clients = QPushButton("Clients")
        self.btn_orders = QPushButton("Orders")
        self.btn_brigades = QPushButton("Brigades")

        for b in [self.btn_dashboard,self.btn_clients,self.btn_orders,self.btn_brigades]:
            b.setMinimumHeight(40)
            sidebar_layout.addWidget(b)

        sidebar_layout.addStretch()

        sidebar = QWidget()
        sidebar.setLayout(sidebar_layout)
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("background:#E9EEF6")

        main_layout.addWidget(sidebar)

        # -------- STACK --------

        self.stack = QStackedWidget()

        self.dashboard_page = self.create_dashboard()
        self.clients_page = self.create_clients()
        self.orders_page = self.create_orders()
        self.brigades_page = self.create_brigades()

        self.stack.addWidget(self.dashboard_page)
        self.stack.addWidget(self.clients_page)
        self.stack.addWidget(self.orders_page)
        self.stack.addWidget(self.brigades_page)

        main_layout.addWidget(self.stack)

        self.btn_dashboard.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.btn_clients.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.btn_orders.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        self.btn_brigades.clicked.connect(lambda: self.stack.setCurrentIndex(3))

        self.load_clients()
        self.load_orders()
        self.load_brigades()
        self.update_dashboard()

    # ---------------- DASHBOARD ----------------

    def create_dashboard(self):

        w = QWidget()
        layout = QVBoxLayout(w)

        title = QLabel("Dashboard")
        title.setStyleSheet("font-size:20px;font-weight:bold")
        layout.addWidget(title)

        grid = QGridLayout()

        self.clients_count = QLabel("0")
        self.orders_count = QLabel("0")
        self.completed_count = QLabel("0")
        self.brigades_count = QLabel("0")

        grid.addWidget(self.card("Clients",self.clients_count),0,0)
        grid.addWidget(self.card("Orders",self.orders_count),0,1)
        grid.addWidget(self.card("Completed",self.completed_count),1,0)
        grid.addWidget(self.card("Brigades",self.brigades_count),1,1)

        layout.addLayout(grid)

        return w

    def card(self,title,value):

        frame = QFrame()
        layout = QVBoxLayout(frame)

        label = QLabel(title)
        value.setStyleSheet("font-size:28px;font-weight:bold")

        layout.addWidget(label)
        layout.addWidget(value)

        return frame

    def update_dashboard(self):

        conn=get_connection()
        cur=conn.cursor()

        cur.execute("SELECT COUNT(*) FROM clients")
        self.clients_count.setText(str(cur.fetchone()[0]))

        cur.execute("SELECT COUNT(*) FROM orders")
        self.orders_count.setText(str(cur.fetchone()[0]))

        cur.execute("SELECT COUNT(*) FROM orders WHERE status='Completed'")
        self.completed_count.setText(str(cur.fetchone()[0]))

        cur.execute("SELECT COUNT(*) FROM brigades")
        self.brigades_count.setText(str(cur.fetchone()[0]))

        conn.close()

    # ---------------- CLIENTS ----------------

    def create_clients(self):

        w=QWidget()
        layout=QVBoxLayout(w)

        self.client_search=QLineEdit()
        self.client_search.setPlaceholderText("Search client...")
        self.client_search.textChanged.connect(self.load_clients)

        layout.addWidget(self.client_search)

        self.clients_table=QTableWidget()
        self.clients_table.setColumnCount(3)
        self.clients_table.setHorizontalHeaderLabels(["Name","Phone","Address"])
        self.clients_table.cellDoubleClicked.connect(self.open_client)

        layout.addWidget(self.clients_table)

        btn=QPushButton("Add Client")
        btn.clicked.connect(self.add_client)

        layout.addWidget(btn)

        return w

    def add_client(self):

        name,ok=QInputDialog.getText(self,"Name","Client name")
        if not ok:return

        phone,ok=QInputDialog.getText(self,"Phone","Phone")
        if not ok:return

        address,ok=QInputDialog.getText(self,"Address","Address")
        if not ok:return

        conn=get_connection()
        cur=conn.cursor()

        cur.execute(
        "INSERT INTO clients(name,phone,address) VALUES(%s,%s,%s)",
        (name,phone,address)
        )

        conn.commit()
        conn.close()

        self.load_clients()
        self.update_dashboard()

    def load_clients(self):

        keyword=self.client_search.text()

        conn=get_connection()
        cur=conn.cursor(dictionary=True)

        if keyword:
            cur.execute("SELECT * FROM clients WHERE name LIKE %s",(f"%{keyword}%",))
        else:
            cur.execute("SELECT * FROM clients")

        data=cur.fetchall()

        self.clients_table.setRowCount(len(data))

        for r,c in enumerate(data):
            self.clients_table.setItem(r,0,QTableWidgetItem(c["name"]))
            self.clients_table.setItem(r,1,QTableWidgetItem(c["phone"]))
            self.clients_table.setItem(r,2,QTableWidgetItem(c["address"]))

        conn.close()

    def open_client(self,row,col):

        name=self.clients_table.item(row,0).text()

        conn=get_connection()
        cur=conn.cursor(dictionary=True)

        cur.execute("SELECT id FROM clients WHERE name=%s",(name,))
        client_id=cur.fetchone()["id"]

        conn.close()

        dialog=ClientProfile(client_id)
        dialog.exec()

    # ---------------- ORDERS ----------------

    def create_orders(self):

        w=QWidget()
        layout=QVBoxLayout(w)

        self.status_filter=QComboBox()
        self.status_filter.addItems(["All","New","In Progress","Completed"])
        self.status_filter.currentTextChanged.connect(self.load_orders)

        layout.addWidget(self.status_filter)

        self.orders_table=QTableWidget()

        self.orders_table.setColumnCount(7)
        self.orders_table.setHorizontalHeaderLabels([
        "ID","Client","Service","Area","Price","Status","Created"
        ])

        layout.addWidget(self.orders_table)

        btn_layout=QHBoxLayout()

        create_btn=QPushButton("Create Order")
        create_btn.clicked.connect(self.create_order)

        assign_btn=QPushButton("Assign Brigade")
        assign_btn.clicked.connect(self.assign_brigade)

        status_btn=QPushButton("Change Status")
        status_btn.clicked.connect(self.change_status)

        btn_layout.addWidget(create_btn)
        btn_layout.addWidget(assign_btn)
        btn_layout.addWidget(status_btn)

        layout.addLayout(btn_layout)

        return w

    def create_order(self):

        conn=get_connection()
        cur=conn.cursor(dictionary=True)

        cur.execute("SELECT * FROM clients")
        clients=cur.fetchall()

        names=[c["name"] for c in clients]

        client,ok=QInputDialog.getItem(self,"Client","Client",names,0,False)
        if not ok:return

        service,ok=QInputDialog.getText(self,"Service","Service")
        if not ok:return

        area,ok=QInputDialog.getDouble(self,"Area","Area")
        if not ok:return

        price,ok=QInputDialog.getDouble(self,"Price","Price")
        if not ok:return

        cur.execute("SELECT id FROM clients WHERE name=%s",(client,))
        client_id=cur.fetchone()["id"]

        cur.execute("""
        INSERT INTO orders(client_id,service,area,price,status)
        VALUES(%s,%s,%s,%s,'New')
        """,(client_id,service,area,price))

        conn.commit()
        conn.close()

        self.load_orders()
        self.update_dashboard()

    def assign_brigade(self):

        row=self.orders_table.currentRow()
        if row==-1:return

        order_id=self.orders_table.item(row,0).text()

        conn=get_connection()
        cur=conn.cursor(dictionary=True)

        cur.execute("SELECT * FROM brigades")
        brigades=cur.fetchall()

        names=[b["name"] for b in brigades]

        brigade,ok=QInputDialog.getItem(self,"Brigade","Select brigade",names,0,False)
        if not ok:return

        cur.execute("SELECT id FROM brigades WHERE name=%s",(brigade,))
        brigade_id=cur.fetchone()["id"]

        cur.execute("UPDATE orders SET brigade_id=%s WHERE id=%s",(brigade_id,order_id))

        conn.commit()
        conn.close()

        self.load_orders()

    def change_status(self):

        row=self.orders_table.currentRow()
        if row==-1:return

        order_id=self.orders_table.item(row,0).text()

        statuses=["New","In Progress","Completed"]

        status,ok=QInputDialog.getItem(self,"Status","Select",statuses,0,False)
        if not ok:return

        conn=get_connection()
        cur=conn.cursor()

        cur.execute("UPDATE orders SET status=%s WHERE id=%s",(status,order_id))

        conn.commit()
        conn.close()

        self.load_orders()
        self.update_dashboard()

    def load_orders(self):

        status=self.status_filter.currentText()

        conn=get_connection()
        cur=conn.cursor(dictionary=True)

        query="""
        SELECT
        orders.id,
        clients.name AS client,
        orders.service,
        orders.area,
        orders.price,
        orders.status,
        orders.created_at
        FROM orders
        LEFT JOIN clients ON orders.client_id=clients.id
        """

        if status!="All":
            query+=" WHERE orders.status=%s"
            cur.execute(query,(status,))
        else:
            cur.execute(query)

        data=cur.fetchall()

        self.orders_table.setRowCount(len(data))

        for r,o in enumerate(data):
            self.orders_table.setItem(r,0,QTableWidgetItem(str(o["id"])))
            self.orders_table.setItem(r,1,QTableWidgetItem(str(o["client"])))
            self.orders_table.setItem(r,2,QTableWidgetItem(str(o["service"])))
            self.orders_table.setItem(r,3,QTableWidgetItem(str(o["area"])))
            self.orders_table.setItem(r,4,QTableWidgetItem(str(o["price"])))
            self.orders_table.setItem(r,5,QTableWidgetItem(str(o["status"])))
            self.orders_table.setItem(r,6,QTableWidgetItem(str(o["created_at"])))

        conn.close()

    # ---------------- BRIGADES ----------------

    def create_brigades(self):

        w=QWidget()
        layout=QVBoxLayout(w)

        self.brigade_table=QTableWidget()
        self.brigade_table.setColumnCount(1)
        self.brigade_table.setHorizontalHeaderLabels(["Brigade"])

        layout.addWidget(self.brigade_table)

        btn=QPushButton("Add Brigade")
        btn.clicked.connect(self.add_brigade)

        layout.addWidget(btn)

        return w

    def add_brigade(self):

        name,ok=QInputDialog.getText(self,"Brigade","Name")
        if not ok:return

        conn=get_connection()
        cur=conn.cursor()

        cur.execute("INSERT INTO brigades(name) VALUES(%s)",(name,))

        conn.commit()
        conn.close()

        self.load_brigades()
        self.update_dashboard()

    def load_brigades(self):

        conn=get_connection()
        cur=conn.cursor(dictionary=True)

        cur.execute("SELECT * FROM brigades")

        data=cur.fetchall()

        self.brigade_table.setRowCount(len(data))

        for r,b in enumerate(data):
            self.brigade_table.setItem(r,0,QTableWidgetItem(b["name"]))

        conn.close()


# ---------------- RUN ----------------

app=QApplication(sys.argv)

window=MainWindow()
window.show()

sys.exit(app.exec())