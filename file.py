import json
import os
from collections import defaultdict
from typing import List, Union, Dict

from worker import Worker


class File:
    def __init__(self, arg):
        self.files: List[str] = arg

    def read(self) -> List[List[List[str]]]:
        read_files: List[List[List[str]]] = []
        for file in self.files:
            try:
                with open(file, "r") as f:
                    lines: List[str] = f.readlines()
                    read_file: List[str] = []
                    for line in lines:
                        read_file.append(line.replace("\n", "").split(","))
                    read_files.append(read_file)
            except:
                raise ValueError(f"file {file} not found")
        return read_files

    def convert_list_to_dict(self) -> List[Dict[str, str]]:
        read_file: List[List[List[str]]] = self.read()
        file_list_dict: List[List[str]] = []
        for file in read_file:
            header = file[0]
            file.pop(0)
            for val in file:
                count: int = 0
                cache: dict = {}
                while count <= len(val) - 1:
                    if header[count] == "salary" or header[count] == "hourly_rate":
                        header[count] = "rate"
                    cache[header[count].lstrip().rstrip()] = val[count].lstrip().rstrip()
                    count += 1
                file_list_dict.append(cache)
        return file_list_dict

    def create_list_worker(self) -> List[Worker]:
        list_dicts: List[Dict[str, str]] = self.convert_list_to_dict()
        list_obj: List[Worker] = []
        for dict in list_dicts:
            worker = Worker(id=dict["id"], email=dict["email"], name=dict["name"], department=dict["department"],
                            hours=dict["hours_worked"], rate=dict["rate"])
            list_obj.append(worker)
        return list_obj

    def create_report_payout(self, filename) -> Dict[str, Dict[str, Union[int, List[Dict[str, Union[str, int]]]]]]:
        list_obj: List[Worker] = self.create_list_worker()
        dict_dep: Dict[str, Dict[str, Union[int, List[Dict[str, Union[str, int]]]]]] = defaultdict(lambda: {
            "workers": [],
            "total_hours": 0,
            "total_payout": 0
        })
        for obj in list_obj:
            dict_dep[obj.department]["workers"].append(
                {
                    "id": obj.id,
                    "email": obj.email,
                    "name": obj.name,
                    "department": obj.department,
                    "hours": obj.hours,
                    "rate": obj.rate
                }
            )
            dict_dep[obj.department]["total_hours"] += obj.hours
            dict_dep[obj.department]["total_payout"] += obj.payout
        self.save_report(dict_dep, filename)
        self.print_report(dict_dep)
        return dict_dep

    def save_report(self, data, filename) -> None:
        try:
            with open(filename, "w") as f:
                json.dump(data, f)
        except:
            os.makedirs(os.path.dirname(filename))

    def print_report(self, report) -> None:
        print(15 * " ", "name", 11 * " ", "hours", 2 * " ", "rate", 1 * " ", "payout", 9 * " ")
        for dep, data in sorted(report.items()):
            print(dep)
            for worker in data["workers"]:
                payout = worker["hours"] * worker["rate"]
                print(15 * " ", worker["name"], (15 - len(worker["name"])) * " ", worker["hours"],
                      (7 - len(str(worker["hours"]))) * " ", worker["rate"], (5 - len(str(worker["rate"]))) * " ", "$",
                      payout,
                      ((15 - len(str(payout))) * " "))
            print(32 * " ", data["total_hours"], (7 - len(str(data["total_hours"]))) * " ", 6 * " ", "$",
                  data["total_payout"])
