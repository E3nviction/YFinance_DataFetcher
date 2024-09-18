# YFinance_DataFetcher

This Python script retrieves historical earnings dates and calculates stock price changes (deltas) between consecutive earnings reports for a given stock ticker symbol using the `yfinance` library. It also handles timezone conversions, future date checks, and missing data.

## Prerequisites

Before running the script, ensure that you have the following Python packages installed:

- `yfinance`: For retrieving stock data.
- `pytz`: For handling timezone-aware dates.

Install the required packages using pip:

```bash
pip install yfinance pytz
```

## Script Overview

### Functions

1. **`get_earnings_dates(ticker)`**
   - Retrieves all earnings dates for a specific stock ticker using `yfinance`.
   - Returns: A list of sorted earnings dates in ascending order.

2. **`get_price_on_date(ticker, date)`**
   - Fetches the closing stock price for the given ticker on the specified date.
   - Returns: The stock price if available, otherwise `None`.

3. **`is_future_date(date)`**
   - Checks whether a given date is in the future compared to the current date.
   - Returns: `True` if the date is in the future, otherwise `False`.

4. **`get_earnings_deltas(ticker)`**
   - Calculates the percentage change (delta) in stock price between consecutive earnings reports.
   - Skips future dates and handles missing price data.
   - Returns: A list of tuples, each containing the previous date, current date, and the percentage delta in price.

### Usage

The script can be run as is, with a specific ticker symbol hardcoded (e.g., `"TSLA"`). It calculates and prints the price deltas for the stock around each earnings report:

```python
ticker = "TSLA"
deltas = get_earnings_deltas(ticker)
for prev_date, curr_date, delta in deltas:
    if delta is not None:
        print(f"Price delta from {prev_date} to {curr_date}: {abs(delta)}%")
    else:
        print(f"Price data unavailable for {prev_date} or {curr_date}")
```

### Example Output

```
Price delta from 2022-01-24 to 2022-04-25: 3.45%
Price data unavailable for 2023-01-22 or 2023-04-24
...
```

## Limitations

- This script assumes that historical price data is available for each earnings date.
- If a stock has missing price data around earnings dates, the delta for those dates will be reported as `None`.
- Future earnings dates are automatically skipped.
