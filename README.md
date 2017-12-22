# pyhtmlreport
A python library to implement html test reporting. 

Automation testing projects using selenium webdriver rely on third party API's to generate reports. 
This API tries to solve the need for test report with test steps and overall test status

How to use:

from pyhtmlreport import Report

report = Report()


report.setup('C:\Automation Test\Reports, 'Login', 'Wave 1')  

report.write_step('Testing login functionality', report.status.Start)

report.write_step('Step1: Login Success', report.status.Pass)

report.write_step('Step2: Login Failure', report.status.Fail, screenshot=True)

report.write_step('Step3: Login Warning', report.status.Warn)

report.generate_report()
