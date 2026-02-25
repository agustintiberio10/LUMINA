"""
Banco de contenido para el bot de X de LUMINA.

Cada tweet esta categorizado por tipo y respeta el limite de 280 caracteres.
Los tweets estan disenados para atraer Productores Asesores de Seguros (PAS).
"""

# --- PROPUESTA DE VALOR CORE ---
TWEETS_VALOR = [
    "Sos productor de seguros y tu organizacion te retiene comision en autos?\n\nEn Lumina te entregamos el 100% de la comision que liquida la aseguradora.\n\nCero retencion. Cero letra chica.",

    "El modelo tradicional de seguros:\n- Vos generas el cliente\n- Vos trabajas la venta\n- La aseguradora liquida comision\n- Tu organizacion se queda un 10-20%\n\nEl modelo Lumina:\n100% de comision en autos para vos.",

    "En Lumina no somos rentables morfando tus comisiones.\n\nSomos rentables con servicios opcionales: coworking, marketing digital, contabilidad.\n\nTu plata es tu plata.",

    "Comisiones en Lumina:\n\n- Automotores: 100% para el PAS\n- Resto de ramos: 97% para el PAS\n- Incentivos y overriders: 97% para el PAS\n\nEl 3% que retenemos cubre administracion. Nada mas.",

    "Un productor de seguros con plata en el bolsillo crece.\n\nY cuando crece, el ecosistema crece con el.\n\nPor eso cedemos el 100% en autos. Es logica, no caridad.",

    "Si tu organizacion se queda con parte de tus comisiones en autos... preguntate por que.\n\nEn Lumina entregamos el 100%. Sin retenciones. Sin excusas.",

    "100% de comision en automotores.\n97% en el resto de los ramos.\nTu cartera es tuya.\nSalida libre con 30 dias de preaviso.\n\nAsi funciona Lumina.",

    "Lumina no compite con vos. Compite por vos.\n\nPacto de no agresion comercial: tenemos prohibido vender seguros de forma directa o contactar a tus asegurados.\n\nTu cliente es tuyo. Punto.",
]

# --- SEGURIDAD Y CONFIANZA ---
TWEETS_CONFIANZA = [
    "\"Donde esta la trampa?\"\n\nEs la pregunta que mas nos hacen. Y tienen razon en desconfiar.\n\nLa respuesta: somos rentables con 3% en otros ramos + membresías opcionales.\n\nEn autos? 100% para vos.",

    "Tu cartera es tu propiedad tecnica y economica.\n\nEn Lumina lo reconocemos de forma irrevocable en el contrato. Salida libre con 30 dias de preaviso y traspaso de codigos garantizado.\n\nSin trabas. Sin retenciones.",

    "\"Tengo miedo de que se queden con mi cartera.\"\n\nEl miedo mas valido del mercado.\n\nPor eso blindamos todo en el contrato: clausula de no agresion, prohibicion de venta directa a tus asegurados, salida libre.\n\nTu cartera es tuya.",

    "No te pedimos que te mudes de organizacion hoy.\n\nSolo que los negocios nuevos que generes los codifiques con nosotros.\n\nProba la diferencia de rentabilidad sin riesgo. Si en 3 meses no ves el cambio, no perdiste nada.",

    "Pedi nuestro contrato y mandaselo a tu abogado.\n\nEs corto, sin letra chica, y tiene clausula de salida libre.\n\nSi te da el ok, empezamos. Si no, tan amigos.",
]

# --- LUMINA HUB ---
TWEETS_HUB = [
    "El Lumina Hub: un espacio disenado para que el productor de seguros profesionalice su imagen.\n\nCoworking premium + Media Hub con estudio de grabacion + salas de reuniones.\n\n$100 USD/mes. Sin contratos largos. Salida libre.",

    "Deja de reunirte con clientes corporativos en el bar de la esquina.\n\nEn el Lumina Hub tenes salas de reuniones equipadas, fibra optica y un entorno profesional.\n\nTu imagen vende. Invertila bien.",

    "Queres grabar contenido para redes pero no tenes estudio?\n\nEn el Media Hub del Lumina Hub tenes luces, microfonos y camara. Todo listo.\n\nLlegas, grabas, y publicamos. Sin reservar semanas ni pagar por hora.",

    "Programa 5x2: trae 5 productores al Hub y si se mantienen 2 meses activos, tu membresia queda bonificada.\n\nBasicamente $0 por tiempo indefinido.\n\nGanar-ganar.",
]

