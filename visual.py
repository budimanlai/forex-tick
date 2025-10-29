import pandas as pd
from sqlalchemy import create_engine
import mplfinance as mpf

# --- KONFIGURASI DATABASE (GANTI DENGAN KREDENSIAL ANDA) ---
DB_USER = "postgres"
DB_PASSWORD = "12345678"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "forex"
DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
ENGINE = create_engine(DB_URL)

# --- QUERY DATA DARI DATABASE ---

SYMBOL = 'XAUUSD'
TIMEFRAME = 'H4' # Ubah Timeframe sesuai yang ingin ditampilkan
LIMIT = 500 # Batasi jumlah baris untuk tampilan cepat

query = f"""
SELECT 
    timestamp, "open", high, low, "close", tick_volume, spread 
FROM 
    ohlcv_data 
WHERE 
    symbol = '{SYMBOL}' AND timeframe = '{TIMEFRAME}'
ORDER BY 
    timestamp DESC 
LIMIT {LIMIT};
"""

# Mengambil data menggunakan Pandas
try:
    df = pd.read_sql(query, ENGINE, index_col='timestamp')
    # Data MT5 biasanya diurutkan dari yang terbaru ke yang terlama. Kita balikkan (sortir ascending)
    df = df.sort_index()
    
    # Pastikan nama kolom sesuai ekspektasi mplfinance (huruf kapital)
    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Spread'] 
    
    print(f"✅ Data {SYMBOL} ({TIMEFRAME}) berhasil diambil: {len(df)} baris.")
    
except Exception as e:
    print(f"❌ Gagal mengambil data dari PostgreSQL. Error: {e}")
    # Jika gagal, DataFrame akan kosong
    df = pd.DataFrame()

# --- VISUALISASI MENGGUNAKAN MPLFINANCE ---
# Pastikan data terambil dan tidak kosong
if not df.empty:
    
    # --- Penyesuaian Style (Mendekati MT5 Default) ---
    # Kita bisa membuat style kustom untuk mendekati MT5 (biru/merah, latar belakang hitam/putih)
    mc = mpf.make_marketcolors(
        up='g', down='r', # Lilin Bullish Hijau, Bearish Merah
        edge='inherit',
        wick='inherit',
        volume='r',
        alpha=0.6
    )
    # Style ini menggunakan latar belakang yang bersih (Putih/Gray)
    s = mpf.make_mpf_style(
        marketcolors=mc,
        figcolor='white',
        gridcolor='gray',
        y_on_right=True, # Memindahkan sumbu Y ke kanan (seperti MT5)
    )

    # --- Menampilkan Volume sebagai plot terpisah ---
    # Jika volume tick tersedia, kita bisa menambahkannya sebagai panel tambahan (addplot)
    ap = [
        mpf.make_addplot(df['Volume'], panel=1, type='bar', color='blue', secondary_y=False)
    ]
    
    # --- Plotting Candlestick ---
    mpf.plot(
        df, 
        type='candle',        # Tipe chart: Candlestick
        style=s,              # Menggunakan style kustom
        title=f'{SYMBOL} - {TIMEFRAME} Chart', 
        ylabel='Price (OHLC)',
        ylabel_lower='Volume',
        addplot=ap,           # Menambahkan plot volume
        volume=True,          # Menampilkan volume (terkadang mplfinance menampilkannya secara default)
        tight_layout=True,    # Menyesuaikan tata letak
        show_nontrading=False, # Sembunyikan gap waktu non-trading (opsional)
        savefig='mt5_H4_chart.png' # Simpan ke file
    )
    print("✅ Chart berhasil dibuat dan disimpan sebagai mt5_like_chart.png")

else:
    print("Tidak dapat membuat chart karena DataFrame kosong.")
