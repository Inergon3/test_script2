class Worker:
    def __init__(self, id, email, name, department, hours, rate):
        self.id = int(id)
        self.email = email
        self.name = name
        self.department = department
        self.hours = int(hours)
        self.rate = int(rate)
        self.payout = self.hours * self.rate