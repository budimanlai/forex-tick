// Chart menggunakan global LightweightCharts dari standalone file
// File JavaScript biasa tanpa ES6 modules

let chart = null;
let candlestickSeries = null;
let currentTimeframe = 'H1';

// Create chart with MetaTrader 5 style
function createTradingChart() {
    // Check if LightweightCharts is available globally
    if (typeof LightweightCharts === 'undefined') {
        console.error('LightweightCharts library tidak ditemukan! Pastikan lightweight-charts.standalone.production.js sudah dimuat.');
        return;
    }

    const chartContainer = document.getElementById('chart-container');
    
    if (!chartContainer) {
        console.error('Chart container not found!');
        return;
    }

    chart = LightweightCharts.createChart(chartContainer, {
        width: chartContainer.clientWidth,
        height: 600,
        layout: {
            backgroundColor: '#1e1e1e',
            textColor: '#d1d4dc',
        },
        grid: {
            vertLines: {
                color: '#2B2B43',
                style: 1,
                visible: true,
            },
            horzLines: {
                color: '#2B2B43',
                style: 1,
                visible: true,
            },
        },
        crosshair: {
            mode: LightweightCharts.CrosshairMode.Normal,
            vertLine: {
                width: 1,
                color: '#758696',
                style: 0,
            },
            horzLine: {
                width: 1,
                color: '#758696',
                style: 0,
            },
        },
        rightPriceScale: {
            borderColor: '#485c7b',
            textColor: '#d1d4dc',
        },
        timeScale: {
            borderColor: '#485c7b',
            textColor: '#d1d4dc',
            timeVisible: true,
            secondsVisible: false,
        },
        watermark: {
            visible: true,
            fontSize: 48,
            horzAlign: 'center',
            vertAlign: 'center',
            color: 'rgba(171, 71, 188, 0.3)',
            text: 'XAUUSD',
        },
    });

    // Create candlestick series using correct API
    candlestickSeries = chart.addSeries(LightweightCharts.CandlestickSeries, {
        upColor: '#26a69a',
        downColor: '#ef5350',
        borderVisible: false,
        wickUpColor: '#26a69a',
        wickDownColor: '#ef5350',
    });

    // Make chart responsive
    window.addEventListener('resize', () => {
        chart.applyOptions({ width: chartContainer.clientWidth });
    });

    console.log('✅ Chart created successfully');
}

// Convert timestamp to format required by Lightweight Charts
function convertTimestamp(timestamp) {
    // Handle different timestamp formats
    if (!timestamp) return Math.floor(Date.now() / 1000);
    
    let date;
    if (typeof timestamp === 'string') {
        // Handle string timestamps like "2025-01-02T01:00:00" or "2025-01-02 01:00:00"
        date = new Date(timestamp);
    } else if (typeof timestamp === 'number') {
        // Handle Unix timestamps (seconds or milliseconds)
        if (timestamp > 1e10) {
            // Milliseconds
            date = new Date(timestamp);
        } else {
            // Seconds
            date = new Date(timestamp * 1000);
        }
    } else {
        date = new Date(timestamp);
    }
    
    if (isNaN(date.getTime())) {
        console.warn('Invalid timestamp:', timestamp);
        return Math.floor(Date.now() / 1000);
    }
    
    return Math.floor(date.getTime() / 1000);
}

// Load chart data from API
async function loadChartData(symbol = 'XAUUSD', timeframe = 'H1') {
    try {
        showLoading();
        
        const response = await fetch(`/api/ohlc/${symbol}/${timeframe}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        const candlestickData = data.map(item => {
            const convertedTime = convertTimestamp(item.timestamp);
            return {
                time: convertedTime,
                open: parseFloat(item.Open),
                high: parseFloat(item.High),
                low: parseFloat(item.Low),
                close: parseFloat(item.Close)
            };
        });
        
        // Sort by time to ensure proper ordering
        candlestickData.sort((a, b) => a.time - b.time);
        
        // Set the data to candlestick series
        candlestickSeries.setData(candlestickData);
        
        // Try to fit content to see all data
        chart.timeScale().fitContent();
        
        // Show the chart
        hideLoading();
        showChart();
        
    } catch (error) {
        console.error('Error loading chart data:', error);
        showError(`Failed to load chart data: ${error.message}`);
        hideLoading();
    }
}

// Change timeframe
function loadTimeframe(timeframe) {
    currentTimeframe = timeframe;
    
    // Update active button
    document.querySelectorAll('.controls button').forEach(btn => {
        btn.classList.remove('active');
    });
    
    const activeBtn = document.getElementById(`btn-${timeframe}`);
    if (activeBtn) {
        activeBtn.classList.add('active');
    }
    
    // Load data with new timeframe
    loadChartData('XAUUSD', timeframe);
}

// UI utility functions
function showLoading() {
    const loading = document.getElementById('loading');
    const error = document.getElementById('error');
    const chartContainer = document.getElementById('chart-container');
    
    if (loading) loading.style.display = 'block';
    if (error) error.style.display = 'none';
    if (chartContainer) chartContainer.style.display = 'none';
}

function hideLoading() {
    const loading = document.getElementById('loading');
    if (loading) loading.style.display = 'none';
}

function showChart() {
    const chartContainer = document.getElementById('chart-container');
    if (chartContainer) chartContainer.style.display = 'block';
}

function showError(message) {
    hideLoading();
    const error = document.getElementById('error');
    const chartContainer = document.getElementById('chart-container');
    
    if (error) {
        error.textContent = message;
        error.style.display = 'block';
    }
    if (chartContainer) chartContainer.style.display = 'none';
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    createTradingChart();
    loadChartData('XAUUSD', currentTimeframe);
});