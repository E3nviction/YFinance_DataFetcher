from src import *

def write_to_csv(data, filename):
    with open(filename, 'w') as f:
        f.write(data)

write_to_csv(get_earnings('AAPL').to_csv(), 'output/AAPL.csv')