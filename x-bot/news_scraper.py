"""
Scraper de noticias de 100seguro.com.ar para el bot de X de LUMINA.

Obtiene las noticias mas recientes del mercado asegurador argentino
una vez por dia (a las 11:00 AM) y las cachea localmente.
Durante el dia el bot publica las noticias relevantes sin repetir.
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup
import pytz

import config

NEWS_URL = "https://100seguro.com.ar/"
DAILY_CACHE_FILE = Path(__file__).parent / "news_daily_cache.json"
NEWS_HISTORY_FILE = Path(__file__).parent / "news_history.json"

# Keywords para filtrar noticias relevantes para PAS
RELEVANT_KEYWORDS = [
    # Regulacion y normativa
    "ssn", "superintendencia", "regulacion", "resolucion", "norma",
    "ley", "legislacion", "reforma", "decreto",
    # Actores del mercado
    "productor", "pas", "corredor", "broker", "organizador",
    "aseguradora", "compania de seguros", "reaseguradora",
    # Productos y operaciones
    "poliza", "cobertura", "prima", "comision", "siniestro",
    "art", "riesgo", "automotor", "auto", "vehiculo",
    "vida", "patrimonial", "hogar", "caucion",
    # Industria
    "mercado asegurador", "mercado de seguros", "industria",
    "innovacion", "tecnologia", "digital", "insurtech",
    # Temas de interes
    "fraude", "prevencion", "capacitacion", "formacion",
    "robo", "accidente", "seguridad vial",
    "credito", "hipotecario", "inmobiliario",
]


def _get_now() -> datetime:
    """Hora actual en zona horaria configurada."""
    tz = pytz.timezone(config.TIMEZONE)
    return datetime.now(tz)


def _url_hash(url: str) -> str:
    """Genera un hash corto de la URL para tracking."""
    return hashlib.md5(url.encode()).hexdigest()[:12]


def _is_relevant(article: dict) -> bool:
    """Determina si una noticia es relevante para el publico PAS de LUMINA."""
    text = (article["title"] + " " + article.get("excerpt", "")).lower()
    return any(kw in text for kw in RELEVANT_KEYWORDS)


def fetch_news_from_web() -> list[dict]:
    """Obtiene las noticias mas recientes de 100seguro.com.ar."""
    try:
        response = requests.get(NEWS_URL, timeout=15, headers={
            "User-Agent": "LUMINA-Bot/1.0 (Insurance News Aggregator)"
        })
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error al obtener noticias: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    articles = []

    for article in soup.find_all("article"):
        title_tag = article.find(["h2", "h3"])
        if not title_tag:
            continue

        link_tag = title_tag.find("a") or article.find("a")
        if not link_tag or not link_tag.get("href"):
            continue

        title = title_tag.get_text(strip=True)
        url = link_tag["href"]

        if url.startswith("/"):
            url = f"https://100seguro.com.ar{url}"

        excerpt = ""
        excerpt_tag = article.find(class_=lambda c: c and ("excerpt" in c or "summary" in c or "description" in c))
        if excerpt_tag:
            excerpt = excerpt_tag.get_text(strip=True)
        else:
            p_tag = article.find("p")
            if p_tag:
                excerpt = p_tag.get_text(strip=True)

        if title and url:
            articles.append({
                "title": title,
                "url": url,
                "excerpt": excerpt,
            })

    return articles


# --- Cache diario ---

def load_daily_cache() -> dict:
    """Carga el cache diario de noticias."""
    if DAILY_CACHE_FILE.exists():
        with open(DAILY_CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"date": "", "articles": []}


def save_daily_cache(data: dict) -> None:
    """Guarda el cache diario de noticias."""
    with open(DAILY_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def refresh_daily_cache() -> list[dict]:
    """
    Scrapea 100seguro.com.ar, filtra noticias relevantes y las cachea.
    Se ejecuta una vez al dia a las 11:00 AM.

    Returns:
        Lista de articulos relevantes del dia.
    """
    now = _get_now()
    today = now.strftime("%Y-%m-%d")

    print(f"[{now.strftime('%H:%M:%S')}] Scrapeando 100seguro.com.ar...")
    all_articles = fetch_news_from_web()

    if not all_articles:
        print("No se pudieron obtener noticias.")
        return []

    # Filtrar solo las relevantes
    relevant = [a for a in all_articles if _is_relevant(a)]

    print(f"  Total encontradas: {len(all_articles)}")
    print(f"  Relevantes para PAS: {len(relevant)}")

    # Guardar en cache
    cache = {
        "date": today,
        "articles": relevant,
    }
    save_daily_cache(cache)

    return relevant


def should_refresh_cache() -> bool:
    """Determina si hay que refrescar el cache (una vez al dia a las 11am)."""
    now = _get_now()
    today = now.strftime("%Y-%m-%d")
    cache = load_daily_cache()

    # Si el cache es de otro dia, hay que refrescar
    if cache["date"] != today:
        return True

    return False


def get_todays_articles() -> list[dict]:
    """
    Obtiene los articulos del dia desde el cache.
    Si no hay cache de hoy, lo refresca.
    """
    cache = load_daily_cache()
    today = _get_now().strftime("%Y-%m-%d")

    if cache["date"] != today:
        return refresh_daily_cache()

    return cache["articles"]


# --- Historial de noticias tweeteadas ---

def load_news_history() -> list[str]:
    """Carga el historial de noticias ya tweeteadas (por hash de URL)."""
    if NEWS_HISTORY_FILE.exists():
        with open(NEWS_HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_news_history(history: list[str]) -> None:
    """Guarda el historial de noticias tweeteadas."""
    history = history[-500:]
    with open(NEWS_HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


# --- Formateo y seleccion ---

def format_news_tweet(article: dict) -> str:
    """
    Formatea un articulo como tweet.
    Formato: titulo + link. Las URLs en X ocupan 23 chars fijos (t.co).
    """
    title = article["title"]
    url = article["url"]

    url_length = 23
    separator = "\n\n"
    max_title_length = 280 - url_length - len(separator)

    if len(title) > max_title_length:
        title = title[:max_title_length - 3] + "..."

    return f"{title}{separator}{url}"


def get_news_tweet() -> str | None:
    """
    Obtiene una noticia relevante del cache diario que no haya sido tweeteada.

    Returns:
        Texto del tweet o None si no hay noticias nuevas.
    """
    articles = get_todays_articles()
    if not articles:
        print("No hay noticias en el cache de hoy.")
        return None

    history = load_news_history()

    for article in articles:
        article_hash = _url_hash(article["url"])
        if article_hash not in history:
            tweet = format_news_tweet(article)
            history.append(article_hash)
            save_news_history(history)
            print(f"  Noticia seleccionada: {article['title'][:60]}...")
            return tweet

    print("Todas las noticias relevantes de hoy ya fueron tweeteadas.")
    return None


# --- CLI para testing ---

if __name__ == "__main__":
    print("=== Test del scraper de noticias ===\n")

    print("1. Scrapeando 100seguro.com.ar...")
    all_articles = fetch_news_from_web()
    print(f"   Total: {len(all_articles)} articulos\n")

    relevant = [a for a in all_articles if _is_relevant(a)]
    print(f"2. Filtro de relevancia: {len(relevant)} de {len(all_articles)} son relevantes\n")

    print("3. Noticias relevantes del dia:\n")
    for i, article in enumerate(relevant, 1):
        tweet = format_news_tweet(article)
        print(f"--- [{i}] ---")
        print(f"Titulo: {article['title']}")
        print(f"URL: {article['url']}")
        print(f"Tweet ({len(tweet)} chars)")
        print()
