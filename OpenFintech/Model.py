from .Databases import MySQL
from .APIs import Alphavantage
from . import queries
import copy

# TODO:
# Configuration CRUD functions
# Implement test_config based on the provided notes
# Implement the __str__ function

class Model:
    def __init__(self, database, market):
        self.db_handler = database
        self.market_handler = market
        return
    
    def create(self, values:dict)->int:
        # Convert the dictionary of values given by the user (which can be variable) into a set for inserting into the database
        ma_1, ma_2, ema_1, ema_2, rsi_1, rsi_2 = 0,0,0,0,0,0
        keys = values.keys()
        if "EMA" in keys:
            ema_1=values["EMA"][0]
            if len(values["EMA"])>1: ema_2=values["EMA"][1]
        if "SMA" in keys:
            ma_1=values["SMA"][0]
            if len(values["SMA"])>1: ma_2=values["SMA"][1]
        if "RSI" in keys:
            rsi_1=values["RSI"][0]
            if len(values["RSI"])>1: rsi_2=values["RSI"][1]
        values = (values["user_id"],ma_1, ma_2, ema_1, ema_2, rsi_1, rsi_2)

        # Execute MySQL statement to insert the configuration values into the AWS RDS
        self.db_handler.execute(queries.insert_configuration_entry, values)
        query_last = "SELECT LAST_INSERT_ID();"
        config_id = self.db_handler.execute(query_last, query=True)[0][0]

        return config_id

    def createSetting(self,values:dict):
        # Convert values dict to a set
        values=(values["user_id"],values["config_id"],values["equity_id"],
                                            values["stop_loss"],values["starting_aum"],values["take_profit"],
                                            values["chart_freq_mins"])
        self.db_handler.execute(queries.insert_setting_entry, values)
        query_last = "SELECT LAST_INSERT_ID();"
        config_id = self.db_handler.execute(query_last, query=True)[0][0]
        return config_id

    # The testing and running of configuation relies on the Market model.
    def backtest(self, setting_values:dict, config_values:dict, api_handler:Alphavantage) -> dict:
        print("\nModel.backtest():")

        # Create the configuration entry using this objects method
        config_id = self.create(config_values)
        
        # Add the config_id to the setting (since these values will be passed onto the database)
        setting_values["config_id"] = config_id 

        # Get the equity_id for the given ticker from db
        ticker = setting_values.pop("ticker") # Remove ticker from the setting_values dict
        response = api_handler.overview(ticker) # Retrive its last appropriate entry from the db (or request data from Alphavantage and create entry in DB)
        setting_values["equity_id"] = response[0] # Add the equity_id to the setting_values dict
        
        # Create a entry to the settings table
        setting_id = self.createSetting(setting_values)
        print(f"\tCreated setting with the ID {setting_id}")
        

        # Import the data for given the setting using the given api_handler (Alphavantage object)
        df = api_handler.equity_intraday(api_handler.key,ticker,interval=setting_values["chart_freq_mins"])
        print("\tPrice Data:")
        print(df)

        # Modify the price_data_df based on the given config values indicators section
        indicators = copy.deepcopy(config_values)
        del indicators["user_id"]
        df = api_handler.technical_indicator(indicators,df).dropna()
        print("After manipulating the dataframe with technical_indicator() method:")
        print(df)
        
        # NOTE: Static implementation. TODO: Needs to be made dynamic so that it can work with any of the given settings
        # Iterate over the dataframe
        signals_count = 0
        for i, r in df.iloc[1:].iterrows():

            # Conditions for buying/opening a new trade
            if r["EMA_5"] > r["SMA_10"] and df['EMA_5'][i-1] < df['SMA_10'][i-1]: # If "short term trend" dips above long term trend (indicating a dip above the mean) (dip is only when previous wasnt already above)
                
                # TODO: Check for false signals using social media sentiment analysis etc.
                signals_count+=1
                print("Buy",i,r)
                # Open a position with all the AUM (calculate the quantity and create a trade entry)

            # If sell by natural condition, clear the quantities at the current close price and update the balance (create a trade entry)
            
            # If hold (bought and in the trading range) (NOTE: can be linked back with line 87's second half):
                # Check for stop loss or take profit conditions to exit trades

                
        print("Total buy signals generated:", signals_count)

        #df.to_csv("sample_model_data.csv", encoding='utf-8') 
        # Check test.py for the implementation

        # Calculate performance data and create performance entry
        return
    
    def simulate(self): # NOTE: We can worry about this after we build backtest
        # Similar to “test_configuration” but for real-time (simulated market) testing. 
        # This would use realtime price data which would be added to (or retrived from) the appropriate collection or database or dataframe in market
        # It would perform the required calculations based on the confiurations
        
        # Realtime (simualted) testing code here

        # This would take a setting and a configuration as well
        # It should output performance and market data (including price data) as pandas df or a list of dictionaries?
        return

    # Prints the market overview specific to the model and configurations. (can use SQL complex queries and create visualizations now)
    def __str__(self):
        return("working")