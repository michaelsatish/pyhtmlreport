# pyhtmlreport
A python library to implement HTML Reports. 

Automation testing projects using selenium webdriver rely on third party API's to generate reports. 
This API tries to solve the need for automation test report with detailed  

Requires Python 3.6.5 or higher

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

