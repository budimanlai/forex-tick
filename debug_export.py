import pandas as pd
import os

def debug_csv_parsing():
    file_path = "data/XAUUSD_M1_202510010101_202512312357.csv"
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    print(f"Reading {file_path}...")
    try:
        df = pd.read_csv(file_path, sep='\t')
        
        # Construct timestamp to match logic
        df['timestamp'] = pd.to_datetime(df['<DATE>'] + ' ' + df['<TIME>'], format='%Y.%m.%d %H:%M:%S')
        
        # Filter for the specific time
        target_time = pd.Timestamp("2025-12-31 23:10:00")
        row = df[df['timestamp'] == target_time]
        
        if not row.empty:
            print("Found row:")
            print(row[['timestamp', '<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>']].to_string(index=False))
        else:
            print("Row not found for 2025-12-31 23:10:00")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_csv_parsing()
