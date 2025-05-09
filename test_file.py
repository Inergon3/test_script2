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
    assert result[0][0] == ["id", "name"]