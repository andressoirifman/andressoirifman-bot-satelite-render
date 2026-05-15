import ccxt
import time
import os

API_KEY = os.environ.get('API_KEY')
API_SECRET = os.environ.get('API_SECRET')

def iniciar_bot():
    bot = ccxt.binance({
        'apiKey': API_KEY,
        'secret': API_SECRET,
        'enableRateLimit': True,
        'options': {'adjustForTimeSkew': True}
    })

    radar = ['ETH', 'SOL', 'BNB', 'XRP', 'ADA', 'DOT', 'LTC', 'LINK', 'AVAX']
    print(f"🛰️ MÉTODO SATÉLITE: En órbita. Monitoreando: {', '.join(radar)}")

    while True:
        for moneda in radar:
            try:
                tickers = bot.fetch_tickers(['BTC/USDT', f'{moneda}/BTC', f'{moneda}/USDT'])
                p1, p2, p3 = tickers['BTC/USDT']['ask'], tickers[f'{moneda}/BTC']['ask'], tickers[f'{moneda}/USDT']['bid']
                
                final = ((10 / p1) * 0.999 / p2 * 0.999 * p3 * 0.999)
                ganancia = (final / 10 - 1) * 100

                if ganancia > -0.1:
                    status = "🚀 OPORTUNIDAD" if ganancia >= 0.4 else "📡 Analizando"
                    print(f"{status} | {moneda}: {ganancia:+.4f}%")
                
                time.sleep(1)
            except: continue

if __name__ == "__main__":
    iniciar_bot()
