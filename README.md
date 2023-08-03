# ilboursa-download

IlBoursa allows you to download historical data but it is limited to 3 months date ranges.
This tool can be used to automate data download for longer data ranges.
It downloads the data in chunks and merges all into a single file.

Requirements: python3, pandas, selenium, chromedriver
https://medium.com/@patrick.yoho11/installing-selenium-and-chromedriver-on-windows-e02202ac2b08

Usage:

ilboursa.py TICKER START_DATE

ilboursa.py TICKER START_DATE END_DATE

Date format: DD/MM/YYYY
