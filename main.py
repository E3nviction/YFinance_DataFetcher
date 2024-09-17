import yfinance as yf
from datetime import timedelta, datetime
import pytz

def get_earnings_dates(ticker):
    # Fetch the earnings dates using yfinance
    stock = yf.Ticker(ticker)
    earnings = stock.earnings_dates
    
    # Ensure the earnings dates are sorted in ascending order
    earnings = earnings.sort_index(ascending=True)
    
    # Get the index (which contains the dates)
    earnings_dates = earnings.index
    
    return earnings_dates

def get_price_on_date(ticker, date):
    stock = yf.Ticker(ticker)
    
    # Fetch historical price for the date
    price_data = stock.history(start=date, end=date + timedelta(days=1))
    
    if not price_data.empty:
        return price_data['Close'].iloc[0]
    else:
        return None  # If no data for that date

def is_future_date(date):
    # Convert date to naive datetime if it is timezone-aware
    if date.tzinfo is not None:
        date = date.tz_localize(None)
    
    # Compare with current naive datetime
    now = datetime.now()
    return date > now

def get_earnings_deltas(ticker):
    earnings_dates = get_earnings_dates(ticker)
    price_deltas = []
    
    # Calculate the differences between stock prices 2 days before consecutive earnings dates
    for i in range(1, len(earnings_dates)):
        previous_date = earnings_dates[i-1] - timedelta(days=2)
        current_date = earnings_dates[i] - timedelta(days=2)

        # Skip if the date is in the future
        if is_future_date(current_date):
            continue
        
        # Fetch prices for the adjusted dates
        previous_price = get_price_on_date(ticker, previous_date)
        current_price = get_price_on_date(ticker, current_date)
        
        if previous_price is not None and current_price is not None:
            # Calculate the price delta
            delta = current_price - previous_price
            price_deltas.append((previous_date, current_date, delta))
        else:
            price_deltas.append((previous_date, current_date, None))  # Handle missing data

    return price_deltas

# Example usage:
ticker = "AAPL"  # Replace with your desired ticker
deltas = get_earnings_deltas(ticker)
for prev_date, curr_date, delta in deltas:
    if delta is not None:
        print(f"Price delta from {prev_date} to {curr_date}: {delta}")
    else:
        print(f"Price data unavailable for {prev_date} or {curr_date}")
