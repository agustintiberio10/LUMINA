"""
Scheduler para publicacion automatica de tweets y monitoreo de menciones.

- Publica tweets a intervalos regulares dentro del horario configurado
- Scrapea noticias de 100seguro.com.ar una vez al dia a las 11:00 AM
- Chequea menciones cada 5 minutos y responde + sigue al usuario

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
from news_scraper import refresh_daily_cache, should_refresh_cache
from mentions import check_and_respond_mentions


def _get_now():
    """Obtiene la hora actual en la zona horaria configurada."""
    tz = pytz.timezone(config.TIMEZONE)
    return datetime.now(tz)


def scheduled_post():
    """Tarea programada: publica un tweet si estamos en horario."""
    now = _get_now()
    print(f"\n[{now.strftime('%Y-%m-%d %H:%M:%S %Z')}] Ejecutando publicacion programada...")
    post_next()


def scheduled_news_refresh():
    """Tarea diaria: scrapea noticias de 100seguro.com.ar a las 11:00 AM."""
    now = _get_now()
    print(f"\n[{now.strftime('%Y-%m-%d %H:%M:%S %Z')}] Refrescando noticias del dia...")
    articles = refresh_daily_cache()
    print(f"  Cache actualizado: {len(articles)} noticias relevantes listas para publicar.")


def scheduled_mentions_check():
    """Tarea periodica: chequea menciones y responde."""
    try:
        check_and_respond_mentions()
    except Exception as e:
        print(f"  Error en chequeo de menciones: {e}")


def start_scheduler():
    """Inicia el scheduler completo del bot."""
    interval = config.TWEET_INTERVAL_MINUTES
    mentions_interval = config.MENTIONS_CHECK_MINUTES
    mode = "DRY RUN" if config.DRY_RUN else "PRODUCCION"
    now = _get_now()

    print("=" * 50)
    print("LUMINA X Bot - Scheduler")
    print("=" * 50)
    print(f"Modo: {mode}")
    print(f"Intervalo tweets: cada {interval} minutos")
    print(f"Monitoreo menciones: cada {mentions_interval} minutos")
    print(f"Scraping noticias: diario a las 11:00 AM")
    print(f"Horario de publicacion: {config.PUBLISH_HOUR_START}:00 - {config.PUBLISH_HOUR_END}:00")
    print(f"Zona horaria: {config.TIMEZONE}")
    print(f"Hora actual: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print("=" * 50)
    print("Presiona Ctrl+C para detener.\n")

    # 1. Programar tweets cada N minutos
    schedule.every(interval).minutes.do(scheduled_post)

    # 2. Programar scraping de noticias a las 11:00 AM
    schedule.every().day.at("11:00").do(scheduled_news_refresh)

    # 3. Programar chequeo de menciones cada M minutos
    schedule.every(mentions_interval).minutes.do(scheduled_mentions_check)

    # Al iniciar: cargar noticias si no hay cache de hoy
    if should_refresh_cache():
        print("No hay cache de noticias de hoy. Scrapeando ahora...")
        scheduled_news_refresh()
    else:
        print("Cache de noticias de hoy ya existe.")

    # Publicar primer tweet al iniciar
    print("\nPublicando primer tweet al iniciar...")
    post_next()

    # Primer chequeo de menciones al iniciar
    print("\nChequeando menciones pendientes...")
    scheduled_mentions_check()

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
