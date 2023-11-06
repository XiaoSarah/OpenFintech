from collections import deque 

# NOTE: The data structures below are i.e. a replacement to having the database
class Candle:
    def __init__(self):
        return
    
class CandleContainer: 
    def __init__(self):
        return
    
class FinancialInstrument:
    def __init__(self):
        return

# NOTE: The class below was previously a static method within the Alphavantage API wrapper
class Indicator:
    def __init__(self):
        return

# NOTE: This class was previously a part of the API wrapper
class DataAcquisition: 
    def __init__(self):
        return
    
    def _request(): # Could use an internal request method that simplifies things (check out the old Alphavantage wrapper code)
        return

    def requestDataFromAPI(self, ticker, interval, outputsize='full'): # declare return type, parameters should be for our functionality
        params = {
            'function': 'TIMESERIES' + interval.upper(),
            'symbol': ticker,
            'apikey': self.key,
            'outputsize': outputsize
        }
        response = requests.get(url=f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval={interval}min&apikey={self.key}", params=params)
        response.raise_for_status()
        return response.json()
    
    def convertDataToCandleContainer(self): # return type is a candle container
        return