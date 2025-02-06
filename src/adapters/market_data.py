import yfinance as yf
import requests

class MarketDataFetcher:
    def get_prices(self, tickers, dates):
        data = {}
        for t in tickers:
            try:
                data[t] = self._fetch_yahoo(t, dates)
            except:
                data[t] = self._fetch_alphavantage(t)
        return data
    
    def _fetch_yahoo(self, ticker, dates):
        return yf.Ticker(ticker).history(
            start=dates['start'],
            end=dates['end']
        )['Close'].values.tolist()
    
    def _fetch_alphavantage(self, ticker):
        
        API_KEY = "4AJTAJMPZJ0MHE7G" 
        response = requests.get(f"https://www.alphavantage.co/query?...{ticker}")
        print(response)
        return response.json()['Global Quote']['05. price']
