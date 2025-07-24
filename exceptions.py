class UnknownReportTypeError(Exception):
    def __init__(self, report_type: str):
        self.report_type = report_type
        super().__init__(f"Unknown report type: {report_type}")
