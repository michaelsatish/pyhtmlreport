# pyhtmlreport

Implement Html Reports in Test Automation. 


# Requirements

Requires Python 3.7 or higher
Access to Internet, materlizecss is used to style the html report and accessed via cdn
https://materializecss.com/

## How to use:

```
from selenium.webdriver import Chrome
from pyhtmlreport import Report

driver = Chrome('path to chromedriver')
driver.get('https://www.google.com/')

report = Report()
report.setup('C:\Automation\Reports', application_name='Google Search', release_name='Test Release')

# Mandatory, report.status.Start signals the start of the Test Run
report.write_step('Testing Search functionality', status=report.status.Start)
driver.find_element_by_id('lst-ib').send_keys('Python is Awesome')
driver.find_element_by_css_selector('input[value="Google Search"]').click()

try:
    results = driver.find_elements_by_tag_name('a')
    assert len(results) > 1
    report.write_step('More than 1 result as expected', status=report.status.Pass, screenshot=True)
except AssertionError:
    report.write_step('No results', status=report.status.Fail, screenshot=True)
except Exception as e:
    print(e)
    report.write_step('Something went wrong during execution!', status=report.status.Warn, screenshot=True)
finally:
    report.generate_report()
    driver.quit()
```

