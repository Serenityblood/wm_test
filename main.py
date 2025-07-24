import argparse
import sys
from reports import get_report_class
from logreader import LogReader
from exceptions import UnknownReportTypeError


def main():
    parser = argparse.ArgumentParser(description="Скрипт для анализа логов")
    parser.add_argument("--file", nargs="+", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--date", required=False)
    args = parser.parse_args()

    try:
        reader = LogReader(args.file, args.date)
        logs = reader.read_logs()
    except FileNotFoundError as e:
        print(f"File error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    try:
        report_cls = get_report_class(args.report)
        report = report_cls()
        table = report.generate(logs)
        print(table)
    except UnknownReportTypeError as e:
        print(f"{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
