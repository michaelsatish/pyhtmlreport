import os
import datetime
import logging
import pkg_resources

from PIL import ImageGrab
from pyhtmlreport.utils import render_pie_chart, render_overall_status_table

logger = logging.getLogger(__name__)
MAX_SCREENSHOTS = 1000


class ReportError(Exception):
    pass


def dispatch_screenshot_number():
    """
    File name for screenshots
    Generator to yield a number from 0 to arg: MAX_SCREENSHOTS
    By default it is 1000 (MAX_SCREENSHOTS)

    :return: generator
    """
    for x in list(range(MAX_SCREENSHOTS)):
        yield x


def update_test_status(p, f, w):
    """
    Update total passed, failed and warning tests
    Called before every test to update status of completed test, and called in function generate_report to update the
    status of final test

    If one or more fail steps, test is marked as failed
    If one or more warn steps and no fail steps, test is maked as warning
    If one or more pass steps and no fail or warn steps, test is marked as passed

    :param p: number of pass steps in a test
    :param f: number of fail steps in a test
    :param w: number of warn steps in a test
    :return: list 
    
    Unpacked in function update_test_status to update total passed, failed and warning tests
    """
    if f >= 1:
        return [0, 1, 0]

    if w >= 1 and f == 0:
        return [0, 0, 1]

    if p >= 1 and f == 0 and w == 0:
        return [1, 0, 0]


class Status:

    Start = 'Start'
    Pass = 'Pass'
    Fail = 'Fail'
    Warn = 'Warn'
    Highlight = 'Highlight'


class Report:

    def __init__(self):

        self.report_folder = None
        self.application_folder = None
        self.capture_folder = None

        self.application_name = None
        self.release_name = None
        self.selenium_driver = None

        with open(pkg_resources.resource_filename(__name__, 'data/report.html')) as f:
            self.html = f.read()

        self.step = ''
        self.screenshot = ''

        self.total_tests, self.passed_tests, self.failed_tests, self.warning_tests = 0, 0, 0, 0
        self.pass_step, self.fail_step, self.warn_step = 0, 0, 0

        self.status = Status
        self.screenshot_num = dispatch_screenshot_number()

    def setup(self, report_folder, application_name='default', release_name='default', selenium_driver=None):
        """
        Setup followed by initialization of Report class to create report folders
        :param report_folder:
        :param application_name:
        :param release_name:
        :param selenium_driver: pass the initialized webdriver to use the method save_screenshot for screenshots
        :return:
        """
        if not report_folder:
            raise ReportError('Require Report Root Folder path')

        if application_name == 'default':
            import warnings
            warnings.warn('Application name set to default')

        self.report_folder = report_folder
        self.application_name = application_name
        self.release_name = release_name

        self.application_folder = os.path.join(
            self.report_folder,
            '{name} {date}'.format(
                name=self.application_name,
                date=datetime.datetime.now().strftime('%m_%d_%Y %H_%M_%S')
                )
            )

        self.capture_folder = os.path.join(self.application_folder, 'Capture')
        self.selenium_driver = selenium_driver

        if not os.path.exists(self.report_folder):
            os.mkdir(self.report_folder)

        if not os.path.exists(self.application_folder):
            os.mkdir(self.application_folder)

        if not os.path.exists(self.capture_folder):
            os.mkdir(self.capture_folder)

    @property
    def use_selenium_driver(self):
        return self.selenium_driver

    @use_selenium_driver.setter
    def use_selenium_driver(self, driver):
        self.selenium_driver = driver

    def __repr__(self):
        return 'Report(application_name=%s, release_name=%s)' % (self.application_name, self.release_name)

    def capture_screenshot(self):
        """
        Capture screenshot
        If selenium_driver is set, screenshot of the browser view port is captured
        """
        current_screenshot = os.path.join(self.capture_folder, str(next(self.screenshot_num)) + '.png')
        try:
            if self.selenium_driver:
                self.selenium_driver.save_screenshot(current_screenshot)
            else:
                ImageGrab.grab().save(current_screenshot)

            return current_screenshot
        except Exception as e:
            logging.error(msg=f'Unable to capture screenshot {e}')

    def update_test_status(self):
        if all(not x for x in [self.total_tests, self.pass_step, self.fail_step, self.warn_step]):
            return

        if all(x == 0 for x in [self.total_tests, self.pass_step, self.fail_step, self.warn_step]):
            return

        status = update_test_status(self.pass_step, self.fail_step, self.warn_step)
        
        if status:
            self.passed_tests += status[0]
            self.failed_tests += status[1]
            self.warning_tests += status[2]
        
        self.pass_step = 0
        self.fail_step = 0
        self.warn_step = 0

    def write_step(self, step, status, screenshot=False):
        if screenshot:
            cc = self.capture_screenshot()
            self.screenshot = f"""
                            <div class="text-center" style="width: 25px; height: 25px;">
                                <a href="{cc}">
                                    <img src="{cc}" style="width: 25px; height: 25px;">
                                </a>
                            </div>
                            """
        else:
            self.screenshot = ''

        if status == 'Start':
            self.step += f"""
                            <tr class="table-info">
                                <td><b>{step}</b></td>
                                <td></td>
                                <td></td>
                            </tr>
                            """
            self.update_test_status()
            self.total_tests += 1

        if status == 'Pass':
            self.pass_step += 1
            self.step += f"""
                            <tr>
                                <td>{step}</td>
                                <td>Passed</td>
                                <td>{self.screenshot}</td>
                            </tr>
                            """

        if status == 'Fail':
            self.fail_step += 1
            self.step += f"""
                            <tr class="bg-danger">
                                <td>{step}</td>
                                <td>Failed</td>
                                <td>{self.screenshot}</td>
                            </tr>
                            """

        if status == 'Warn':
            self.warn_step += 1
            self.step += f"""
                            <tr class="bg-warning">
                                <td>{step}</td>
                                <td>Warning</td>
                                <td>{self.screenshot}</td>
                            </tr>
                            """
        if status == 'Highlight':
            self.step += f"""
                            <tr class="table-success">
                                <td>{step}</td>
                                <td></td>
                                <td>{self.screenshot}</td>
                            </tr>
                            """

    def generate_report(self):
        """
        Generate the Report, render overall status and pie chart
        :return: report folder
        """
        self.update_test_status()

        try:
            with open(os.path.join(self.application_folder, 'Report.html'), 'w') as f:
                d = {
                    'module_name': self.application_name,
                    'release_name': self.release_name,
                    'date': datetime.datetime.now().strftime('%m_%d_%Y'),
                    'result': self.step,
                    'overall_status': render_overall_status_table(self.total_tests, self.passed_tests,
                                                                  self.failed_tests, self.warning_tests),
                    'pie_chart': render_pie_chart(self.passed_tests, self.failed_tests, self.warning_tests)
                }
                f.write(self.html.format(**d))
        except Exception as e:
            logging.error(msg=f'Unable to generate Test Result file {e}')
            raise ReportError('Unable to generate Test Result file')

        return self.application_folder
