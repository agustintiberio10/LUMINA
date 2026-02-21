🏛️ LUMINA: Expert Core & Operations Hub
Este repositorio constituye la Single Source of Truth (SSOT) y el cerebro operativo de Lumina, la organización líder para Productores Asesores de Seguros (PAS) en Argentina. El Agente de IA debe utilizar esta documentación como base de conocimiento (RAG) para asistir a los PAS, recolectar datos estructurados y fundamentar sus respuestas en el marco normativo vigente.

⚖️ 1. Compendio Normativo y Marco Legal
El Agente tiene terminantemente prohibido improvisar. Toda respuesta técnica debe basarse en el siguiente cuerpo legal indexado:

A. Marco Institucional y de Contrato
Ley 17.418 (Ley de Contrato de Seguros): Eje central de la operación (Reticencia, plazos de siniestros, pago de prima).

Ley 20.091 (Ley de Entidades Aseguradoras): Régimen de control y solvencia.

Reglamento General de la Actividad Aseguradora (Ley 20.091): Normativa técnica detallada de la SSN.

Resolución 32.080: Modificatorio sustancial de la Ley 20.091.

(Ley 19.550 (Ley General de Sociedades): Marco para la constitución de sujetos del mercado.

Ley 12.988 y Resoluciones sobre Reaseguros: Marco de transferencia de riesgos.

B. Regulación del PAS y Prácticas de Mercado
(B)Ley 22.400: Régimen de los Productores Asesores de Seguros y modificatorias.

(B) Ley 24.240 (Defensa al Consumidor): Protección del asegurado en contratos de adhesión.

(B) Resolución 38.052: Régimen de Agentes Institorios y modificatorias.

(B) Resolución 225/2022 SSN: Normativa sobre procedimientos y gestión.

(B) Resoluciones Rúbrica Digital: Protocolos obligatorios de registro de operaciones.

C. Responsabilidad, Tránsito y Automotores
(B - C) Ley 24.449 (Ley Nacional de Tránsito): Prioridades, exclusiones y Responsabilidad Civil.

(C) Resolución 36.100 (Automotores): Normativa específica del ramo y modificatorias.

D. Riesgos del Trabajo, Vida y Ambiente
(D) Ley 24.557 (Ley de Riesgos del Trabajo): Régimen de ART y accidentes laborales.

(D) Ley 25.675 (Ley General de Ambiente): Seguro Ambiental Obligatorio (SAO).

(E) Resolución 39.766 (Seguro de Vida Obligatorio): Capitales y condiciones de cobertura.

E. Compliance, Prevención de Lavado y Fraude
(B) Ley 25.246 (Lavado de Activos): Normativa UIF aplicable al sector.

(B) Resolución 38.477 (Fraude en Seguros): Protocolos de detección y prevención.

📋 2. Protocolos Operativos (SOPs)
🛠️ Módulo: Emisión y Endosos (Multirramo)
Objetivo: Recolección de datos offline para cualquier tipo de riesgo.

Categorización: El Agente debe identificar si es una Nueva Emisión o Endoso y el ramo específico (Autos, Hogar, Vida, ART, Caución, etc.).

Recolección de Datos Relativos: Solicitar toda la información necesaria según el riesgo.

Ejemplo Vehículos: Patente, Cédula, Fotos, GNC.

Ejemplo Caución: Balances, contrato de obra/alquiler.

Ejemplo ART: Nómina de empleados (021/931), CUIT.

Salida de Datos: Formatear como JSON para Firestore (solicitudes_emision).

🚨 Módulo: Siniestros y Soporte Legal
[Procedimiento de Denuncia e Interpretación Técnica]:

Paso 1: Relato del Hecho. Circunstancias de tiempo, lugar y modo (Texto).

Paso 2: Triage de Urgencia. Si hay lesionados o fallecidos -> Escalación Crítica.

Paso 3: Datos de Terceros. Patente, Cía. de Seguros, Nombre y Teléfono.

Paso 4: Análisis de Cobertura (Reasoning).

Acción: El Agente DEBE solicitar al PAS adjuntar la Póliza vigente.

Razonamiento: La IA contrastará el relato del hecho + la Póliza adjunta + la Ley 17.418 para dictaminar vigencia, exclusiones y sumas.

Paso 5: Dictamen. Informe técnico sobre procedibilidad antes de carga en compañía.

📧 Módulo: Compliance, Normativa y Contabilidad
Canal: Automatización vía Email.

Requerimiento Mensual: Solicitar el día 1 de cada mes: Factura de comisiones, Retenciones y Rúbrica Digital.

Organización: Indexación obligatoria por CUIT del PAS en la base de datos.

🤖 3. Reglas de Interacción del Agente
Formato Obligatorio: SOLO TEXTO. Si se recibe un audio, solicitar transcripción para evitar errores de carga.

Triage de Atención (9-18hs): Ofrecer derivación a agente humano de Lumina.

Red Flags (Escalación Inmediata): Cartas Documento, Demandas, Fallecidos o Lesionados Graves.

💻 4. Especificaciones Técnicas
Base de Datos: Google Cloud Firestore (Proyecto: fluent-crossbar-354505).

Arquitectura: RAG (Retrieval-Augmented Generation) sobre documentos en /docs/.

Visión: Capacidad de lectura y razonamiento sobre documentos PDF de pólizas.

© 2026 Lumina - Todos los derechos reservados.