# --- SERVICIOS ON-DEMAND ---
TWEETS_SERVICIOS = [
    "Tu cabeza tiene que estar en vender, no en los impuestos.\n\nNuestra Unidad Contable Integral se encarga de tus recategorizaciones de Monotributo, liquidaciones de IVA y exigencias de AFIP/SSN.\n\n$50 USD/mes.",

    "Dejas de depender del boca a boca.\n\nNuestra Unidad de Performance Marketing disena, configura y optimiza tus campanas en Google Ads, Instagram y Facebook.\n\nLeads calificados directo a tu WhatsApp.\n\n$50 USD/mes.",

    "Servicios opcionales para miembros del Hub:\n\n- Contabilidad integral: $50 USD/mes\n- Marketing digital: $50 USD/mes\n\nVos decidis si los tomas o no. Sin obligacion.",
]

# --- EDUCATIVOS / INDUSTRIA ---
TWEETS_EDUCATIVOS = [
    "Dato: segun la Ley 22.400, el PAS es el unico intermediario habilitado para asesorar en seguros en Argentina.\n\nTu matricula tiene valor. No dejes que te paguen menos de lo que vale tu trabajo.",

    "Art. 56 de la Ley 17.418: si la aseguradora no se pronuncia dentro de los 30 dias de recibida la informacion complementaria del siniestro, se considera aceptado.\n\nConocer la ley es tu mejor herramienta.",

    "Plazos legales que todo PAS debe conocer:\n\n- Denuncia de siniestro: 3 dias\n- Pedido de informacion: 15 dias\n- Aceptacion/rechazo: 30 dias\n- Prescripcion: 1 ano\n\nFuente: Ley 17.418",

    "El mercado asegurador argentino necesita mas PAS independientes que piensen en grande.\n\nNo cadetes de organizaciones que se quedan con su plata.\n\nEl futuro es del productor empoderado.",

    "La diferencia entre un PAS que factura y uno que sobrevive no es la cantidad de polizas.\n\nEs cuanto de cada comision se queda en su bolsillo.\n\nRevisa tu esquema. Los numeros no mienten.",
]

# --- MOTIVACIONALES / MINDSET ---
TWEETS_MINDSET = [
    "No vendes seguros. Vendes tranquilidad.\n\nCuando lo entiendas, tu forma de cerrar cambia para siempre.",

    "El PAS que se capacita, vende mas.\nEl PAS que se profesionaliza, retiene mas.\nEl PAS que elige bien su organizacion, gana mas.\n\nEn ese orden.",

    "Si tu organizacion no crece cuando vos creces... es hora de evaluar si estas en el lugar correcto.",

    "Cross-selling: si tu cliente ya confio en vos para el auto, por que no para el hogar, la vida o el negocio?\n\nCada poliza nueva es comision pura sin costo de adquisicion.",

    "El mejor momento para cambiar de organizacion fue hace 5 anos.\n\nEl segundo mejor momento es hoy.",
]

# Todas las categorias agrupadas
ALL_CATEGORIES = {
    "valor": TWEETS_VALOR,
    "confianza": TWEETS_CONFIANZA,
    "hub": TWEETS_HUB,
    "servicios": TWEETS_SERVICIOS,
    "educativos": TWEETS_EDUCATIVOS,
    "mindset": TWEETS_MINDSET,
}

ALL_TWEETS = (
    TWEETS_VALOR
    + TWEETS_CONFIANZA
    + TWEETS_HUB
    + TWEETS_SERVICIOS
    + TWEETS_EDUCATIVOS
    + TWEETS_MINDSET
)
