from pathlib import Path
from collections import namedtuple
from typing import Union, TypeVar

from jinja2 import Environment, FileSystemLoader


WebDriver = TypeVar('WebDriver')

# Step represents a test case actual step.
Step = namedtuple('Step', ('description', 'screenshot'))


class Test:
    """Test object."""

    def __init__(
        self,
        identifier: str,
        id: Union[int, str],
        driver: Union[None, WebDriver]
    ) -> None:
        """Test represents a test case."""
        self.identifier = identifier
        self.id = id
        self.description = None

        self.setup_status = None
        self.call_status = None
        self.teardown_status = None

        self.driver = driver
        self.steps = []

    def add_step(self, description: str, screenshot: bool = False) -> None:
        """Add the new step to test."""
        final_screenshot = None

        # Use selenium webdriver object to take screenshot of browser viewport.
        if screenshot and (ss_method := getattr(self.driver, 'get_screenshot_as_base64', None):
            final_screenshot = ss_method()

        self.steps.append(Step(description, final_screenshot))


class Report:
    """Report object."""

    def __init__(self) -> None:
        self.path = None
        self.filename = None
        self.tests = dict()

        self.jinja_env = Environment(
            loader=FileSystemLoader(
                searchpath=Path(__file__).parents[1] / 'templates'
            )
        )
        self.report_template = self.env.get_template('report.html')

    def append_test(self, test: Test) -> None:
        """Add test to tests."""
        self.tests[test.identifier] = test

    def get_test(self, identifier: str) -> Union[None, Test]:
        """Get the test object from tests."""
        return self.tests.get(identifier, None)

    def create_report(self):
        pass
