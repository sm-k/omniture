python sdk for adobe analytics api (reporting-api-1.4)

The below is an example how to authenticate to the API and to request a sample report

# Example

```python
import omniture

# get an api by submitting an aspen request
credentials = {
	'username':'stephen.knoth@adidas.com:Adidas', 
	'password': 'api_key'
}

# Create the omniture object
om = omniture.Omniture(
	company='Adidas', 
	user=credentials['username'], 
	password=credentials['password']
)

'''
This is the 'adidas - U.S' report suite, however, you can get all of the report suites
by accessing the `om.report_suite` class
'''
suite = 'ag-adi-us-prod'


report = om.report

# The below report will give you a count of orders by day.
description = omniture.data.ReportDescription(
	rsid=suite,
	date_from='2020-09-01',
	date_to='2020-09-30',
	date_granularity='day',
	metrics=[
		omniture.data.ReportDescriptionMetric(
			metric_id='orders'
		)
	]
)

# When you queue a report to be run, it returns the queued report ID.
report_id = report.queue(
	report_description=description
)

# Because the reports are executed in a queue, you can continuously poll the report status until it returns data
while True:
	try:
		report_data = report.get(
			report_id=report_id
		)
		
		# Do something with `report_data`
		
		break
	except Exception as e:
		# Assuming your above code doesn't throw an error this will return 'report not ready'
		print(e)
```