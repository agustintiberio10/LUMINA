"""
Base de conocimiento y generador de respuestas para el bot de X de LUMINA.

Cuando alguien menciona al bot con una consulta, este modulo busca la
respuesta mas relevante en la base de conocimiento y la formatea como
reply dentro del limite de 280 caracteres de X.

La base de conocimiento incluye:
- Informacion sobre LUMINA (servicios, comisiones, Hub, etc.)
- Conocimiento general de seguros (glosario, leyes, plazos, siniestros)

La invitacion a www.lumina-org.com se envia solo 1 vez por usuario.
"""

import json
from pathlib import Path

MAX_TWEET_LENGTH = 280
LUMINA_URL = "www.lumina-org.com"
INVITE_SUFFIX = f"\n\nConoce mas en {LUMINA_URL}"

# Archivo para trackear usuarios que ya recibieron la invitacion
INVITED_USERS_FILE = Path(__file__).parent / "invited_users.json"


# =====================================================================
# BASE DE CONOCIMIENTO
# =====================================================================

KNOWLEDGE_BASE = [
    # --- LUMINA: Servicios ---

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
        "keywords": ["contab", "monotributo", "afip", "impuesto", "iva", "recategorizacion"],
        "answer": "Nuestra Unidad Contable maneja recategorizaciones de Monotributo, liquidaciones de IVA y exigencias de AFIP. $50 USD/mes. Vos concentrate en vender.",
    },
    # Marketing
    {
        "keywords": ["marketing", "publicidad", "leads", "campana", "google", "instagram", "facebook", "redes"],
        "answer": "Nuestra Unidad de Performance Marketing diseña y optimiza tus campanas en Google, Instagram y Facebook. Leads calificados directo a tu WhatsApp. $50 USD/mes.",
    },
    # Costos / Precios
    {
        "keywords": ["costo", "precio", "cuanto sale", "cuanto cuesta", "tarifa", "fee", "gratis"],
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
    # Programa referidos
    {
        "keywords": ["referido", "invitar", "programa", "5x2", "bonific", "descuento"],
        "answer": "Programa 5x2: invita a 5 productores al Hub. Si 2 se mantienen activos por 2 meses, tu membresia queda bonificada. Crecer juntos tiene recompensa.",
    },

    # --- SEGUROS: Conocimiento general ---

    # Que es un PAS
    {
        "keywords": ["pas", "productor", "asesor", "intermediario", "matricula", "habilitado"],
        "answer": "El PAS (Productor Asesor de Seguros) es el unico intermediario habilitado por la SSN para asesorar en seguros en Argentina (Ley 22.400). Tu matricula tiene mucho valor.",
    },
    # Tipos de seguros / Ramos
    {
        "keywords": ["tipo de seguro", "ramo", "ramos", "que seguros", "clase de seguro"],
        "answer": "Los principales ramos son: Automotores, Hogar, Vida, ART, Caucion, Transporte, Incendio, RC y Accidentes Personales. Cada uno regulado por la SSN con condiciones especificas.",
    },
    # Poliza
    {
        "keywords": ["poliza", "que es una poliza", "documento", "contrato de seguro"],
        "answer": "La poliza es el documento legal que formaliza el contrato de seguro (Art. 1, Ley 17.418). Detalla riesgos cubiertos, suma asegurada, prima y condiciones.",
    },
    # Siniestro
    {
        "keywords": ["siniestro", "accidente", "choque", "robo", "denuncia", "denunciar"],
        "answer": "Un siniestro debe denunciarse dentro de los 3 dias de conocerlo (Art. 46, Ley 17.418). La aseguradora tiene 30 dias para aceptar o rechazar. Si no responde, se considera aceptado.",
    },
    # Plazos legales
    {
        "keywords": ["plazo", "tiempo", "dias", "vencimiento", "prescripcion", "caduca"],
        "answer": "Plazos clave: Denuncia de siniestro 3 dias, pedido de info 15 dias, aceptacion/rechazo 30 dias, prescripcion 1 año. Fuente: Ley 17.418.",
    },
    # Prima / Precio del seguro
    {
        "keywords": ["prima", "premio", "cuota", "pago del seguro", "costo del seguro", "cuanto cuesta un seguro"],
        "answer": "La prima es el costo tecnico del riesgo. El premio es lo que pagas: prima + gastos + impuestos. Se puede fraccionar en cuotas. La mora suspende la cobertura automaticamente.",
    },
    # Cobertura
    {
        "keywords": ["cobertura", "que cubre", "alcance", "exclusion", "excluido", "no cubre"],
        "answer": "La cobertura define los riesgos amparados por la poliza. Las exclusiones (como vicio propio o dolo) estan detalladas en las condiciones generales aprobadas por la SSN.",
    },
    # Seguro de auto
    {
        "keywords": ["seguro de auto", "automotor", "vehiculo", "auto", "responsabilidad civil", "tercero"],
        "answer": "El seguro de auto cubre RC obligatoria, danos parciales/totales, robo, hurto e incendio. La RC es obligatoria por ley para circular. Siempre verifica las exclusiones de tu poliza.",
    },
    # Seguro de hogar
    {
        "keywords": ["hogar", "casa", "departamento", "combinado familiar", "incendio", "robo en casa"],
        "answer": "El Combinado Familiar ampara incendio, robo, danos por agua, cristales, RC y accidentes en la vivienda. Es clave mantener las sumas actualizadas para evitar infraseguro.",
    },
    # Seguro de vida
    {
        "keywords": ["vida", "seguro de vida", "fallecimiento", "beneficiario", "invalidez"],
        "answer": "El seguro de vida cubre fallecimiento o invalidez del asegurado. Es fundamental designar beneficiarios en la poliza para evitar demoras por tramite sucesorio.",
    },
    # ART / Riesgos del trabajo
    {
        "keywords": ["art", "riesgo del trabajo", "laboral", "accidente laboral", "enfermedad profesional"],
        "answer": "La ART cubre accidentes y enfermedades profesionales (Ley 24.557). Es obligatoria para todo empleador. El trabajador esta protegido desde el primer dia.",
    },
    # Franquicia
    {
        "keywords": ["franquicia", "deducible", "a cargo", "excedente"],
        "answer": "La franquicia es el monto del siniestro a cargo del asegurado. Puede ser deducible (siempre pagas la franquicia) o no deducible (si supera el monto, la cia paga todo).",
    },
    # Infraseguro
    {
        "keywords": ["infraseguro", "prorrata", "regla proporcional", "suma asegurada baja"],
        "answer": "Si la suma asegurada es menor al valor real del bien, hay infraseguro. En siniestro parcial se aplica prorrata: pagas la diferencia proporcional (Art. 65, Ley 17.418).",
    },
    # SSN / Regulacion
    {
        "keywords": ["ssn", "superintendencia", "regulacion", "norma", "resolucion", "organismo"],
        "answer": "La SSN (Superintendencia de Seguros de la Nacion) es el organismo que controla y regula toda la actividad aseguradora en Argentina (Ley 20.091).",
    },
    # Ley 17.418
    {
        "keywords": ["ley 17418", "ley de seguros", "contrato de seguro", "ley 17.418"],
        "answer": "La Ley 17.418 es la ley de contrato de seguros de Argentina. Regula derechos y obligaciones de asegurado y asegurador: reticencia, plazos, siniestros y prescripcion.",
    },
    # Ley 22.400
    {
        "keywords": ["ley 22400", "ley del productor", "regimen pas", "ley 22.400"],
        "answer": "La Ley 22.400 regula el regimen de los Productores Asesores de Seguros. Define roles (directo y organizador), requisitos de matriculacion, comisiones y obligaciones.",
    },
    # Reticencia
    {
        "keywords": ["reticencia", "declaracion falsa", "ocultar", "mentir", "falsear"],
        "answer": "La reticencia es ocultar o falsear datos al contratar un seguro. Puede anular el contrato (Art. 5, Ley 17.418). Es fundamental declarar con honestidad total.",
    },
    # Subrogacion
    {
        "keywords": ["subrogacion", "subrogar", "recupero", "cobrar al tercero"],
        "answer": "Subrogacion: cuando la aseguradora paga un siniestro, adquiere el derecho de reclamar al tercero responsable. Es clave no renunciar a derechos contra el culpable del dano.",
    },
    # Caucion
    {
        "keywords": ["caucion", "garantia", "licitacion", "contrato publico"],
        "answer": "El seguro de caucion garantiza el cumplimiento de obligaciones contractuales (obras, licitaciones, contratos). La aseguradora responde si el tomador incumple.",
    },
    # Fraude
    {
        "keywords": ["fraude", "estafa", "auto robo", "simulacion", "dolo"],
        "answer": "El fraude en seguros es un delito. La Resolucion 38.477 establece protocolos de deteccion. El asegurador queda liberado si el siniestro fue provocado con dolo (Art. 70, Ley 17.418).",
    },
    # Cross-selling
    {
        "keywords": ["cross selling", "venta cruzada", "vender mas", "ampliar cartera", "crecer"],
        "answer": "El cross-selling es clave para el PAS: si tu cliente confia en vos para el auto, hogar y vida son oportunidades naturales. Comision pura, sin costo de adquisicion.",
    },
    # Defensa al consumidor
    {
        "keywords": ["consumidor", "defensa", "reclamo", "queja", "demora de la compania"],
        "answer": "Si la aseguradora demora injustificadamente, aplica la Ley 24.240 de Defensa al Consumidor ademas de los plazos de la Ley 17.418. El PAS puede defender a su cliente.",
    },
]

