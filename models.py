from datetime import datetime

class Client:
    def __init__(self, id=None, name='', phone='', address='', created_at=None):
        self.id = id
        self.name = name
        self.phone = phone
        self.address = address
        self.created_at = created_at or datetime.now()

class Order:
    def __init__(self, id=None, client_id=0, manager_id=0, area='', price=0.0, created_at=None):
        self.id = id
        self.client_id = client_id
        self.manager_id = manager_id
        self.area = area
        self.price = price
        self.created_at = created_at or datetime.now()