"""
Bot de X (Twitter) para LUMINA.

Publica tweets automaticos sobre la propuesta de valor de LUMINA
para atraer Productores Asesores de Seguros (PAS).
"""

import json
import os
import random
import sys
from datetime import datetime
from pathlib import Path

import tweepy
import pytz

import config
from content import ALL_TWEETS, ALL_CATEGORIES

# Archivo para rastrear tweets ya publicados y evitar repeticiones
HISTORY_FILE = Path(__file__).parent / "tweet_history.json"


def create_client() -> tweepy.Client:
    """Crea y autentica el cliente de X API v2."""
    client = tweepy.Client(
        consumer_key=config.X_API_KEY,
        consumer_secret=config.X_API_SECRET,
        access_token=config.X_ACCESS_TOKEN,
        access_token_secret=config.X_ACCESS_TOKEN_SECRET,
    )
    return client


def load_history() -> list[str]:
    """Carga el historial de tweets publicados."""
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_history(history: list[str]) -> None:
    """Guarda el historial de tweets publicados."""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def pick_tweet(category: str | None = None) -> str | None:
    """
    Selecciona un tweet que no haya sido publicado recientemente.

    Args:
        category: Categoria especifica (valor, confianza, hub, servicios,
                  educativos, mindset). Si es None, elige de todas.

    Returns:
        El texto del tweet, o None si ya se publicaron todos.
    """
    history = load_history()

    if category and category in ALL_CATEGORIES:
        pool = ALL_CATEGORIES[category]
    else:
        pool = ALL_TWEETS

    # Filtrar tweets que ya fueron publicados
    available = [t for t in pool if t not in history]

    # Si ya publicamos todos, resetear el historial
    if not available:
        print("Todos los tweets fueron publicados. Reiniciando ciclo.")
        history.clear()
        save_history(history)
        available = pool

    return random.choice(available)


def is_within_publish_hours() -> bool:
    """Verifica si estamos dentro del horario de publicacion."""
    tz = pytz.timezone(config.TIMEZONE)
    now = datetime.now(tz)
    return config.PUBLISH_HOUR_START <= now.hour < config.PUBLISH_HOUR_END


def publish_tweet(text: str) -> dict | None:
    """
    Publica un tweet en X.

    Args:
        text: Contenido del tweet (max 280 caracteres).

    Returns:
        Respuesta de la API o None si es dry run.
    """
    tz = pytz.timezone(config.TIMEZONE)
    timestamp = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S %Z")

    if len(text) > 280:
        print(f"ADVERTENCIA: Tweet excede 280 caracteres ({len(text)}). Truncando.")
        text = text[:277] + "..."

    if config.DRY_RUN:
        print(f"[DRY RUN] [{timestamp}] Tweet que se publicaria:")
        print(f"---\n{text}\n---")
        print(f"Caracteres: {len(text)}/280")
        # Igual registrar en historial para testear la rotacion
        history = load_history()
        history.append(text)
        save_history(history)
        return None

    try:
        client = create_client()
        response = client.create_tweet(text=text)
        tweet_id = response.data["id"]
        print(f"[{timestamp}] Tweet publicado exitosamente (ID: {tweet_id})")
        print(f"  URL: https://x.com/i/status/{tweet_id}")

        # Registrar en historial
        history = load_history()
        history.append(text)
        save_history(history)

        return response.data

    except tweepy.errors.Forbidden as e:
        print(f"ERROR 403 Forbidden: {e}")
        print("Verifica que:")
        print("  1. Tu app este dentro de un PROYECTO en el Developer Portal")
        print("  2. Los permisos de la app sean 'Read and Write'")
        print("  3. Regeneraste los tokens DESPUES de cambiar permisos")
        sys.exit(1)

    except tweepy.errors.Unauthorized as e:
        print(f"ERROR 401 Unauthorized: {e}")
        print("Tus credenciales son invalidas. Regenera las claves en el Developer Portal.")
        sys.exit(1)

    except tweepy.errors.TooManyRequests as e:
        print(f"ERROR 429 Rate Limit: {e}")
        print("Excediste el limite de la API. Espera antes de reintentar.")
        return None

    except tweepy.errors.TweepyException as e:
        print(f"ERROR al publicar tweet: {e}")
        return None


def post_next(category: str | None = None) -> None:
    """Selecciona y publica el siguiente tweet."""
    if not is_within_publish_hours() and not config.DRY_RUN:
        tz = pytz.timezone(config.TIMEZONE)
        now = datetime.now(tz)
        print(
            f"Fuera de horario de publicacion ({now.hour}h). "
            f"Rango permitido: {config.PUBLISH_HOUR_START}h - {config.PUBLISH_HOUR_END}h"
        )
        return

    tweet = pick_tweet(category)
    if tweet:
        publish_tweet(tweet)


# --- CLI ---

def main():
    """Punto de entrada para ejecucion directa."""
    import argparse

    parser = argparse.ArgumentParser(description="Bot de X para LUMINA")
    parser.add_argument(
        "action",
        choices=["post", "preview", "stats"],
        help="Accion a realizar: post (publicar), preview (ver siguiente tweet), stats (estadisticas)",
    )
    parser.add_argument(
        "--category",
        choices=["valor", "confianza", "hub", "servicios", "educativos", "crecimiento"],
        default=None,
        help="Categoria del tweet (opcional)",
    )

    args = parser.parse_args()

    if args.action == "post":
        post_next(args.category)

    elif args.action == "preview":
        tweet = pick_tweet(args.category)
        if tweet:
            print("Siguiente tweet a publicar:")
            print(f"---\n{tweet}\n---")
            print(f"Caracteres: {len(tweet)}/280")
            cat = args.category or "todas"
            print(f"Categoria: {cat}")

    elif args.action == "stats":
        history = load_history()
        total = len(ALL_TWEETS)
        posted = len(history)
        remaining = total - posted
        print(f"Tweets totales en banco: {total}")
        print(f"Tweets publicados: {posted}")
        print(f"Tweets restantes: {remaining}")
        print(f"Progreso: {posted}/{total} ({posted/total*100:.0f}%)")
        print(f"\nPor categoria:")
        for name, tweets in ALL_CATEGORIES.items():
            cat_posted = len([t for t in tweets if t in history])
            print(f"  {name}: {cat_posted}/{len(tweets)}")


if __name__ == "__main__":
    main()
