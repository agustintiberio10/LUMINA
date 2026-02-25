"""
Scraper de noticias de 100seguro.com.ar para el bot de X de LUMINA.

Obtiene las noticias mas recientes del mercado asegurador argentino
y genera tweets informativos con el link a la nota original.
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
NEWS_HISTORY_FILE = Path(__file__).parent / "news_history.json"

# Categorias relevantes para el publico PAS de LUMINA
RELEVANT_KEYWORDS = [
    "productor", "pas ", "corredor", "broker", "comision",
    "ssn", "superintendencia", "regulacion", "resolucion",
    "art ", "riesgo", "siniestro", "poliza",
    "aseguradora", "seguro", "prima", "cobertura",
    "ley", "legislacion", "reforma", "norma",
    "mercado", "industria", "innovacion", "tecnologia",
    "auto", "automotor", "vehiculo",
    "vida", "patrimonial", "hogar",
    "fraude", "prevencion", "capacitacion",
]


def fetch_news() -> list[dict]:
    """
    Obtiene las noticias mas recientes de 100seguro.com.ar.

    Returns:
        Lista de diccionarios con titulo, url y resumen de cada noticia.
    """
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

    # Buscar articulos en la pagina principal
    for article in soup.find_all("article"):
        title_tag = article.find(["h2", "h3"])
        if not title_tag:
            continue

        link_tag = title_tag.find("a") or article.find("a")
        if not link_tag or not link_tag.get("href"):
            continue

        title = title_tag.get_text(strip=True)
        url = link_tag["href"]

        # Asegurar URL completa
        if url.startswith("/"):
            url = f"https://100seguro.com.ar{url}"

        # Buscar resumen/extracto
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


def load_news_history() -> list[str]:
    """Carga el historial de noticias ya tweeteadas (por hash de URL)."""
    if NEWS_HISTORY_FILE.exists():
        with open(NEWS_HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_news_history(history: list[str]) -> None:
    """Guarda el historial de noticias tweeteadas."""
    # Mantener solo las ultimas 200 para no crecer indefinidamente
    history = history[-200:]
    with open(NEWS_HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def _url_hash(url: str) -> str:
    """Genera un hash corto de la URL para tracking."""
    return hashlib.md5(url.encode()).hexdigest()[:12]


def format_news_tweet(article: dict) -> str:
    """
    Formatea un articulo como tweet.

    El formato es: titulo + link. Se respeta el limite de 280 caracteres.
    Las URLs de t.co en X ocupan 23 caracteres fijos.
    """
    title = article["title"]
    url = article["url"]

    # En X, cualquier URL ocupa 23 caracteres (t.co shortener)
    url_length = 23
    # Separador entre titulo y URL
    separator = "\n\n"
    max_title_length = 280 - url_length - len(separator)

    if len(title) > max_title_length:
        title = title[:max_title_length - 3] + "..."

    return f"{title}{separator}{url}"


def get_news_tweet() -> str | None:
    """
    Obtiene una noticia nueva y la formatea como tweet.

    Returns:
        Texto del tweet o None si no hay noticias nuevas.
    """
    articles = fetch_news()
    if not articles:
        print("No se pudieron obtener noticias de 100seguro.com.ar")
        return None

    history = load_news_history()

    # Buscar la primera noticia que no hayamos tweeteado
    for article in articles:
        article_hash = _url_hash(article["url"])
        if article_hash not in history:
            tweet = format_news_tweet(article)
            # Registrar como tweeteada
            history.append(article_hash)
            save_news_history(history)
            return tweet

    print("Todas las noticias actuales ya fueron tweeteadas.")
    return None


# --- CLI para testing ---

if __name__ == "__main__":
    print("Obteniendo noticias de 100seguro.com.ar...\n")
    articles = fetch_news()

    if not articles:
        print("No se encontraron articulos.")
    else:
        print(f"Se encontraron {len(articles)} articulos:\n")
        for i, article in enumerate(articles, 1):
            tweet = format_news_tweet(article)
            print(f"--- Articulo {i} ---")
            print(f"Titulo: {article['title']}")
            print(f"URL: {article['url']}")
            print(f"Tweet ({len(tweet)} chars):")
            print(tweet)
            print()
