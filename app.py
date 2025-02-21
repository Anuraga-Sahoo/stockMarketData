import nselib
from nselib import capital_market
import pandas as pd
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def get_index_data(index_symbol, start_date, end_date):
    try: 
        data = capital_market.index_data(index_symbol, start_date, end_date)
        data_frame = pd.DataFrame(data)
        
        required_columns = [
            'TIMESTAMP', 'INDEX_NAME', 'OPEN_INDEX_VAL', 'HIGH_INDEX_VAL',
            'CLOSE_INDEX_VAL', 'LOW_INDEX_VAL', 'TRADED_QTY', 'TURN_OVER'
        ]
        data_frame = data_frame[required_columns]
        # data_frame['TIMESTAMP'] = pd.to_datetime(data_frame['TIMESTAMP'])
        
        print("data frame ======= ",data_frame.to_dict(orient='records'))
        return data_frame.to_dict(orient='records')
        
    except Exception as e:
        print(f"Error fetching index data: {e}")
        return []

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/index')
def handle_index():
    indexsymbol = request.args.get('symbol')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not all([indexsymbol, start_date, end_date]):
        return jsonify({'error': 'Missing required parameters: symbol, start_date, end_date'}), 400
    
    data = get_index_data(indexsymbol, start_date, end_date)
    
    return jsonify(data) if data else jsonify({'error': 'Failed to fetch index data'}) , 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)