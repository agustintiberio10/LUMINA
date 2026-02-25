"""
Scheduler para publicacion automatica de tweets.

Ejecuta el bot a intervalos regulares dentro del horario configurado.
Uso: python scheduler.py
"""

import signal
import sys
import time
from datetime import datetime

import pytz
import schedule

import config
from bot import post_next


def _get_now():
    """Obtiene la hora actual en la zona horaria configurada."""
    tz = pytz.timezone(config.TIMEZONE)
    return datetime.now(tz)


def scheduled_post():
    """Tarea programada: publica un tweet si estamos en horario."""
    now = _get_now()
    print(f"\n[{now.strftime('%Y-%m-%d %H:%M:%S %Z')}] Ejecutando publicacion programada...")
    post_next()


def start_scheduler():
    """Inicia el scheduler que publica tweets a intervalos regulares."""
    interval = config.TWEET_INTERVAL_MINUTES
    mode = "DRY RUN" if config.DRY_RUN else "PRODUCCION"
    now = _get_now()

    print("=" * 50)
    print("LUMINA X Bot - Scheduler")
    print("=" * 50)
    print(f"Modo: {mode}")
    print(f"Intervalo: cada {interval} minutos")
    print(f"Horario de publicacion: {config.PUBLISH_HOUR_START}:00 - {config.PUBLISH_HOUR_END}:00")
    print(f"Zona horaria: {config.TIMEZONE}")
    print(f"Hora actual: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print("=" * 50)
    print("Presiona Ctrl+C para detener.\n")

    # Programar la tarea
    schedule.every(interval).minutes.do(scheduled_post)

    # Publicar inmediatamente al iniciar
    print("Publicando primer tweet al iniciar...")
    post_next()

    # Manejar SIGINT/SIGTERM para salida limpia
    def handle_signal(signum, frame):
        print(f"\nSenal recibida ({signum}). Deteniendo scheduler...")
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    # Loop principal
    while True:
        schedule.run_pending()
        time.sleep(60)  # Checkear cada minuto


if __name__ == "__main__":
    start_scheduler()
