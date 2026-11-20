"""Módulo de registro de eventos (logs) de Software FJ.

Todos los demás módulos importan este archivo para registrar
eventos y errores en logs/software_fj.log.
"""

import logging  # Librería estándar de Python para registrar mensajes
import os       # Permite crear carpetas y construir rutas

# Carpeta "logs" junto a este archivo (no depende de dónde se ejecute)
DIRECTORIO_LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
# Ruta completa del archivo de log
ARCHIVO_LOG = os.path.join(DIRECTORIO_LOGS, "software_fj.log")

# Crea la carpeta de logs si no existe
os.makedirs(DIRECTORIO_LOGS, exist_ok=True)