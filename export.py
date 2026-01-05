import pandas as pd
from sqlalchemy import create_engine
import os

# --- 1. KONFIGURASI DATABASE (GANTI DENGAN KREDENSIAL ANDA) ---
DB_USER = "dev"        # Contoh: "postgres"
DB_PASSWORD = "12345678"  # Contoh: "secret"
DB_HOST = "127.0.0.1"        # Contoh: "127.0.0.1"
DB_PORT = "5432"             # Port PostgreSQL standar
DB_NAME = "forex" # Nama database yang berisi tabel ohlcv_data

# URL Koneksi SQLAlchemy
DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
ENGINE = create_engine(DB_URL)

# --- 2. FUNGSI PEMROSESAN & IMPORT ---

def process_and_load_csv(file_path, symbol, timeframe, engine):
    """
    Membaca file CSV OHLCV, memproses kolomnya, dan memuatnya ke PostgreSQL.
    """
    print(f"-> Memproses data untuk {symbol} - {timeframe} dari file: {file_path}")
    
    try:
        # Membaca CSV dengan delimiter TAB (\t)
        df = pd.read_csv(file_path, sep='\t')
    except Exception as e:
        print(f"ERROR: Gagal membaca file {file_path}. {e}")
        return

    # 1. Pembuatan Kolom Datetime (timestamp)
    # Menggabungkan kolom <DATE> dan <TIME>
    df['timestamp'] = pd.to_datetime(df['<DATE>'] + ' ' + df['<TIME>'], format='%Y.%m.%d %H:%M:%S')

    # 2. Penambahan Kolom Kunci
    df['symbol'] = symbol
    df['timeframe'] = timeframe

    # 3. Penyesuaian Nama Kolom untuk database (dengan tanda kutip ganda)
    # Penting: Karena Anda membuat kolom dengan kutip ganda di SQL, 
    # Pandas akan otomatis menanganinya jika nama kolom DataFrame sesuai.
    df.rename(columns={
        '<OPEN>': 'open',
        '<HIGH>': 'high',
        '<LOW>': 'low',
        '<CLOSE>': 'close',
        '<TICKVOL>': 'tick_volume',
        '<VOL>': 'real_volume',
        '<SPREAD>': 'spread'
    }, inplace=True)

    # Pilih dan susun ulang kolom yang sesuai dengan skema PostgreSQL, 
    # kecuali 'id' (dibuat otomatis oleh DB) dan kolom sumber (<DATE>, <TIME>).
    columns_to_keep = [
        'symbol', 'timeframe', 'timestamp', 
        'open', 'high', 'low', 'close', 
        'tick_volume', 'real_volume', 'spread'
    ]
    df_final = df[columns_to_keep]

    # 4. Memuat Data ke PostgreSQL
    try:
        # 'if_exists="append"' akan menambahkan data. 
        # Index UNIQUE di DB akan mencegah duplikasi baris yang sama.
        # 'index=False' karena 'id' adalah SERIAL di DB, bukan dari DataFrame.
        df_final.to_sql(
            name='ohlcv_data', 
            con=engine, 
            if_exists='append', 
            index=False,
            schema='public' # Sesuaikan jika Anda menggunakan skema lain
        )
        print(f"✅ Selesai: {len(df_final)} baris data {symbol} - {timeframe} berhasil dimuat.")
    except Exception as e:
        # Jika terjadi duplikasi (karena UNIQUE INDEX), ini akan tertangkap.
        print(f"❌ GAGAL memuat {symbol} - {timeframe}. Kemungkinan duplikasi data. Error: {e}")

# --- 3. EKSEKUSI UTAMA ---

if __name__ == '__main__':
    
    # Ganti 'path/to/your/files' dengan direktori tempat file CSV Anda berada
    BASE_DIR = os.getcwd() + "/data"

    # Daftar file Anda dan parameter terkait
    file_list = [
        # Ganti nama file ini sesuai dengan file yang Anda miliki
        ("XAUUSD_M1_202101040100_202106302354.csv", "XAUUSD", "M1"), 
        ("XAUUSD_M1_202107010100_202112312354.csv", "XAUUSD", "M1"),

        ("XAUUSD_M1_202201030100_202206302354.csv", "XAUUSD", "M1"),
        ("XAUUSD_M1_202207010100_202212302354.csv", "XAUUSD", "M1"),
        ("XAUUSD_M1_202301030100_202306302354.csv", "XAUUSD", "M1"),
        ("XAUUSD_M1_202307030101_202312292354.csv", "XAUUSD", "M1"),
        ("XAUUSD_M1_202401020101_202406282357.csv", "XAUUSD", "M1"),
        ("XAUUSD_M1_202407010100_202412312357.csv", "XAUUSD", "M1"),
        ("XAUUSD_M1_202501020101_202509292357.csv", "XAUUSD", "M1"),
        ("XAUUSD_M1_202510010101_202512312357.csv", "XAUUSD", "M1"),
    ]
    
    print("Memulai proses koneksi dan pemuatan data...")

    for file_name, symbol_name, tf_name in file_list:
        full_path = os.path.join(BASE_DIR, file_name)
        
        # Hanya memproses jika file ada
        if os.path.exists(full_path):
            process_and_load_csv(full_path, symbol_name, tf_name, ENGINE)
        else:
            print(f"⚠️ File tidak ditemukan: {full_path}. Melewati.")

    print("\nProses pemuatan data ke PostgreSQL selesai.")