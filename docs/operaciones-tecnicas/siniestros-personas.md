# 🎖️ Protocolo de Siniestros: Seguros de Personas (Vida y AP)

Este protocolo rige para Vida Individual, Vida Colectivo, Sepelio y Accidentes Personales (fallecimiento o invalidez). El bot debe actuar con máxima celeridad, precisión técnica y empatía.

## ✉️ Canal de Reporte Prioritario
* **Email:** siniestros@lumina-org.com
* **Asunto:** URGENTE - Vida/Personas - [Nombre del Asegurado] - [DNI]

## 🛠️ Requerimientos según el Evento

### 1. Fallecimiento (Vida / Sepelio / AP)
* **Certificado de Defunción:** Copia legalizada del acta o certificado de defunción.
* **Muerte Natural:** Historia clínica o informe del médico tratante indicando la causa (fundamental para descartar enfermedades preexistentes no declaradas).
* **Muerte Accidental (NUEVO):** Copia de las actuaciones policiales (Sumario/Causa Penal) y resultado de la autopsia si la hubiere. Las compañías exigen esto para descartar dolo, suicidio o exclusiones (ej: alcoholemia).
* **Documentación del Beneficiario:** DNI y constancia de CUIL de los beneficiarios designados.
* **CBU de los Beneficiarios:** Para la transferencia directa de la indemnización.

### 2. Invalidez Total o Parcial (Vida / AP)
* **Formulario de Denuncia:** Formulario específico de la compañía firmado por el asegurado y el médico tratante.
* **Dictamen de Junta Médica:** Documento oficial que indique el grado de incapacidad (porcentaje).
* **Historia Clínica y Alta Médica:** Completa, desde el inicio del evento hasta la consolidación de la lesión (Alta).
* **Estudios Complementarios:** Radiografías, resonancias o informes que respalden la incapacidad.

### 3. Accidentes Personales (Reintegro de Gastos Médicos)
* **Facturas Originales:** De farmacia, ortopedia o centros médicos (a nombre del asegurado, facturas B o C válidas por AFIP).
* **Recetarios:** Órdenes médicas que justifican la compra de medicamentos o estudios.

## ⚖️ Consideraciones Legales de Lumina
* **Liberación de Secreto Médico (NUEVO):** El bot debe indicar al PAS que los beneficiarios deberán firmar el formulario de "Relevo de Secreto Médico" para que la compañía pueda auditar la historia clínica sin trabas legales.
* **Beneficiarios y Sucesión:** Recordar al PAS que, si no hay beneficiarios designados explícitamente en póliza, se requerirá la Declaratoria de Herederos (proceso judicial judicial que demora el cobro).
* **Prescripción (NUEVO):** Recordar que en los seguros de Vida, el plazo de prescripción es de 3 años (Art. 50 Ley 17.418), pero la denuncia administrativa debe hacerse a la brevedad para no demorar la asistencia a la familia.

## 🤖 Instrucción para la IA (Acción del Bot)
Ante estos casos, el bot de Lumina debe:
1.  **Priorizar la Empatía:** Usar frases de apoyo ("Lamento mucho la situación de tu cliente, vamos a resolver esto lo más rápido posible") y evitar un tono puramente burocrático.
2.  **Triage Inmediato:** Preguntar obligatoriamente: *"¿El fallecimiento fue por causas naturales o por un accidente?"* para saber si debe pedir la actuación policial.
3.  **Claridad Total:** No dejar dudas sobre los documentos; redactar el checklist exacto para que el PAS se lo reenvíe a la familia. Un error aquí retrasa meses el pago.
