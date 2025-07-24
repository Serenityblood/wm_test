import pytest
from reports import AverageReport, get_report_class
from logreader import LogReader
from exceptions import UnknownReportTypeError


@pytest.mark.parametrize(
    "logs,expected",
    [
        (
            [
                {
                    "url": "/a",
                    "response_time": 1.0,
                    "@timestamp": "2025-06-22T10:00:00+00:00",
                },
                {
                    "url": "/a",
                    "response_time": 3.0,
                    "@timestamp": "2025-06-22T10:05:00+00:00",
                },
                {
                    "url": "/b",
                    "response_time": 2.0,
                    "@timestamp": "2025-06-22T10:10:00+00:00",
                },
            ],
            [["/a", 2, 2.0], ["/b", 1, 2.0]],
        ),
        (
            [
                {
                    "url": "/c",
                    "response_time": 5.0,
                    "@timestamp": "2025-06-22T10:00:00+00:00",
                },
            ],
            [["/c", 1, 5.0]],
        ),
        (
            [],
            [],
        ),
    ],
)
def test_average_report_compute(logs, expected):
    report = AverageReport()
    data = report.compute(logs)
    assert data == expected


def test_average_report_headers():
    report = AverageReport()
    assert report.headers == ["handler", "total", "avg_response_time"]


def test_unknown_report_type():
    with pytest.raises(UnknownReportTypeError):
        get_report_class("unknown_type")


def test_logreader_reads_and_filters(tmp_path):
    data = [
        '{"@timestamp": "2025-06-22T10:00:00+00:00", "url": "/x", "response_time": 1.0}\n',
        '{"@timestamp": "2025-06-23T10:00:00+00:00", "url": "/y", "response_time": 2.0}\n',
    ]
    log_file = tmp_path / "log.json"
    log_file.write_text("".join(data))

    reader = LogReader([str(log_file)], date="2025-06-22")
    logs = reader.read_logs()
    assert len(logs) == 1
    assert logs[0]["url"] == "/x"


def test_logreader_file_not_found():
    from logreader import LogReader

    with pytest.raises(FileNotFoundError):
        LogReader(["/definitely/not_exist.log"]).read_logs()
