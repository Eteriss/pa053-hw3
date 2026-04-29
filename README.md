# PA053 Homework 3 — REST Service
 
A simple REST service built with Flask and deployed on Vercel.
 
## Endpoints
 
The service accepts GET requests on `/` with exactly one of the following query parameters:
 
| Parameter | Description | Example |
|---|---|---|
| `queryAirportTemp` | Returns current temperature (°C) at the given IATA airport code | `?queryAirportTemp=PRG` |
| `queryStockPrice` | Returns current stock price for the given ticker symbol | `?queryStockPrice=AAPL` |
| `queryEval` | Evaluates an arithmetic expression (supports `+`, `-`, `*`, `/`, parentheses) | `?queryEval=10+(5*2)` |
 
## Response format
 
All responses are returned as `application/json` containing the numeric result.
 
## Data sources
 
- Airport coordinates: [airport-data.com](https://airport-data.com)
- Weather data: [Open-Meteo](https://open-meteo.com)
- Stock prices: [yfinance](https://github.com/ranaroussi/yfinance)
