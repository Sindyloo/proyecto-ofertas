# Configuración de Gunicorn para evitar timeouts en producción
import multiprocessing

# Número de workers (ajustar según recursos disponibles)
workers = 2

# Timeout aumentado para permitir que las categorías se procesen completamente
# 300 segundos = 5 minutos (suficiente para procesar categorías grandes)
timeout = 300

# Timeout para mantener conexiones vivas
keepalive = 5

# Logging
accesslog = "-"  # stdout
errorlog = "-"   # stderr
loglevel = "info"

# Worker class
worker_class = "sync"

# Preload app para mejor rendimiento
preload_app = True

# Máximo de requests por worker antes de reciclar (previene memory leaks)
max_requests = 1000
max_requests_jitter = 50

