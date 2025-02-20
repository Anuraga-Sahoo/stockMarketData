import nselib
from nselib import capital_market
import pandas as pd
import datetime


def get_stock_data(stock_symbol, start_date, end_date):
    try:
        # Fetch price-volume data for the stock symbol
        data = capital_market.price_volume_data(stock_symbol,start_date, end_date)
        
        # Convert the data into a Pandas DataFrame
        dataFrame = pd.DataFrame(data)
        
        # Select only the required columns
        required_columns = [
            'Symbol', 'Series', 'Date', 'PrevClose', 'OpenPrice', 
            'HighPrice', 'LowPrice', 'LastPrice', 'ClosePrice', 'AveragePrice'
        ]
        dataFrame = dataFrame[required_columns]
        
        # Convert 'Date' column to datetime format for better handling
        dataFrame['Date'] = pd.to_datetime(dataFrame['Date'])

        # convert dataframe to json data
        jsonData = dataFrame.to_json(orient='records')
        
        # Print the DataFrame
        print("Stock Data:")
        print(dataFrame)
        print(jsonData)
        
        # Return the DataFrame for further use
        return jsonData
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

# ======================= Index search ===================
def get_index_data(stock_symbol, start_date, end_date):
    try:
        # Fetch price-volume data for the stock symbol
        data = capital_market.index_data(stock_symbol,start_date, end_date )

        # convert the data into data frame
        dataFrame = pd.DataFrame(data)

        # select onlly the required columns
        required_columns = [
            'TIMESTAMP', 'INDEX_NAME',  'OPEN_INDEX_VAL',  'HIGH_INDEX_VAL',  'CLOSE_INDEX_VAL',  'LOW_INDEX_VAL',  'TRADED_QTY',  'TURN_OVER'
        ]
        dataFrame = dataFrame[required_columns]

        # convert dataframe to json data
        jsonData = dataFrame.to_json(orient='records')
        
        # Print the DataFrame
        print("Stock Data:")
        print(dataFrame)
        print(jsonData)
        
        return jsonData
        
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


# Example usage
if __name__ == "__main__":
    stock_symbol = 'SBIN'
    index_symbol = 'NIFTY IT' 
    start_date = '12-02-2025'
    end_date = '18-02-2025' 
    # stock_data = get_index_data(index_symbol, start_date , end_date)
    # index_data = get_stock_data(stock_symbol, start_date , end_date)
    
    # Accessing specific data from the DataFrame
    # if stock_data is not None:
    #     print("\nAccessing specific data:")
    #     print("Open Price:", stock_data['OpenPrice'].iloc[-1])
    #     print("Close Price:", stock_data['ClosePrice'].iloc[-1])
        




# =======================================

from flask import Flask, render_template, jsonify

app = Flask(__name__)
print(app)

@app.route('/stockapi')
def send_json():
    stock_data = get_index_data(index_symbol, start_date , end_date)
    return jsonify(stock_data)


@app.route('/indexapi')
def send_index_json():
     index_data = get_stock_data(stock_symbol, start_date , end_date)
     return jsonify(index_data)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)