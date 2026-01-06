import pandas as pd
from sqlalchemy import create_engine, text
import os

def debug_timezone():
    # 1. Check Pandas Parsing
    print("--- Checking Pandas Parsing ---")
    date_str = "2025.10.01"
    time_str = "01:01:00"
    combined = date_str + " " + time_str
    
    # Simulate what export.py does
    df = pd.DataFrame({'<DATE>': [date_str], '<TIME>': [time_str]})
    df['timestamp'] = pd.to_datetime(df['<DATE>'] + ' ' + df['<TIME>'], format='%Y.%m.%d %H:%M:%S')
    
    print(f"Input: {combined}")
    print(f"Parsed Timestamp: {df['timestamp'].iloc[0]}")
    print(f"Parsed Timestamp Repr: {repr(df['timestamp'].iloc[0])}")
    
    # 2. Check Database Column Type and Stored Value
    print("\n--- Checking Database ---")
    DB_USER = "dev"
    DB_PASSWORD = "12345678"
    DB_HOST = "127.0.0.1"
    DB_PORT = "5432"
    DB_NAME = "forex"
    DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    try:
        engine = create_engine(DB_URL)
        with engine.connect() as conn:
            # Check column type
            result = conn.execute(text("SELECT data_type FROM information_schema.columns WHERE table_name = 'ohlcv_data' AND column_name = 'timestamp'"))
            col_type = result.fetchone()
            print(f"Column Type: {col_type[0] if col_type else 'Unknown'}")
            
            # Check what's actually in DB for this specific time
            result = conn.execute(text("SELECT timestamp, CAST(timestamp as varchar) FROM ohlcv_data WHERE symbol='XAUUSD' AND timeframe='M1' ORDER BY timestamp DESC LIMIT 1"))
            row = result.fetchone()
            if row:
                print(f"Last Row Timestamp (Raw): {row[0]}")
                print(f"Last Row Timestamp (String): {row[1]}")
    except Exception as e:
        print(f"DB Error: {e}")

if __name__ == "__main__":
    debug_timezone()
