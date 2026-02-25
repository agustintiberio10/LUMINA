"""
Scheduler para publicacion automatica de tweets y monitoreo de menciones.

- Publica tweets a intervalos regulares dentro del horario configurado
- Scrapea noticias de 100seguro.com.ar una vez al dia a las 11:00 AM
- Chequea menciones cada 5 minutos y responde + sigue al usuario
- Log a archivo para monitoreo en produccion

Uso: python scheduler.py
"""

import logging
import signal
import sys
import time
from datetime import datetime
from pathlib import Path

import pytz
import schedule

import config
from bot import post_next
from news_scraper import refresh_daily_cache, should_refresh_cache
from mentions import check_and_respond_mentions

# --- Logging ---
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_DIR / "bot.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger("lumina-bot")


def _get_now():
    """Obtiene la hora actual en la zona horaria configurada."""
    tz = pytz.timezone(config.TIMEZONE)
    return datetime.now(tz)


def scheduled_post():
    """Tarea programada: publica un tweet si estamos en horario."""
    logger.info("Ejecutando publicacion programada...")
    try:
        post_next()
    except Exception as e:
        logger.error(f"Error en publicacion: {e}")


def scheduled_news_refresh():
    """Tarea diaria: scrapea noticias de 100seguro.com.ar a las 11:00 AM."""
    logger.info("Refrescando noticias del dia...")
    try:
        articles = refresh_daily_cache()
        logger.info(f"Cache actualizado: {len(articles)} noticias relevantes.")
    except Exception as e:
        logger.error(f"Error en scraping de noticias: {e}")


def scheduled_mentions_check():
    """Tarea periodica: chequea menciones y responde."""
    try:
        count = check_and_respond_mentions()
        if count > 0:
            logger.info(f"Menciones procesadas: {count}")
    except Exception as e:
        logger.error(f"Error en chequeo de menciones: {e}")


def start_scheduler():
    """Inicia el scheduler completo del bot."""
    interval = config.TWEET_INTERVAL_MINUTES
    mentions_interval = config.MENTIONS_CHECK_MINUTES
    mode = "DRY RUN" if config.DRY_RUN else "PRODUCCION"
    now = _get_now()

    logger.info("=" * 50)
    logger.info("LUMINA X Bot - Scheduler")
    logger.info("=" * 50)
    logger.info(f"Modo: {mode}")
    logger.info(f"Intervalo tweets: cada {interval} minutos")
    logger.info(f"Monitoreo menciones: {'cada ' + str(mentions_interval) + ' minutos' if config.ENABLE_MENTIONS else 'DESACTIVADO'}")
    logger.info(f"Scraping noticias: diario a las 11:00 AM")
    logger.info(f"Horario: {config.PUBLISH_HOUR_START}:00 - {config.PUBLISH_HOUR_END}:00")
    logger.info(f"Zona horaria: {config.TIMEZONE}")
    logger.info(f"Hora actual: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    logger.info(f"Log: {LOG_DIR / 'bot.log'}")
    logger.info("=" * 50)

    # 1. Programar tweets cada N minutos
    schedule.every(interval).minutes.do(scheduled_post)

    # 2. Programar scraping de noticias a las 11:00 AM
    schedule.every().day.at("11:00").do(scheduled_news_refresh)

    # 3. Programar chequeo de menciones cada M minutos (si esta habilitado)
    if config.ENABLE_MENTIONS:
        schedule.every(mentions_interval).minutes.do(scheduled_mentions_check)

    # Al iniciar: cargar noticias si no hay cache de hoy
    if should_refresh_cache():
        logger.info("No hay cache de noticias de hoy. Scrapeando ahora...")
        scheduled_news_refresh()
    else:
        logger.info("Cache de noticias de hoy ya existe.")

    # Publicar primer tweet al iniciar
    logger.info("Publicando primer tweet al iniciar...")
    post_next()

    # Primer chequeo de menciones al iniciar (si esta habilitado)
    if config.ENABLE_MENTIONS:
        logger.info("Chequeando menciones pendientes...")
        scheduled_mentions_check()
    else:
        logger.info("Monitoreo de menciones desactivado (ENABLE_MENTIONS=false).")

    # Manejar SIGINT/SIGTERM para salida limpia
    def handle_signal(signum, frame):
        logger.info(f"Senal recibida ({signum}). Deteniendo scheduler...")
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    logger.info("Scheduler activo. Presiona Ctrl+C para detener.\n")

    # Loop principal
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    start_scheduler()
