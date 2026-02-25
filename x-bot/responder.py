"""
Base de conocimiento y generador de respuestas para el bot de X de LUMINA.

Cuando alguien menciona al bot con una consulta, este modulo busca la
respuesta mas relevante en la base de conocimiento de LUMINA y la formatea
como reply dentro del limite de 280 caracteres de X.
"""

# Limite de un reply en X: 280 chars totales (incluyendo @usuario)
MAX_TWEET_LENGTH = 280

# URL de la pagina de LUMINA para incluir en respuestas
LUMINA_URL = "www.lumina-org.com"

# Invitacion a la pagina (se agrega al final de cada respuesta)
INVITE_SUFFIX = f"\n\nConoce mas en {LUMINA_URL}"

# --- Base de conocimiento ---
# Cada entrada: (keywords para match, respuesta)
# Las respuestas deben ser cortas para dejar espacio al @usuario + invitacion

KNOWLEDGE_BASE = [
    # Comisiones
    {
        "keywords": ["comision", "comisiones", "porcentaje", "cuanto pagan", "cuanto gano", "rentabilidad", "cobra"],
        "answer": "En Lumina el PAS recibe el 100% de la comision en automotores y el 97% en el resto de los ramos. Nuestro modelo se sostiene con servicios opcionales, no con tu comision.",
    },
    # Modelo de negocio
    {
        "keywords": ["modelo", "como funciona", "que es lumina", "que hacen", "que ofrecen", "explicame"],
        "answer": "Lumina es un organizador donde el PAS es el centro. Comisiones completas (100% autos, 97% resto), cartera propia, libertad total y servicios opcionales de marketing y contabilidad.",
    },
    # Cartera propia
    {
        "keywords": ["cartera", "propiedad", "traspaso", "codigo", "salida", "irme", "dejar"],
        "answer": "En Lumina tu cartera es tu propiedad, reconocida de forma irrevocable en el contrato. Salida libre con 30 dias de preaviso y traspaso de codigos garantizado.",
    },
    # Hub / Coworking
    {
        "keywords": ["hub", "coworking", "oficina", "espacio", "grabacion", "sala", "reunion"],
        "answer": "El Lumina Hub es un espacio premium para el PAS: coworking, estudio de grabacion, salas de reuniones y comunidad. Todo por $100 USD/mes con salida libre.",
    },
    # Servicios contables
    {
        "keywords": ["contab", "monotributo", "afip", "impuesto", "iva", "recategorizacion", "numero"],
        "answer": "Nuestra Unidad Contable maneja recategorizaciones de Monotributo, liquidaciones de IVA y exigencias de AFIP. $50 USD/mes. Vos concentrate en vender.",
    },
    # Marketing
    {
        "keywords": ["marketing", "publicidad", "leads", "campana", "google", "instagram", "facebook", "redes"],
        "answer": "Nuestra Unidad de Performance Marketing diseña y optimiza tus campanas en Google, Instagram y Facebook. Leads calificados directo a tu WhatsApp. $50 USD/mes.",
    },
    # Costos / Precios
    {
        "keywords": ["costo", "precio", "cuanto sale", "cuanto cuesta", "valor", "tarifa", "fee", "gratis"],
        "answer": "Sumarte a Lumina no tiene costo. Solo retenemos 3% en ramos no-auto. Hub: $100 USD/mes. Contabilidad y Marketing: $50 USD/mes cada uno. Todo opcional.",
    },
    # Como unirse
    {
        "keywords": ["sumar", "unir", "empezar", "arrancar", "inscrib", "registr", "contacto", "quiero"],
        "answer": "No necesitas migrar toda tu cartera. Podes empezar codificando solo negocios nuevos y comparar la diferencia. Sin riesgo, sin compromiso.",
    },
    # Contrato
    {
        "keywords": ["contrato", "condicion", "clausula", "letra chica", "compromiso", "permanencia"],
        "answer": "Nuestro contrato es corto, claro y sin letra chica. Salida libre con 30 dias de preaviso. Pedilo, revisalo con tu abogado y despues decidis.",
    },
    # PAS / Productor
    {
        "keywords": ["pas", "productor", "asesor", "intermediario", "matricula", "habilitado"],
        "answer": "Lumina esta disenado 100% para el PAS independiente. Comisiones completas, cartera propia y un ecosistema de soporte para que crezcas a tu ritmo.",
    },
    # Seguros / Ramos
    {
        "keywords": ["seguro", "poliza", "auto", "hogar", "vida", "art", "riesgo", "cobertura", "ramo"],
        "answer": "Trabajamos con las principales aseguradoras del mercado argentino en todos los ramos: auto, hogar, vida, ART, caucion y mas. El PAS elige como armar su cartera.",
    },
    # SSN / Regulacion
    {
        "keywords": ["ssn", "superintendencia", "regulacion", "ley", "norma", "resolucion", "legal"],
        "answer": "Lumina opera dentro del marco regulatorio de la SSN. El PAS mantiene su matricula y opera con total respaldo legal.",
    },
    # Programa referidos
    {
        "keywords": ["referido", "invitar", "programa", "5x2", "bonific", "descuento"],
        "answer": "Programa 5x2: invita a 5 productores al Hub. Si 2 se mantienen activos por 2 meses, tu membresia queda bonificada. Crecer juntos tiene recompensa.",
    },
]

