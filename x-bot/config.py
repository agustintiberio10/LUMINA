"""Configuracion del bot de X para LUMINA."""

import os
import sys
from dotenv import load_dotenv

load_dotenv()


def _require_env(key: str) -> str:
    """Obtiene una variable de entorno obligatoria o termina con error."""
    value = os.getenv(key)
    if not value or value.startswith("tu_"):
        print(f"ERROR: La variable de entorno '{key}' no esta configurada.")
        print("Copia .env.example a .env y completa tus credenciales.")
        sys.exit(1)
    return value


# Credenciales de la API de X
X_API_KEY = _require_env("X_API_KEY")
X_API_SECRET = _require_env("X_API_SECRET")
X_ACCESS_TOKEN = _require_env("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET = _require_env("X_ACCESS_TOKEN_SECRET")

# Configuracion del bot
TWEET_INTERVAL_MINUTES = int(os.getenv("TWEET_INTERVAL_MINUTES", "20"))
PUBLISH_HOUR_START = int(os.getenv("PUBLISH_HOUR_START", "9"))
PUBLISH_HOUR_END = int(os.getenv("PUBLISH_HOUR_END", "22"))
TIMEZONE = os.getenv("TIMEZONE", "America/Argentina/Buenos_Aires")
DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"
