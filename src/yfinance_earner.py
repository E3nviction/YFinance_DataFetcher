import yfinance as YF
import pandas as pd

class Stock:
    """Stock class"""
    def __init__(self, ticker: str) -> None:
        self.ticker = ticker
        self.data = YF.Ticker(ticker)
    
    def set_ticker(self, ticker: str) -> None:
        """Sets ticker."""
        self.ticker = ticker
        self.data = YF.Ticker(ticker)
    
    def get_ticker(self) -> str:
        """Gets ticker."""
        return self.ticker

    def set_data(self, data: YF.Ticker) -> None:
        """Sets ticker data."""
        self.data = data

    def get_data(self) -> YF.Ticker:
        """Gets ticker data."""
        return self.data

    def get_ticker_info(self) -> dict:
        """Gets ticker information."""
        return self.get_data().info

    def get_historical_data(self, period: str='1mo', interval: str='1d') -> pd.DataFrame:
        """Gets historical data for a ticker."""
        historical_data = self.get_data().history(period=period, interval=interval)
        return historical_data

    def get_earnings(self) -> pd.DataFrame:
        """Gets earnings for a ticker."""
        # Access the financials data correctly
        earnings_data = self.get_data().financials.loc['Net Income']
        return earnings_data

    def get_historical_earnings(self, period='1mo', interval='1d') -> pd.DataFrame:
        """Gets historical earnings for a ticker."""
        """
        Historical earnings aren't directly available from stock price history. 
        We retrieve the historical stock price and estimate the corresponding financials 
        (income) over those periods based on available financial reports.
        """
        # Fetch historical stock price data over the specified period and interval
        historical_data = self.get_historical_data(period=period, interval=interval)
        
        # Fetch the earnings (Net Income) over the most recent reporting periods
        earnings_data = self.get_data().financials.loc['Net Income']
        
        # Match historical periods with earnings reporting dates
        earnings_over_time = pd.DataFrame()
        for date in earnings_data.index:
            if date in historical_data.index:
                earnings_over_time = earnings_over_time.append({
                    'Date': date,
                    'Net Income': earnings_data[date],
                    'Close Price': historical_data.loc[date]['Close']
                }, ignore_index=True)
        
        return earnings_over_time

def get_ticker_info(ticker: str) -> dict:
    """Gets ticker information."""
    return Stock(ticker).get_ticker_info()

def get_data(ticker: str) -> pd.DataFrame:
    """Gets data for a ticker."""
    return Stock(ticker).get_data()

def get_historical_data(ticker: str, period='1mo', interval='1d') -> pd.DataFrame:
    """Gets historical data for a ticker."""
    return Stock(ticker).get_historical_data(period=period, interval=interval)

def get_earnings(ticker: str) -> pd.DataFrame:
    """Gets earnings for a ticker."""
    return Stock(ticker).get_earnings()

def get_historical_earnings(ticker: str, period='1mo', interval='1d') -> pd.DataFrame:
    """Gets historical earnings for a ticker."""
    return Stock(ticker).get_historical_earnings(period=period, interval=interval)