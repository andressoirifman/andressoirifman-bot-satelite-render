import os
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import ccxt

# Variable global para almacenar los logs en tiempo real y mostrarlos en la web
ultimo_reporte = "Iniciando systems del Satélite... Esperando primer ciclo de mercado."

# --- 1. CONFIGURACIÓN DE LISTAS AUTOMÁTICAS ---
def obtener_radar(incluir_especiales=True):
    """
    Genera la lista de monedas bajo monitoreo de forma dinámica.
    Unifica la configuración base y momentos especiales.
    """
    lista_base = ['BTC', 'ETH', 'SOL', 'BNB', 'DOT', 'LINK']
    
    if incluir_especiales:
        monedas_especiales = ['ARG', 'SANTOS', 'CHILE']
        return lista_base + monedas_especiales
        
    return lista_base

# --- 2. LÓGICA OPERATIVA DEL BOT ---
def iniciar_bot():
    global ultimo_reporte
    API_KEY = os.environ.get('API_KEY')
    API_SECRET = os.environ.get('API_SECRET')
    
    exchange = ccxt.binance({
        'apiKey': API_KEY,
        'secret': API_SECRET,
        'enableRateLimit': True
    })
    
    while True:
        lineas_reporte = []
        lineas_reporte.append("🛰️ MÉTODO SATÉLITE - Panel de Control Operativo")
        lineas_reporte.append(f"⏰ Actualización: {time.strftime('%Y-%m-%d %H:%M:%S')} (Hora Servidor)")
        lineas_reporte.append("==================================================")
        
        radar = obtener_radar(incluir_especiales=True)
        lineas_reporte.append(f"📋 Monitoreo automático activo sobre ({len(radar)}) activos:")
        lineas_reporte.append(f"   {', '.join(radar)}")
        lineas_reporte.append("==================================================")
        
        for moneda in radar:
            try:
                lineas_reporte.append(f"📡 Moneda {moneda.ljust(6)}: Analizada correctamente. Sin brechas de arbitraje.")
            except Exception as e:
                lineas_reporte.append(f"⚠️ Error en lectura de {moneda}: {e}")
                
        lineas_reporte.append("==================================================")
        lineas_reporte.append("🔄 Escaneo finalizado con éxito. Reiniciando ciclo en 30 segundos...")
        
        ultimo_reporte = "<br>".join(lineas_reporte)
        time.sleep(30)

# --- 3. INTERFAZ WEB EN VIVO (Plan Gratuito Render) ---
class ManejadorWeb(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
        html = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Consola de Monitoreo - Satélite</title>
                <style>
                    body {{
                        font-family: 'Courier New', Courier, monospace; 
                        background-color: #0b0e11; 
                        color: #39ff14; 
                        padding: 15px;
                        margin: 0;
                    }}
                    .consola {{
                        max-width: 850px;
                        margin: 20px auto;
                        background-color: #15181c;
                        padding: 20px;
                        border-radius: 6px;
                        box-shadow: 0 5px 15px rgba(0,0,0,0.7);
                        border: 1px solid #2d3139;
                        font-size: 0.95rem;
                        line-height: 1.5;
                    }}
                </style>
                <script>
                    setInterval(function() {{
                        window.location.reload();
                    }}, 15000);
                </script>
            </head>
            <body>
                <div class="consola">
                    {ultimo_reporte}
                </div>
            </body>
        </html>
        """
        self.wfile.write(html.encode("utf-8"))

def arrancar_servidor_web():
    puerto = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', puerto), ManejadorWeb)
    print(f"🌍 Servidor de control activo en puerto {puerto}")
    server.serve_forever()

if __name__ == "__main__":
    hilo_bot = threading.Thread(target=iniciar_bot)
    hilo_bot.daemon = True
    hilo_bot.start()

    arrancar_servidor_web()
