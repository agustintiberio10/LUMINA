"""
Monitor de menciones para el bot de X de LUMINA.

Chequea periodicamente si alguien menciono al bot, y:
1. Sigue al usuario (follow back)
2. Responde la consulta con info de LUMINA
3. Invita a visitar www.lumina-org.com
"""

import json
import sys
from datetime import datetime
from pathlib import Path

import tweepy
import pytz

import config
from responder import build_reply

# Archivo para trackear la ultima mencion procesada
LAST_MENTION_FILE = Path(__file__).parent / "last_mention_id.json"


def _get_now() -> datetime:
    tz = pytz.timezone(config.TIMEZONE)
    return datetime.now(tz)


def _create_client() -> tweepy.Client:
    """Crea el cliente autenticado de X API v2."""
    return tweepy.Client(
        consumer_key=config.X_API_KEY,
        consumer_secret=config.X_API_SECRET,
        access_token=config.X_ACCESS_TOKEN,
        access_token_secret=config.X_ACCESS_TOKEN_SECRET,
    )


def load_last_mention_id() -> str | None:
    """Carga el ID de la ultima mencion procesada."""
    if LAST_MENTION_FILE.exists():
        with open(LAST_MENTION_FILE, "r") as f:
            data = json.load(f)
            return data.get("last_id")
    return None


def save_last_mention_id(mention_id: str) -> None:
    """Guarda el ID de la ultima mencion procesada."""
    with open(LAST_MENTION_FILE, "w") as f:
        json.dump({"last_id": mention_id}, f)


def follow_user(client: tweepy.Client, user_id: str, username: str) -> bool:
    """
    Sigue a un usuario en X.

    Returns:
        True si se pudo seguir, False en caso contrario.
    """
    try:
        client.follow_user(user_id)
        print(f"  -> Siguiendo a @{username}")
        return True
    except tweepy.errors.Forbidden:
        # Ya lo seguimos o esta bloqueado
        print(f"  -> Ya seguimos a @{username} (o no se puede seguir)")
        return False
    except tweepy.errors.TweepyException as e:
        print(f"  -> Error al seguir a @{username}: {e}")
        return False


def reply_to_mention(client: tweepy.Client, mention_id: str, username: str, text: str) -> bool:
    """
    Responde a una mencion con informacion de LUMINA.

    Returns:
        True si se pudo responder, False en caso contrario.
    """
    reply_text = build_reply(username, text)

    if config.DRY_RUN:
        print(f"  [DRY RUN] Reply a @{username} ({len(reply_text)}/280 chars):")
        print(f"  {reply_text}")
        return True

    try:
        response = client.create_tweet(
            text=reply_text,
            in_reply_to_tweet_id=mention_id,
        )
        tweet_id = response.data["id"]
        print(f"  -> Reply enviado a @{username} (ID: {tweet_id}, {len(reply_text)}/280 chars)")
        return True
    except tweepy.errors.TooManyRequests:
        print(f"  -> Rate limit alcanzado. Se reintentara en el proximo ciclo.")
        return False
    except tweepy.errors.TweepyException as e:
        print(f"  -> Error al responder a @{username}: {e}")
        return False


def check_and_respond_mentions() -> int:
    """
    Chequea menciones nuevas y responde a cada una.

    Flujo para cada mencion:
    1. Follow al usuario
    2. Responder con info de LUMINA + link a www.lumina-org.com

    Returns:
        Cantidad de menciones procesadas.
    """
    now = _get_now()
    print(f"\n[{now.strftime('%H:%M:%S')}] Chequeando menciones...")

    client = _create_client()

    # Obtener el ID de nuestra propia cuenta
    try:
        me = client.get_me()
        if not me.data:
            print("  Error: no se pudo obtener info de la cuenta.")
            return 0
        my_user_id = me.data.id
    except tweepy.errors.TweepyException as e:
        print(f"  Error al obtener info de cuenta: {e}")
        return 0

    # Obtener menciones nuevas
    last_id = load_last_mention_id()
    try:
        mentions = client.get_users_mentions(
            id=my_user_id,
            since_id=last_id,
            max_results=config.MENTIONS_MAX_RESULTS,
            tweet_fields=["author_id", "created_at", "text"],
            expansions=["author_id"],
            user_fields=["username"],
        )
    except tweepy.errors.TweepyException as e:
        print(f"  Error al obtener menciones: {e}")
        return 0

    if not mentions.data:
        print("  Sin menciones nuevas.")
        return 0

    # Crear mapa de author_id -> username
    users_map = {}
    if mentions.includes and "users" in mentions.includes:
        for user in mentions.includes["users"]:
            users_map[user.id] = user.username

    processed = 0
    newest_id = last_id

    # Procesar menciones (de mas vieja a mas nueva)
    for mention in reversed(mentions.data):
        mention_id = str(mention.id)
        author_id = str(mention.author_id)
        username = users_map.get(mention.author_id, "usuario")
        text = mention.text

        print(f"\n  Mencion de @{username}: \"{text[:80]}{'...' if len(text) > 80 else ''}\"")

        # 1. Follow al usuario
        follow_user(client, author_id, username)

        # 2. Responder con info de LUMINA
        reply_to_mention(client, mention_id, username, text)

        processed += 1

        # Trackear la mencion mas reciente
        if not newest_id or int(mention_id) > int(newest_id):
            newest_id = mention_id

    # Guardar el ID de la ultima mencion procesada
    if newest_id:
        save_last_mention_id(newest_id)

    print(f"\n  Menciones procesadas: {processed}")
    return processed


# --- CLI para testing ---

if __name__ == "__main__":
    print("=== Test del monitor de menciones ===\n")

    if config.DRY_RUN:
        print("Modo: DRY RUN (no se publicaran replies reales)\n")

    print("Chequeando menciones...")
    count = check_and_respond_mentions()
    print(f"\nTotal procesadas: {count}")
