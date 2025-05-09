from worker import Worker


class File:
    def __init__(self, *args):
        self.files: list = [*args]
        self.read_files: list = []

    def read(self):
        self.read_files: list = []
        read_file: list = []
        for file in self.files:
            with open(file, "r") as f:
                lines = f.readlines()
                read_file = []
                for line in lines:
                    read_file.append(line.split("\n"))
                self.read_files.append(read_file)
        return self.read_files

    def convert_list_to_dict(self):
        read_file = self.read()
        file_list_dict: list = []
        if len(read_file) == 0:
            return "error"
        for file in self.read_files:
            header = file[0][0].split(",")
            file.pop(0)
            for val in file:
                count: int = 0
                val1 = val[count]
                val1 = val1.strip().split(",")
                cache: dict = {}
                while count <= len(val1) - 1:
                    if header[count] == "salary" or header[count] == "hourly_rate":
                        header[count] = "rate"
                    cache[header[count]] = val1[count]
                    count += 1
                file_list_dict.append(cache)
        return file_list_dict

    def create_list_worker(self):
        list_dicts = self.convert_list_to_dict()
        list_obj = []
        for dict in list_dicts:
            worker = Worker(id=dict["id"], email=dict["email"], name=dict["name"], department=dict["department"],
                            hours=dict["hours_worked"], rate=dict["rate"])
            list_obj.append(worker)
        return list_obj

    def create_report_payout(self):
        list_obj = self.create_list_worker()
        list_dep = []
        for obj in list_obj:
            if obj.department not in list_dep:
                list_dep.append(obj.department)
