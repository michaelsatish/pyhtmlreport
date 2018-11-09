# pyhtmlreport

Implement Html Reports in Test Automation. 


### Requirements ###

* Requires Python 3.7 or higher
* Access to Internet, materlizecss (https://materializecss.com/) is used to style the html report and accessed via cdn

## How to use ###

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
    print(len(results))
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