# Respuesta por defecto cuando no hay match
DEFAULT_ANSWER = "Gracias por tu consulta. En Lumina el PAS recibe comisiones completas y tiene libertad total."


def _normalize(text: str) -> str:
    """Normaliza texto para comparacion: minusculas, sin acentos basicos."""
    text = text.lower()
    replacements = {
        "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
        "ü": "u", "ñ": "n",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def find_best_answer(question: str) -> str:
    """
    Busca la mejor respuesta en la base de conocimiento.

    Args:
        question: Texto de la mencion/pregunta del usuario.

    Returns:
        La respuesta mas relevante.
    """
    normalized = _normalize(question)

    best_match = None
    best_score = 0

    for entry in KNOWLEDGE_BASE:
        score = sum(1 for kw in entry["keywords"] if kw in normalized)
        if score > best_score:
            best_score = score
            best_match = entry

    if best_match and best_score > 0:
        return best_match["answer"]

    return DEFAULT_ANSWER


def build_reply(username: str, question: str) -> str:
    """
    Construye un reply completo para X.

    El formato es: @usuario + respuesta + invitacion a la web.
    Todo debe caber en 280 caracteres.

    Args:
        username: Nombre de usuario de X (sin @).
        question: Texto de la pregunta/mencion.

    Returns:
        Texto del reply listo para publicar.
    """
    mention = f"@{username} "
    answer = find_best_answer(question)

    # Espacio disponible para respuesta + invitacion
    available = MAX_TWEET_LENGTH - len(mention)

    full_reply = answer + INVITE_SUFFIX

    if len(full_reply) <= available:
        return mention + full_reply

    # Si no cabe con invitacion, recortar respuesta para que entre todo
    space_for_answer = available - len(INVITE_SUFFIX) - 3  # 3 para "..."
    if space_for_answer > 50:
        truncated = answer[:space_for_answer] + "..."
        return mention + truncated + INVITE_SUFFIX

    # Ultimo recurso: solo respuesta sin invitacion
    if len(answer) <= available:
        return mention + answer

    return mention + answer[:available - 3] + "..."


# --- CLI para testing ---

if __name__ == "__main__":
    test_questions = [
        "Hola, cuanto pagan de comision?",
        "Como funciona Lumina?",
        "Mi cartera sigue siendo mia?",
        "Cuanto sale el Hub?",
        "Necesito ayuda con el monotributo",
        "Como hago para sumarme?",
        "Que onda con la SSN?",
        "Tienen marketing digital?",
        "Hola que tal!",
    ]

    for q in test_questions:
        reply = build_reply("usuario_test", q)
        print(f"Pregunta: {q}")
        print(f"Reply ({len(reply)}/280): {reply}")
        print()
