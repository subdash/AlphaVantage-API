# AlphaVantage API Microservice
### The goal here was to create a microservice for the [AlphaVantage API](https://www.alphavantage.co/documentation/) which provides data on stocks that can be used for data-oriented analysis as well as visual analysis of stock data.
### This project demonstrates creating a Python interface for a web API as well as some simple SQL integration for caching.

### Discussion
#### 1. Microservice vs. AlphaVantage API
#### There is a single endpoint for the AlphaVantage API which accepts various query parameters, one of which is always FUNCTION, so it works more like an RPC API than a REST one.
#### So you may be wondering, what does this microservice provide that the API itself does not?
#### Well, it provides code completion when writing queries in an IDE, validation of query params, and caching.
#### What is missing from this microservice? Well, not every single function has been implemented, mostly just the ones that are flagged as "high usage" on the API documentation.
#### 2. Caching
#### The caching mechanism here is very simple. The service only has one function: `get`. Three things can happen when this function is called:
#### - If the url has never been queried before, a new entry is made in the cache table
#### - If it has been queried before and was cached recently, the data will be returned from the cache
#### - If it has been queried before but was not cached recently, the entry in the cache is updated
#### As you can see the cache performs simple CRUD operations to reduce the number requests to the AlphaVantage API.
### Usage
#### This microservice can be used in the Python shell, in scripts, and as a module for a larger application. There is a short example script below.
```python
#!/usr/bin/env python3
# Script example
API_KEY = os.environ["API_KEY"]
service = AlphaVantageService()
ticker = "RPM"
earnings_history_payload = {
    "function": AVFunction.EARNINGS,
    "symbol": ticker,
    "apikey": API_KEY
}
res = service.get(earnings_history_payload)
print(res)
""""
Output:
{
  "symbol": "RPM",
  "annualEarnings": [
    {
      "fiscalDateEnding": "2021-02-28",
      "reportedEPS": "2.88"
    },
    ...
  ],
  "quarterlyEarnings": [
    {
      "fiscalDateEnding": "2021-02-28",
      "reportedDate": "2021-04-07",
      "reportedEPS": "0.38",
      "estimatedEPS": "0.2907",
      "surprise": "0.0893",
      "surprisePercentage": "30.719"
    },
    ...
  ]
}"""
```
An example of using this module for visual stock analysis in the Python shell (reference `tools/compare_earnings.py`):
```
$ ./src/tools.py -k $(cat api_key) -t EBF --cmpearnings
Ticker: EBF
Earnings will be announced: 2021-04-19
Earnings information for last 4 quarters:
===========================================
	yearly EPS average: 0.27
===========================================
	reportedDate: 2020-12-20
	reportedEPS: 0.32
	surprisePercentage: 14.2857
===========================================
	reportedDate: 2020-09-21
	reportedEPS: 0.25
	surprisePercentage: 13.6364
===========================================
	reportedDate: 2020-06-22
	reportedEPS: 0.16
	surprisePercentage: 33.3333
===========================================
	reportedDate: 2020-04-20
	reportedEPS: 0.33
	surprisePercentage: -5.7143

Next quarter expected earnings:
	0.27
Expected earnings / last quarter earnings:
	0.84
Expected earnings / last year avg. earnings:
	1.02
```

### Improvements
#### This project could be improved in many ways. The cache database schema is inefficient and does not use relations between tables as you normally would with a relational database. 
#### More tools could be added for analysis, and converting the JSON data into stock charts would make this a lot more useful.
#### Support for different types of SQL databases would be a nice addition: the service could accept a config file for your local SQL database.
#### Unit tests could (honestly, *should*) be added.
