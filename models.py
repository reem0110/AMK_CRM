from datetime import datetime

class Client:
    def __init__(self, id=None, name="", phone="", address="", created_at=None):
        self.id = id
        self.name = name
        self.phone = phone
        self.address = address
        self.created_at = created_at or datetime.now()


class Order:
    def __init__(
        self,
        id=None,
        client_id=None,
        brigade_id=None,
        service="",
        status="New",
        date=None
    ):
        self.id = id
        self.client_id = client_id
        self.brigade_id = brigade_id
        self.service = service
        self.status = status
        self.date = date or datetime.now()
        