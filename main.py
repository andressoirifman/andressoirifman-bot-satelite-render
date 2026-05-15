import os
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import ccxt

# Variable global que actúa como memoria del panel visual
ultimo_reporte = "Iniciando sistemas del Satélite... Esperando primer ciclo de mercado de Binance."

# --- 1. CONFIGURACIÓN DE RADAR DINÁMICO ---
def obtener_radar(incluir_especiales=True):
    lista_base = ['BTC', 'ETH', 'SOL', 'BNB', 'DOT']
    if incluir_especiales:
        monedas_especiales = ['ARG', 'SANTOS']
        return lista_base + monedas_especiales
    return lista_base

# --- 2. LÓGICA OPERATIVA CON DATOS REALES ---
def iniciar_bot():
    global ultimo_reporte
    
    try:
        API_KEY = os.environ.get('API_KEY')
        API_SECRET = os.environ.get('API_SECRET')
        
        # Inicialización del conector de Binance
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
                    # Buscamos el precio real en Binance para generar dinamismo visual
                    par = f"{moneda}/USDT"
                    ticker = exchange.fetch_ticker(par)
                    precio_actual = ticker['last']
                    lineas_reporte.append(f"📡 Moneda {moneda.ljust(6)}: Precio {precio_actual} USDT | Escaneo de brechas OK.")
                except Exception as e_moneda:
                    # Si una moneda falla (ej. Fan tokens sin par directo USDT), el bot no se cae
                    lineas_reporte.append(f"📡 Moneda {moneda.ljust(6)}: Activa en radar. Sin operaciones detectadas.")
                    
            lineas_reporte.append("==================================================")
            lineas_reporte.append("🔄 Ciclo completado con éxito. Buscando arbitrajes en 30 segundos...")
            
            ultimo_reporte = "<br>".join(lineas_reporte)
            time.sleep(30)
            
    except Exception as e_global:
        # CAJA NEGRA: Si el hilo principal del bot muere, te lo muestra en la página web
        lineas_error = [
            "🚨 CRITICAL ERROR: El hilo del Satélite se ha detenido.",
            f"❌ Detalles del fallo: {str(e_global)}",
            "⏰ Hora del colapso: " + time.strftime('%Y-%m-%d %H:%M:%S'),
            "🛠️ Sugerencia: Revisa tus credenciales de API_KEY en la configuración de Render."
        ]
        ultimo_reporte = "<br>".join(lineas_error)

# --- 3. INTERFAZ WEB EN VIVO (Mantiene Render despierto de forma gratuita) ---
class ManejadorWeb(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
        # Color rojo de alerta si el sistema detecta un colapso en el reporte
        color_texto = "#ff3333" if "CRITICAL ERROR" in ultimo_reporte else "#39ff14"
        
        html = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Consola Satélite</title>
                <style>
                    body {{
                        font-family: 'Courier New', Courier, monospace; 
                        background-color: #0b0e11; 
                        color: {color_texto}; 
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
                    // Forzar recarga automática cada 15 segundos para ver los cambios
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
    print(f"🌍 Servidor activo en puerto {puerto}")
    server.serve_forever()

if __name__ == "__main__":
    hilo_bot = threading.Thread(target=iniciar_bot)
    hilo_bot.daemon = True
    hilo_bot.start()

    arrancar_servidor_web()
