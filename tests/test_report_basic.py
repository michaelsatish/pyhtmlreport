import types

import pytest
from jinja2 import Template
from pyhtmlreport import Report
from pyhtmlreport.report import Step, Test, Tests, dispatch_screenshot_number


def test_dispatch_screenshot_number_return_type():
    assert isinstance(dispatch_screenshot_number(1000), types.GeneratorType)


def test_screenshot_num():
    r = Report()
    assert isinstance(r.screenshot_num, types.GeneratorType)
    assert 0 == next(r.screenshot_num)
    assert 1 == next(r.screenshot_num)


def test_template_type():
    r = Report()
    assert isinstance(r.report_template, Template)


def test_type_error():
    with pytest.raises(TypeError):
        ts = Tests()
        ts.append('this is not a test type')


def test_append():
    t = Test(1, 'This is a Test')
    ts = Tests()
    ts.append(t)
    assert len(ts) == 1


def test_pass_status():
    step1 = Step('This is Step1', 'Pass', None)
    step2 = Step('This is Step2', 'Pass', None)
    step3 = Step('This is Step2', 'Pass', None)

    t = Test(1, 'This is a Test')
    t.steps.append(step1)
    t.steps.append(step2)
    t.steps.append(step3)

    ts = Tests()
    ts.append(t)
    tr = ts[0]
    assert tr.status == 'Pass'


def test_fail_status():
    step1 = Step('This is Step1', 'Pass', None)
    step2 = Step('This is Step2', 'Fail', None)
    step3 = Step('This is Step2', 'Warn', None)

    t = Test(1, 'This is a Test')
    t.steps.append(step1)
    t.steps.append(step2)
    t.steps.append(step3)

    ts = Tests()
    ts.append(t)
    tr = ts[0]
    assert tr.status == 'Fail'


def test_warn_status():
    step1 = Step('This is Step1', 'Pass', None)
    step2 = Step('This is Step2', 'Pass', None)
    step3 = Step('This is Step2', 'Warn', None)

    t = Test(1, 'This is a Test')
    t.steps.append(step1)
    t.steps.append(step2)
    t.steps.append(step3)

    ts = Tests()
    ts.append(t)
    tr = ts[0]
    assert tr.status == 'Warn'
