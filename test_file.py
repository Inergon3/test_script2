import json

import pytest

from file import File


def test_read(tmp_path):
    test_file = tmp_path / "test.csv"
    test_file.write_text(
        "id,name\n"
        "11,qwe qwe\n"
    )

    file = File([str(test_file)])
    result = file.read()
    assert result == [[["id", "name"], ["11", "qwe qwe"]]]


def test_read_error():
    name_file = "qwe.csv"
    file = File([name_file])
    with pytest.raises(ValueError, match=f"file {name_file} not found"):
        file.read()


def test_convert_list_to_dict_first(tmp_path):
    test_file = tmp_path / "test.csv"
    test_file.write_text(
        "id,name\n"
        "11,qwe qwe\n"
    )

    file = File([str(test_file)])
    result = file.convert_list_to_dict()
    assert result == [{"id": "11", "name": "qwe qwe"}]


def test_convert_list_to_dict_second(tmp_path):
    test_file = tmp_path / "test.csv"
    test_file.write_text(
        "id,name\n"
        "11,qwe qwe\n"
    )

    test_file2 = tmp_path / "test2.csv"
    test_file2.write_text(
        "name,id\n"
        "asd asd,1"
    )
    test_list = [str(test_file), str(test_file2)]
    file2 = File(test_list)
    result = file2.convert_list_to_dict()
    assert result == [{"id": "11", "name": "qwe qwe"}, {"name": "asd asd", "id": "1"}]

def test_create_list_workers(tmp_path):
    test_file = tmp_path / "test.csv"
    test_file.write_text(
        "id,email, name, department ,hours_worked,hourly_rate\n"
        "1,alice@example.com, Alice Johnson, Marketing, 160, 50\n"
        "2,bob@example.com, Bob Smith,Design,150,40"
    )
    file = File([str(test_file)])
    result = file.create_list_worker()
    assert result[0].id == 1
    assert result[0].name == "Alice Johnson"
    assert  result[1].id == 2
    assert  result[1].name == "Bob Smith"

def test_create_report_payout(tmp_path):
    test_file = tmp_path / "test.csv"
    test_file.write_text(
        "id,email, name, department ,hours_worked,hourly_rate\n"
        "1,alice@example.com, Alice Johnson, Marketing, 160, 50\n"
        "2,bob@example.com, Bob Smith,Design,150,40"
    )

    file = File([str(test_file)])

    file.save_report = lambda data, filename: None
    file.print_report = lambda report: None

    result = file.create_report_payout(str(tmp_path / "report.json"))

    assert "Marketing" in result
    assert "Design" in result

    assert result["Marketing"]["total_hours"] == 160
    assert result["Marketing"]["total_payout"] == 8000

    assert result["Design"]["total_hours"] == 150
    assert result["Design"]["total_payout"] == 6000

    assert result["Marketing"]["workers"][0]["name"] == "Alice Johnson"
    assert result["Design"]["workers"][0]["name"] == "Bob Smith"

def test_save_report(tmp_path):
    file = File([])
    test_data = {
        "HR": {
            "workers": [{"id": 1, "name": "Alice", "email": "a@a.com", "department": "HR", "hours": 40, "rate": 25}],
            "total_hours": 40,
            "total_payout": 1000
        }
    }

    filename = tmp_path / "report.json"
    file.save_report(test_data, str(filename))

    assert filename.exists()

    with open(filename) as f:
        content = json.load(f)
        assert content == test_data