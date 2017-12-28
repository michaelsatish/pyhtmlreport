import os

import pytest

from pyhtmlreport import Report


@pytest.fixture(scope='function')
def temp_dir(tmpdir_factory):
    td = tmpdir_factory.mktemp('download')
    yield td


def test_setup(temp_dir):
    r = Report()
    root_report_folder = os.path.join(temp_dir, 'Reports')
    r.setup(root_report_folder, module_name='Test Module')
    assert os.path.exists(root_report_folder)

    assert 'Test Module' in os.listdir(root_report_folder)[0]
    assert 'Capture' in os.listdir(os.path.join(root_report_folder, os.listdir(root_report_folder)[0]))[0]


def test_capture_screenshot(temp_dir):
    r = Report()
    root_report_folder = os.path.join(temp_dir, 'Reports')
    r.setup(root_report_folder, module_name='Test Screenshot')

    capture_folder = os.path.join(root_report_folder, os.listdir(root_report_folder)[0], 'Capture')
    r.capture_screenshot()
    assert len(os.listdir(capture_folder)) == 1


def test_generate_report(temp_dir):
    r = Report()
    root_report_folder = os.path.join(temp_dir, 'Reports')
    r.setup(root_report_folder, module_name='Test Module', release_name='Test Release')
    r.write_step('Test', r.status.Start)
    r.write_step('Test Passed', r.status.Pass, screenshot=True)
    r.write_step('Test Failed', r.status.Fail, screenshot=True)
    r.write_step('Test Warning', r.status.Fail, screenshot=True)
    r.generate_report()
    assert 'Report.html' in os.listdir(os.path.join(root_report_folder, os.listdir(root_report_folder)[0]))


if __name__ == '__main__':
    pytest.main()
