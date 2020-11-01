from tempfile import TemporaryDirectory
from datetime import datetime

import pytest

from .objects import Report, Test

# Singleton
report = Report()


def pytest_addoption(parser) -> None:
    """Register pythmlreport command line options."""

    report_path_help = 'Set the report path.'
    filename_help = 'Set the report filename.'

    group = parser.getgroup('pyhtmlreport')
    group.addoption('--report-path', dest='report_path', help=report_path_help)
    group.addoption('--filename', dest='filename', help=filename_help)

    parser.addini('report_path', report_path_help)
    parser.addini('filename', filename_help)


def pytest_configure(config) -> None:
    """Setup report dependencies."""
    report_path_cmd_option = config.option.report_path
    filename_cmd_option = config.option.filename

    report.path = report_path_cmd_option if report_path_cmd_option \
        else TemporaryDirectory()

    report.filename = filename_cmd_option if filename_cmd_option \
        else f'report-{datetime.now().strptime("%m-%d-%Y-%H-%M-%S")}'

    config.add_cleanup(report.create_report())


@pytest.fixture
def test(request):
    identifier = request.node.nodeid
    test_id = request.own_markers

    t = Test(identifier=identifier)

    try:
        yield t
    finally:
        report.append_test(t)


def pytest_exception_interact(node, call) -> None:
    identifier = node.nodeid
    failed_stage = call.when
    test = report.get_test(identifier=identifier)
