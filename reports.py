from abc import ABC, abstractmethod
from typing import List, Any, Dict, Type

from exceptions import UnknownReportTypeError


class BaseReport(ABC):
    @property
    @abstractmethod
    def headers(self) -> List[str]:
        """Заголовки для таблицы"""
        pass

    @abstractmethod
    def compute(self, logs: List[Dict[str, Any]]) -> List[List[Any]]:
        """Вычисляет табличные данные для отчёта"""
        pass

    def generate(self, logs: List[Dict[str, Any]]) -> str:
        from tabulate import tabulate

        data = self.compute(logs)
        return tabulate(data, headers=self.headers, showindex=True)


class AverageReport(BaseReport):
    @property
    def headers(self):
        return ["handler", "total", "avg_response_time"]

    def compute(self, logs):
        data = {}
        for log in logs:
            handler = log["url"]
            data.setdefault(handler, {"count": 0, "sum": 0.0})
            data[handler]["count"] += 1
            data[handler]["sum"] += float(log["response_time"])
        rows = []
        for handler, stats in sorted(data.items(), key=lambda x: -x[1]["count"]):
            avg = stats["sum"] / stats["count"]
            rows.append([handler, stats["count"], round(avg, 3)])
        return rows


def get_report_class(report_type: str) -> Type[BaseReport]:
    reports = {
        "average": AverageReport,
    }
    try:
        return reports[report_type]
    except KeyError:
        raise UnknownReportTypeError(report_type, list(reports.keys()))
