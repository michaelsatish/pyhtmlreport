import types

import pytest

from pyhtmlreport import Report
from pyhtmlreport.client import dispatch_screenshot_number, update_test_status


def test_dispatch_screenshot_number_return_type():
    assert isinstance(dispatch_screenshot_number(), types.GeneratorType)


def test_update_test_status_failed():
    assert [0, 1, 0] == update_test_status(0, 1, 0)
    assert [0, 1, 0] == update_test_status(1, 1, 0)
    assert [0, 1, 0] == update_test_status(0, 1, 1)
    assert [0, 1, 0] == update_test_status(1, 1, 1)
    assert [0, 1, 0] == update_test_status(2, 2, 2)


def test_update_test_status_warning():
    assert [0, 0, 1] == update_test_status(0, 0, 1)
    assert [0, 0, 1] == update_test_status(1, 0, 1)
    assert [0, 0, 1] == update_test_status(0, 0, 2)
    assert [0, 0, 1] == update_test_status(2, 0, 2)
    assert [0, 0, 1] != update_test_status(1, 1, 1)


def test_update_test_status_passed():
    assert [1, 0, 0] == update_test_status(1, 0, 0)
    assert [1, 0, 0] == update_test_status(2, 0, 0)
    assert [1, 0, 0] == update_test_status(3, 0, 0)
    assert [1, 0, 0] != update_test_status(3, 0, 1)
    assert [1, 0, 0] != update_test_status(3, 1, 0)


def test_screenshot_num():
    r = Report()
    assert isinstance(r.screenshot_num, types.GeneratorType)
    assert 0 == next(r.screenshot_num)
    assert 1 == next(r.screenshot_num)


def test_html():
    r = Report()
    assert isinstance(r.html, str)


def test_selenium_webdriver_plug():
    r = Report()
    assert not r.selenium_driver


if __name__ == '__main__':
    pytest.main()
