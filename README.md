# ilboursa-download

ilBoursa allows you to download historical data but it is limited to 3 months date ranges.
This tool can be used to automate downloading data for longer data ranges.
Data is downloaded in chunks until reaching the specified end date (today's date if not specified)

Requirements: python3, pandas, selenium, chromedriver

https://medium.com/@patrick.yoho11/installing-selenium-and-chromedriver-on-windows-e02202ac2b08

Usage:

ilboursa.py TICKER START_DATE

ilboursa.py TICKER START_DATE END_DATE

Date format: DD/MM/YYYY
