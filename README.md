# pyhtmlreport

Often open source Test Automation projects lack a good reporting solution, pyhtmlreport solves that by creating HTML reports and represents the output as steps with screenshots.

### Requirements ###

* Requires Python 3.7 or higher.
* Access to Internet, materlizecss (https://materializecss.com/) is used to style the html report and accessed via cdn.

### How to Install ###

```
pip install pyhtmlreport
```

### Getting Started Guide ###

Once you have installed pyhtmlreport - how do you get started?
* Import the Report class and create a Report instance.
* Call the setup method.</br>
    **Parameters**
    * *Report Folder*: Root report folder to contain all test reports.
    * *Module Name*: Name of the application, a module within the application or a function.
    * *Release Name*: Application Release cycle.
    * *Maximum Screenshots*: By default, the number of screenshots for a Report instance is 1000. This parameter can be used to increase the number.
    * *Selenium Webdriver*: Screenshots are taken using the pillow library. If an instance of Selenium Webdriver is provided, the brower viewport is taken as screenshot using Selenium's save_screenshot method.
* Start writing to the test report by using the write_step method. The first step should have the **Start** status, it signals the start of a test to the report instance.</br>
    **Parameters**
    * *Step*: Description (Expected or Actual Step Description).
    * *Status*: Start, Pass, Fail and Warn.
    * *Screenshot*: Optional flag to capture screenshot for a step.
* Call the generate_report method at the end to generate the HTML report.

```python
from pyhtmlreport import Report
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys

report = Report()
driver = Chrome()

report.setup(
	report_folder=r'D:\Automation\Reports',
	module_name='Google',
	release_name='Release 1',
	selenium_driver=driver
)
driver.get('https://www.google.com/')

try:
    # Start of Test
    report.write_step(
    	'Testing Search functionality',
    	status=report.status.Start,
    	test_number=1
    )
    search_box = driver.find_element_by_css_selector('input[aria-label="Search"]')
    search_box.send_keys('pyhtmlreport is Awesome')
    search_box.send_keys(Keys.ENTER)

    # Test Steps
    results = driver.find_elements_by_css_selector('div[id="search"] div[class="g"]')
    assert len(results) > 1
    report.write_step(
    	'Google Search returned more than 1 results',
    	status=report.status.Pass,
    	screenshot=True
    )
except AssertionError:
    report.write_step(
        'Google Search did not return any result',
	 status=report.status.Fail,
	 screenshot=True
    )
except Exception as e:
    report.write_step(
        f'Something went wrong during execution!</br>{e}',
        status=report.status.Warn,
	screenshot=True
    )
finally:
    report.generate_report()
    driver.quit()
```
