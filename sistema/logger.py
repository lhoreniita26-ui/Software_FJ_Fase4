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


# Se obtiene un logger con nombre propio
logger = logging.getLogger("software_fj")
# Se registran mensajes desde nivel DEBUG hacia arriba
logger.setLevel(logging.DEBUG)

# Se evita duplicar manejadores si el módulo se importa varias veces
if not logger.handlers:
    # Manejador que escribe en el archivo (utf-8 para las tildes)
    manejador = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")
    # Formato: fecha, nivel, módulo y mensaje
    formato = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(module)s | %(message)s"
    )
    # Se asigna el formato al manejador
    manejador.setFormatter(formato)
    # Se agrega el manejador al logger
    logger.addHandler(manejador)
    # Se evita que los mensajes salgan duplicados
    logger.propagate = False


def registrar_evento(mensaje):
    """Registra un evento informativo (operación exitosa)."""
    logger.info(mensaje)


def registrar_error(mensaje):
    """Registra un error (operación fallida)."""
    logger.error(mensaje)
    