import os

import pytest

from pyhtmlreport import Report


@pytest.fixture(scope='function')
def temp_dir(tmpdir_factory):
    td = tmpdir_factory.mktemp('reports')
    yield td


@pytest.fixture(scope='function')
def tr():
    r = Report()
    yield r


class TestReport:

    def test_setup(self, temp_dir, tr):
        root_report_folder = os.path.join(temp_dir, 'Test Reports')
        tr.setup(root_report_folder, module_name='Test Module')
        assert os.path.exists(root_report_folder)

        module_folder = os.listdir(root_report_folder)[0]
        assert 'Test Module' in module_folder
        assert 'Capture' in os.listdir(os.path.join(root_report_folder, module_folder))[0]

    def test_capture_screenshot(self, temp_dir, tr):
        root_report_folder = os.path.join(temp_dir, 'Test Reports')
        tr.setup(root_report_folder, module_name='Test Module')

        capture_folder = os.path.join(root_report_folder, os.listdir(root_report_folder)[0], 'Capture')
        tr.capture_screenshot()
        assert len(os.listdir(capture_folder)) == 1

    def test_generate_report(self, temp_dir, tr):
        root_report_folder = os.path.join(temp_dir, 'Test Reports')
        tr.setup(root_report_folder, module_name='Test Module')

        tr.write_step('Test', tr.status.Start)
        tr.write_step('Test Passed', tr.status.Pass, screenshot=True)
        tr.write_step('Test Failed', tr.status.Fail, screenshot=True)
        tr.write_step('Test Warning', tr.status.Fail, screenshot=True)

        assert 'Test Module' in tr.generate_report()
        assert 'Report.html' in os.listdir(os.path.join(root_report_folder, os.listdir(root_report_folder)[0]))


if __name__ == '__main__':
    pytest.main()
