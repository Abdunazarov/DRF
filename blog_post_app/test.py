
class Computer():
    def __init__(self, brand, ram, storage):
        self.brand = brand
        self.ram = ram
        self.storage = storage




class Mobile(Computer):
    def __init__(self, brand, ram, storage, model):
        super().__init__(brand, ram, storage)
        self.model = model



# mobile = Mobile("Samsung", 4, 64, "Galaxy S21")
# print(mobile.__dict__)
