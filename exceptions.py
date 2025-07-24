from typing import List


class UnknownReportTypeError(Exception):
    def __init__(self, report_type: str, allowed_types: List[str]):
        self.report_type = report_type
        super().__init__(
            f"Unknown report type: {report_type}. Allowed types: {allowed_types}"
        )
