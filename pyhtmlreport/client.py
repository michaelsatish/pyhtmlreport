"""
Copyright (C) 2017 Satish Kumar Kadarkarai Mani

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import datetime
import logging
import pkg_resources

from PIL import ImageGrab

from pyhtmlreport.utils import render_pie_chart, render_overall_status_table


MAX_SCREENSHOTS = 1000


class ReportError(Exception):
    pass


def dispatch_screenshot_number():
    """
    File name for screenshots:
    generator to yield a number from 0 to arg: MAX_SCREENSHOTS
    by default its 1000, if more than 1000 numbers are yielded contrasting to number of screenshots,
    StopIteration exception will be thrown.

    :return: generator
    """
    for x in list(range(MAX_SCREENSHOTS)):
        yield x


def update_test_status(p, f, w):
    """
    To update total passed, failed and warning tests
    called before every test to update status of completed test, and called in function generate_report to update the
    status of final test

    if one or more fail steps, test is marked as failed
    if one or more warn steps and no fail steps, test is maked as warning
    if one or more pass steps and no fail or warn steps, test is marked as passed

    :param p: number of pass steps in a test
    :param f: number of fail steps in a test
    :param w: number of warn steps in a test
    :return: list unpacked in function update_test_status to update total passed, failed and warning tests
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

        self.root_report_folder = None
        self.module_folder = None
        self.capture_folder = None

        self.module_name = None
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

    def setup(self, root_report_folder, module_name='default', release_name='default', selenium_driver=None):
        """
        Setup followed by initialization of Report class to create report folders
        :param root_report_folder:
        :param module_name:
        :param release_name:
        :param selenium_driver: pass the initialized webdriver to use the method save_screenshot for screenshots
        :return:
        """
        if not root_report_folder:
            raise ReportError('Require Report Root Folder path')

        if module_name == 'default':
            import warnings
            warnings.warn('Module name set to default')

        self.root_report_folder = root_report_folder
        self.module_name = module_name
        self.release_name = release_name

        self.module_folder = os.path.join(self.root_report_folder,
                                          '{name} {date}'.format(name=self.module_name,
                                                                 date=datetime.datetime.now().strftime('%m_%d_%Y '
                                                                                                       '%H_%M_%S')))
        self.capture_folder = os.path.join(self.module_folder, 'Capture')
        self.selenium_driver = selenium_driver

        if not os.path.exists(self.root_report_folder):
            os.mkdir(self.root_report_folder)

        if not os.path.exists(self.module_folder):
            os.mkdir(self.module_folder)

        if not os.path.exists(self.capture_folder):
            os.mkdir(self.capture_folder)

    def __repr__(self):
        return 'Report(module_name=%s, release_name=%s)' % (self.module_name, self.release_name)

    def capture_screenshot(self):
        """
        Capture screenshot of default monitor view
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
            logging.log(40, str(e))

    def update_test_status(self):
        if all(not x for x in [self.total_tests, self.pass_step, self.fail_step, self.warn_step]):
            return

        if all(x == 0 for x in [self.total_tests, self.pass_step, self.fail_step, self.warn_step]):
            return

        status = update_test_status(self.pass_step, self.fail_step, self.warn_step)

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
            with open(os.path.join(self.module_folder, 'Report.html'), 'w') as f:
                d = {
                    'module_name': self.module_name,
                    'release_name': self.release_name,
                    'date': datetime.datetime.now().strftime('%m_%d_%Y'),
                    'result': self.step,
                    'overall_status': render_overall_status_table(self.total_tests, self.passed_tests,
                                                                  self.failed_tests, self.warning_tests),
                    'pie_chart': render_pie_chart(self.passed_tests, self.failed_tests, self.warning_tests)
                }
                f.write(self.html.format(**d))
        except Exception as e:
            logging.log(40, str(e))
            raise ReportError('Unable to generate Test Result file')

        return self.module_folder
