from argparse import ArgumentParser

from file import File


def main():
    parser = ArgumentParser()

    parser.add_argument("files", nargs="+", help="Считывание CSV файлов с данными сотрудников")
    parser.add_argument("--report", default="payout.json",
                        help="Сохранение отчета в json файл(по умолчанию payout.json)")

    args = parser.parse_args()
    file = File(args.files)
    file.create_report_payout(args.report)


if __name__ == "__main__":
    main()
