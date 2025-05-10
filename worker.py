class Worker:
    def __init__(self, id: str, email: str, name: str, department: str, hours: str, rate: str):
        self.id: int = int(id)
        self.email: str = email
        self.name: str = name
        self.department: str = department
        self.hours: int = int(hours)
        self.rate: int = int(rate)
        self.payout: int = self.hours * self.rate