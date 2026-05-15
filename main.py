import os
import time
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
import ccxt  # Asegurate de tener esto para Binance

# --- 1. CONFIGURACIÓN DEL BOT ---
API_KEY = os.environ.get('API_KEY')
API_SECRET = os.environ.get('API_SECRET')

def iniciar_bot():
    print("🛰️ Método Satélite: Iniciando análisis de mercado...")
    # Conexión a Binance
    exchange = ccxt.binance({
        'apiKey': API_KEY,
        'secret': API_SECRET,
        'enableRateLimit': True
    })
    
    # Tu lista de monedas (Base + Mundial)
    radar = ['BTC', 'ETH', 'SOL', 'ARG', 'SANTOS', 'CHILE']
    
    while True:
        for moneda in radar:
            try:
                print(f"📡 Analizando {moneda}...")
                # Aquí el bot hace su magia...
            except Exception as e:
                print(f"⚠️ Error en {moneda}: {e}")
        
        print("--- Ciclo completado. Esperando 30 segundos ---")
        time.sleep(30)

# --- 2. EL "TRUCO" PARA RENDER GRATIS ---
def arrancar_servidor_web():
    # Render usa un puerto variable, lo leemos de aquí
    puerto = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', puerto), SimpleHTTPRequestHandler)
    print(f"🌍 Servidor de control activo en puerto {puerto}")
    server.serve_forever()

if __name__ == "__main__":
    # Lanzamos el bot en un hilo separado
    hilo_bot = threading.Thread(target=iniciar_bot)
    hilo_bot.daemon = True
    hilo_bot.start()

    # Dejamos el servidor web activo para que Render vea que todo OK
    arrancar_servidor_web()
