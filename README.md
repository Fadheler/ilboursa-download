# ilboursa-download

ilBoursa allows downloading historical data but it is limited to 3 months date ranges.
This tool can be used to automate downloading data for any date range.
Data is downloaded in chunks until reaching the specified end date (today's date if not specified)

Requirements: python, pandas, selenium, chromedriver

Usage:
import ilboursa
ilboursa.quotes(ticker, start_date, end_date=datetime.strftime(datetime.now(), "%d/%m/%Y"), path=False)

Date format: DD/MM/YYYY

Installing chromedriver and selenium:
https://medium.com/@patrick.yoho11/installing-selenium-and-chromedriver-on-windows-e02202ac2b08
