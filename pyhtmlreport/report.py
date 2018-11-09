import logging
import os
from dataclasses import dataclass, field
from datetime import datetime
from shutil import copy2
from typing import Generator, List, Optional

from jinja2 import Environment, FileSystemLoader
from PIL import ImageGrab

logger = logging.getLogger(__name__)


class ReportError(Exception):
    pass


def dispatch_screenshot_number(max_ss: int) -> Generator[int, None, None]:
    """
    File name for screenshots
    Generator to yield a number from 0 to arg: max_ss

    To govern the no of screenshots for a run
    :return: generator
    """
    for x in list(range(max_ss)):
        yield x


class Status:
    Start: str = 'Start'
    Pass: str = 'Pass'
    Fail: str = 'Fail'
    Warn: str = 'Warn'
    Highlight: str = 'Highlight'


@dataclass
class Step:
    description: str
    status: str
    screenshot: Optional[str]


@dataclass
class Test:
    number: int
    description: str
    status: str = field(default=None)
    steps: List[Step] = field(default_factory=list)


class Tests(list):
    """
    If one or more fail steps, test is marked as failed
    If one or more warn steps and no fail steps,test is maked as warning
    If one or more pass steps and no fail/warn steps, test is marked as passed
    """

    def append(self, test):
        if not isinstance(test, Test):
            raise TypeError(f'{test} is not of type Test')

        statues = [step.status for step in test.steps]
        pass_ = statues.count('Pass')
        fail = statues.count('Fail')
        warn = statues.count('Warn')

        if fail >= 1:
            test.status = 'Fail'

        if warn >= 1 and fail == 0:
            test.status = 'Warn'

        if pass_ >= 1 and fail == 0 and warn == 0:
            test.status = 'Pass'

        super(Tests, self).append(test)


class Report:

    def __init__(self):

        self.report_folder = None
        self.module_folder = None
        self.screenshots_folder = None

        self.module_name = None
        self.release_name = None

        self.max_screenshots = 1000
        self.selenium_driver = None

        self.env = Environment(
            loader=FileSystemLoader(
                searchpath=os.path.join(__file__, '../templates')
            )
        )
        self.report_template = self.env.get_template('report.html')

        self.tests = Tests()
        self.test = None
        self.attachments = []
        self.screenshot = None

        self.status = Status
        self.screenshot_num = dispatch_screenshot_number(self.max_screenshots)

    def setup(
        self,
        report_folder,
        module_name='default',
        release_name='default',
        max_screenshots=None,
        selenium_driver=None
    ):
        """
        This method should follow Report Class Initialization
        :param report_folder: Report folder (Root) Path
        :param module_name: Module/Application/Function Name
        :param release_name: Release Name
        :param selenium_driver: Selenium Webdriver Instance
        :return:
        """
        if not report_folder:
            raise ReportError('Report Folder Path Required')

        if module_name == 'default':
            import warnings
            warnings.warn('Module name set to default')

        if release_name == 'default':
            import warnings
            warnings.warn('Release name set to default')

        if max_screenshots:
            self.max_screenshots = max_screenshots
        self.selenium_driver = selenium_driver

        self.report_folder = report_folder
        self.module_name = module_name
        self.release_name = release_name

        self.module_folder = os.path.join(
            self.report_folder,
            '{name} {date}'.format(
                name=self.module_name,
                date=datetime.now().strftime('%m_%d_%Y %H_%M_%S')
                )
            )

        self.screenshots_folder = os.path.join(
            self.module_folder, 'Screenshots'
        )

        if not os.path.exists(self.report_folder):
            os.mkdir(self.report_folder)

        if not os.path.exists(self.module_folder):
            os.mkdir(self.module_folder)

        if not os.path.exists(self.screenshots_folder):
            os.mkdir(self.screenshots_folder)

    def __repr__(self):
        return 'Report(Module=%s, Release=%s)' % (
            self.module_name,
            self.release_name
        )

    def capture_screenshot(self):
        """
        Capture screenshot
        If selenium_driver, screenshot of the browser view port is captured
        """
        current_screenshot_num = str(next(self.screenshot_num))
        current_screenshot = os.path.join(
            self.screenshots_folder,
            current_screenshot_num + '.png'
        )

        if self.selenium_driver:
            self.selenium_driver.save_screenshot(current_screenshot)
        else:
            ImageGrab.grab().save(current_screenshot)

        return current_screenshot_num

    def write_step(self, step, status, test_number=None, *, screenshot=False):
        if screenshot:
            self.screenshot = self.capture_screenshot()
        else:
            self.screenshot = None

        if status == 'Start':
            if not test_number:
                raise ReportError('Test Number Required with Start Status')

            if not self.test:
                self.test = Test(test_number, step)
            else:
                self.tests.append(self.test)
                self.test = Test(test_number, step)

        elif status in ['Pass', 'Fail', 'Warn', 'Highlight']:
            if not self.test:
                raise ReportError(
                    'Start step missing, please call Start status first'
                )
            self.test.steps.append(Step(step, status, self.screenshot))

        else:
            raise ReportError('Invalid Status')

    def add_attachment(self, attachment):
        if not os.path.isfile(attachment):
            raise ReportError(f'{attachment} is not of type file')
        self.attachments.append(attachment)

    def generate_report(self):
        # Generate the Automation Report
        self.tests.append(self.test)

        if self.attachments:
            attachments_folder = os.path.join(
                self.module_folder,
                'Attachments'
            )
            if not os.path.exists(attachments_folder):
                os.mkdir(attachments_folder)

            for attachment in self.attachments:
                copy2(attachment, attachments_folder)

        total_tests = len(self.tests)
        passed_tests = len([
            test for test in self.tests if test.status == 'Pass']
        )
        failed_tests = len(
            [test for test in self.tests if test.status == 'Fail']
        )
        warning_tests = len(
            [test for test in self.tests if test.status == 'Warn']
        )

        report_output = self.report_template.render(
            module_name=self.module_name,
            release_name=self.release_name,
            run_date=datetime.now().strftime('%m:%d:%Y'),
            total_tests=total_tests,
            passed_tests=passed_tests,
            failed_tests=failed_tests,
            warning_tests=warning_tests,
            tests=self.tests
        )
        with open(os.path.join(self.module_folder, 'Report.html'), 'w') as f:
            f.write(report_output)
