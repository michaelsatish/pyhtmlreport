import os

import pytest
from pyhtmlreport import Report
from pyhtmlreport.report import ReportError


@pytest.fixture
def temp_dir(tmpdir_factory):
    td = tmpdir_factory.mktemp('reports')
    yield td


@pytest.fixture
def tr():
    r = Report()
    yield r


class TestReport:
    def test_report_folder_error(self, tr):
        with pytest.raises(ReportError):
            tr.setup(None)

    def test_number_error(self, tr):
        with pytest.raises(ReportError):
            tr.write_step(
                'This is a Start Step without Test Number',
                tr.status.Start
            )

    def test_pass_status_before_start_error(self, tr):
        with pytest.raises(ReportError):
            tr.write_step(
                'This is Pass Step before Start Status',
                tr.status.Pass
                )

    def test_fail_status_before_start_error(self, tr):
        with pytest.raises(ReportError):
            tr.write_step(
                'This is Fail Step before Start Status',
                tr.status.Fail
            )

    def test_warn_status_before_start_error(self, tr):
        with pytest.raises(ReportError):
            tr.write_step(
                'This is Warn Step before Start Status',
                tr.status.Warn
            )

    def test_highlight_status_before_start_error(self, tr):
        with pytest.raises(ReportError):
            tr.write_step(
                'This is Highlight Step before Start Status',
                tr.status.Highlight
            )

    def test_invalid_step_status_error(self, tr):
        with pytest.raises(ReportError):
            tr.write_step(
                'This is a Start Step',
                tr.status.Start,
                test_number=1
            )
            tr.write_step('This is a Step with Invalid Status', 'Invalid')

    def test_attachment_error(self, tr):
        with pytest.raises(ReportError):
            tr.add_attachment('This is not a file')

    def test_max_screenshots(self, temp_dir, tr):
        assert tr.max_screenshots == 1000

        report_folder = os.path.join(temp_dir, 'Test Reports')
        tr.setup(report_folder, max_screenshots=100000)
        assert tr.max_screenshots == 100000

    def test_attachments(self, temp_dir, tr):
        p = temp_dir.join('text.txt')
        p.write('Testing Attachments')

        tr.add_attachment(p)
        assert len(tr.attachments) == 1

    def test_setup(self, temp_dir, tr):
        report_folder = os.path.join(temp_dir, 'Test Reports')
        tr.setup(report_folder, module_name='Test Application')
        assert os.path.exists(report_folder)

        module_folder = os.listdir(report_folder)[0]
        assert 'Test Application' in module_folder
        assert 'Screenshots' in os.listdir(
            os.path.join(report_folder, module_folder)
        )[0]

    def test_capture_screenshot(self, temp_dir, tr):
        report_folder = os.path.join(temp_dir, 'Test Reports')
        tr.setup(report_folder, module_name='Test Application')

        capture_folder = os.path.join(
            report_folder,
            os.listdir(report_folder)[0],
            'Screenshots'
        )
        tr.capture_screenshot()
        screenshots = os.listdir(capture_folder)
        assert len(screenshots) == 1
        assert screenshots[0] == '0.png'

    def test_generate_report(self, temp_dir, tr):
        report_folder = os.path.join(temp_dir, 'Test Reports')
        tr.setup(report_folder, module_name='Test Application')

        tr.write_step('Start Step', tr.status.Start, test_number=1)
        tr.write_step('Passed Step', tr.status.Pass, screenshot=True)
        tr.write_step('Failed Step', tr.status.Fail, screenshot=True)
        tr.write_step('Warning Step', tr.status.Fail, screenshot=True)

        p = temp_dir.join('text.txt')
        p.write('Testing Attachments')
        tr.add_attachment(p)

        tr.generate_report()

        module_folder = os.listdir(report_folder)[0]
        sub_folders = os.listdir(
            os.path.join(report_folder, module_folder)
        )
        assert 'Attachments' == sub_folders[0]
        assert 'Report.html' == sub_folders[1]
        assert 'text.txt' == os.listdir(
            os.path.join(report_folder, module_folder, 'Attachments')
        )[0]
