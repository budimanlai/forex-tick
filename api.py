import pandas as pd
from sqlalchemy import create_engine
from flask import Flask, jsonify, send_from_directory
import os

# --- KONFIGURASI DATABASE (GANTI DENGAN KREDENSIAL ANDA) ---
DB_USER = "postgres"
DB_PASSWORD = "12345678"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "forex"
DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
ENGINE = create_engine(DB_URL)

# --- QUERY DATA DARI DATABASE ---

# SYMBOL = 'XAUUSD'
# TIMEFRAME = 'H4' # Ubah Timeframe sesuai yang ingin ditampilkan
LIMIT = 500 # Batasi jumlah baris untuk tampilan cepat

def fetch_data_from_db(symbol, timeframe):
    query = f"""
    SELECT 
        timestamp, "open", high, low, "close", tick_volume, spread 
    FROM 
        ohlcv_data 
    WHERE 
        symbol = '{symbol}' AND timeframe = '{timeframe}'
    ORDER BY 
        timestamp DESC 
    LIMIT {LIMIT};
    """

    # Mengambil data menggunakan Pandas
    try:
        # Jangan jadikan timestamp sebagai index, biarkan sebagai kolom biasa
        df = pd.read_sql(query, ENGINE)
        # Data MT5 biasanya diurutkan dari yang terbaru ke yang terlama. Kita balikkan (sortir ascending)
        df = df.sort_values('timestamp')
        
        # Pastikan nama kolom sesuai ekspektasi (timestamp tetap sebagai kolom)
        df.columns = ['timestamp', 'Open', 'High', 'Low', 'Close', 'Volume', 'Spread'] 
        
        print(f"✅ Data {symbol} ({timeframe}) berhasil diambil: {len(df)} baris.")

    except Exception as e:
        print(f"❌ Gagal mengambil data dari PostgreSQL. Error: {e}")
        # Jika gagal, DataFrame akan kosong
        df = pd.DataFrame()
    return df

app = Flask(__name__, static_folder='static', static_url_path='/static')

# Endpoint untuk melayani halaman utama (index.html)
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# Endpoint untuk melayani file JavaScript
@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('static/js', filename)

@app.route('/api/ohlc/<symbol>/<timeframe>', methods=['GET'])
def get_ohlc_data(symbol, timeframe):
    df = fetch_data_from_db(symbol, timeframe)
    
    if df.empty:
        return jsonify({"error": "Data not found"}), 404
    
    # Convert timestamp to Unix timestamp (seconds) for Lightweight Charts
    df['timestamp'] = pd.to_datetime(df['timestamp']).astype('int64') // 10**9
    
    # Mengembalikan data dalam format JSON dengan timestamp
    result = df.to_dict('records')
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)