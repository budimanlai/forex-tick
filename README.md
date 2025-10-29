# XAUUSD Trading Chart Application

Aplikasi web untuk menampilkan chart trading XAUUSD (Gold/USD) dengan gaya MetaTrader 5 menggunakan Flask (Python) sebagai backend API dan **Vanilla JavaScript** untuk frontend.

## 🚀 Quick Start

### Menjalankan Aplikasi (Otomatis)

```bash
./start.sh
```

Script ini akan:
- Membuat virtual environment Python (jika belum ada)
- Menginstall dependencies Python
- Menginstall dependencies JavaScript
- Menjalankan Flask server

### Menjalankan Aplikasi (Manual)

1. **Setup Python Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # atau
   venv\Scripts\activate     # Windows
   ```

2. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install JavaScript Dependencies**
   ```bash
   npm install
   ```

4. **Jalankan Server**
   ```bash
   python api.py
   ```

5. **Akses Aplikasi**
   - Buka browser dan kunjungi: http://localhost:5000

## 📁 Struktur Project (Simplified)

```
python-tick/
├── api.py                  # Flask server & API endpoints
├── requirements.txt        # Python dependencies
├── package.json           # JavaScript dependencies
├── start.sh              # Startup script
├── .gitignore            # Git ignore rules
├── static/               # Frontend files
│   ├── index.html        # Main HTML page
│   └── js/               # JavaScript files
│       ├── chart.js      # Chart logic (Vanilla JS)
│       └── lightweight-charts.standalone.production.js
├── data/                 # CSV data files
│   ├── XAUUSD_H1.csv
│   ├── XAUUSD_H4.csv
│   └── ...
├── node_modules/         # JavaScript dependencies
└── venv/                # Python virtual environment
```

## 🔗 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Halaman utama (index.html) |
| `/static/<path>` | GET | File statis (HTML, CSS, gambar) |
| `/js/<filename>` | GET | File JavaScript |
| `/api/ohlc/<symbol>/<timeframe>` | GET | Data OHLC untuk trading |

### Contoh API Call:
```
GET /api/ohlc/XAUUSD/H1
```

Response:
```json
[
  {
    "Open": 2624.81,
    "High": 2625.63,
    "Low": 2621.57,
    "Close": 2623.66,
    "Volume": 1795,
    "Spread": 15,
    "timestamp": "2025-01-02T01:00:00"
  }
]
```

## ⚙️ Konfigurasi Database

Edit file `api.py` untuk konfigurasi database:

```python
DB_USER = "postgres"
DB_PASSWORD = "12345678"
DB_HOST = "localhost" 
DB_PORT = "5432"
DB_NAME = "forex"
```

## 🎨 Features

- ✅ Chart candlestick real-time
- ✅ Multiple timeframes (M5, M15, M30, H1, H4)
- ✅ MetaTrader 5 style theme
- ✅ Responsive design
- ✅ RESTful API
- ✅ Error handling
- ✅ Loading indicators
- ✅ **Vanilla JavaScript** (No frameworks, no modules)

## 🛠️ Technology Stack

### Frontend
- **Vanilla JavaScript**: No frameworks, simple dan mudah dipahami
- **Lightweight Charts**: Library chart dari TradingView
- **HTML5 + CSS3**: Responsive design

### Backend
- **Flask**: Web framework Python yang ringan
- **Pandas**: Data manipulation
- **SQLAlchemy**: Database ORM
- **psycopg2**: PostgreSQL adapter

## 🧪 Development

### Menambah Timeframe Baru

1. Tambahkan button di `static/index.html`
2. Update fungsi `loadTimeframe()` di `static/js/chart.js`
3. Pastikan data tersedia di database

### Menambah Symbol Baru

1. Update fungsi `loadChartData()` di `static/js/chart.js`
2. Pastikan data symbol tersedia di database
3. Update UI untuk selector symbol

## 📝 Dependencies

### Python
- Flask: Web framework
- Pandas: Data manipulation
- SQLAlchemy: Database ORM
- psycopg2: PostgreSQL adapter

### JavaScript
- Lightweight Charts: Chart library (standalone version)
- **No npm build process needed!**
- **No bundlers required!**

## 🐛 Troubleshooting

### Error: "Data not found"
- Periksa koneksi database
- Pastikan table `ohlcv_data` ada dan berisi data
- Periksa konfigurasi database di `api.py`

### Error: "LightweightCharts is not defined"
- Pastikan file `lightweight-charts.standalone.production.js` dimuat dengan benar
- Periksa order script loading di HTML

### Error: "Port already in use"
```bash
# Cari process yang menggunakan port 5000
lsof -i :5000
# Kill process
kill -9 <PID>
```

### Error: "Module not found"
```bash
# Pastikan virtual environment aktif
source venv/bin/activate
# Install ulang dependencies
pip install -r requirements.txt
```

## 🎯 Why Vanilla JavaScript?

- **Simple**: Tidak perlu setup bundler atau transpiler
- **Fast**: Loading time lebih cepat
- **Compatible**: Bekerja di semua browser modern
- **Easy Debug**: Code mudah di-debug langsung di browser
- **No Build Step**: Langsung edit dan refresh browser

## 📄 License

MIT License