# Respuesta por defecto cuando no hay match
DEFAULT_ANSWER = "Gracias por tu consulta. En Lumina el PAS es el centro: comisiones completas, cartera propia y libertad total."


# =====================================================================
# TRACKING DE USUARIOS INVITADOS
# =====================================================================

def load_invited_users() -> list[str]:
    """Carga la lista de usuarios que ya recibieron el link a la web."""
    if INVITED_USERS_FILE.exists():
        with open(INVITED_USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_invited_users(users: list[str]) -> None:
    """Guarda la lista de usuarios invitados."""
    users = users[-1000:]  # Mantener ultimos 1000
    with open(INVITED_USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def is_user_invited(username: str) -> bool:
    """Verifica si un usuario ya recibio la invitacion a la web."""
    users = load_invited_users()
    return username.lower() in users


def mark_user_invited(username: str) -> None:
    """Marca a un usuario como invitado."""
    users = load_invited_users()
    normalized = username.lower()
    if normalized not in users:
        users.append(normalized)
        save_invited_users(users)


# =====================================================================
# BUSQUEDA Y GENERACION DE RESPUESTAS
# =====================================================================

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

    El formato es: @usuario + respuesta + invitacion (solo si es primera vez).
    Todo debe caber en 280 caracteres.

    Args:
        username: Nombre de usuario de X (sin @).
        question: Texto de la pregunta/mencion.

    Returns:
        Texto del reply listo para publicar.
    """
    mention = f"@{username} "
    answer = find_best_answer(question)
    available = MAX_TWEET_LENGTH - len(mention)

    # Solo incluir link a la web si es la primera vez que le respondemos
    include_invite = not is_user_invited(username)

    if include_invite:
        full_reply = answer + INVITE_SUFFIX

        if len(full_reply) <= available:
            mark_user_invited(username)
            return mention + full_reply

        # Si no cabe con invitacion, recortar respuesta
        space_for_answer = available - len(INVITE_SUFFIX) - 3
        if space_for_answer > 50:
            truncated = answer[:space_for_answer] + "..."
            mark_user_invited(username)
            return mention + truncated + INVITE_SUFFIX

    # Sin invitacion (ya fue invitado o no cabe)
    if len(answer) <= available:
        return mention + answer

    return mention + answer[:available - 3] + "..."


# --- CLI para testing ---

if __name__ == "__main__":
    # Simular usuario nuevo y usuario repetido
    print("=== Test del responder ===\n")

    test_questions = [
        ("usuario_nuevo", "Hola, cuanto pagan de comision?"),
        ("usuario_nuevo", "Y como funciona el Hub?"),
        ("otro_usuario", "Que es un siniestro?"),
        ("otro_usuario", "Y que es la franquicia?"),
        ("tercero", "Que dice la ley 17418?"),
        ("cuarto", "Me pueden explicar que es infraseguro?"),
        ("quinto", "Que es una ART?"),
        ("sexto", "Que es la subrogacion?"),
    ]

    for username, q in test_questions:
        reply = build_reply(username, q)
        has_link = LUMINA_URL in reply
        print(f"@{username}: {q}")
        print(f"  Reply ({len(reply)}/280) [link: {'SI' if has_link else 'NO'}]:")
        print(f"  {reply}")
        print()
