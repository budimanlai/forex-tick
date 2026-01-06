from sqlalchemy import create_engine, text
import pandas as pd

# Reuse config from export.py (hardcoded for simplicity based on file view)
DB_USER = "dev"
DB_PASSWORD = "12345678"
DB_HOST = "127.0.0.1"
DB_PORT = "5432"
DB_NAME = "forex"
DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
ENGINE = create_engine(DB_URL)

def verify():
    # Gunakan query dengan range atau timezone explicit jika perlu.
    # Namun untuk simple testing, kita coba cari berdasarkan range menit tersebut.
    query = text("""
    SELECT 
        timestamp, "open", high, low, "close", tick_volume, spread 
    FROM 
        ohlcv_data 
    WHERE 
        symbol = 'XAUUSD' AND timeframe = 'M1' 
        AND timestamp >= '2025-12-31 23:10:00+07' 
        AND timestamp < '2025-12-31 23:11:00+07'
    ORDER BY timestamp DESC
    LIMIT 1
    """)
    
    with ENGINE.connect() as conn:
        result = conn.execute(query)
        row = result.fetchone()
        
        if row:
            print("Row found in DB:")
            print(f"Timestamp: {row[0]}")
            print(f"Open: {row[1]}")
            print(f"High: {row[2]}")
            print(f"Low: {row[3]}")
            print(f"Close: {row[4]}")
            print(f"TickVol: {row[5]}")
            
            # Expected: 4312.84 for Close
            expected_close = 4312.84
            # Convert decimal to float for comparison if needed
            close_val = float(row[4])
            
            if abs(close_val - expected_close) < 0.01:
                print("✅ VERIFIED: Price matches CSV.")
            else:
                print(f"❌ MISMATCH: Expected Close ~ {expected_close}, got {close_val}")

            # Check Timezone
            ts = row[0]
            print(f"Timestamp Timezone: {ts.tzinfo}")
            # Ensure it is interpreted as 23:10 or 23:10+07 depending on how it's stored/retrieved.
            # If we store 23:10+07, it should come back as 23:10+07 (or equivalent UTC).
            # Let's print the hour in +07
            import datetime
            jakarta_tz = datetime.timezone(datetime.timedelta(hours=7))
            ts_jakarta = ts.astimezone(jakarta_tz)
            print(f"Timestamp in Jakarta: {ts_jakarta}")
            
            if ts_jakarta.hour == 23 and ts_jakarta.minute == 10:
                 print("✅ VERIFIED: Time matches CSV (23:10).")
            else:
                 print(f"❌ MISMATCH: Expected 23:10, got {ts_jakarta.strftime('%H:%M')}")
        else:
            print("❌ Row NOT found in DB.")

if __name__ == "__main__":
    verify()
