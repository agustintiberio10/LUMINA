# 📑 Protocolo de Reporte de Siniestros Automotores

Este documento es la guía técnica para que el PAS recolecte la información necesaria y la envíe correctamente a la casilla oficial de la organización.

## ✉️ Destino del Reporte
* **Email:** siniestros@lumina-org.com
* **Asunto sugerido:** Siniestro - [Nombre del Asegurado] - [Patente] - [Compañía]

## 🛠️ Requisitos Obligatorios (El Checklist)

Para que el equipo de Siniestros de Lumina pueda procesar la denuncia, el PAS debe adjuntar o informar lo siguiente:

### 1. Datos del Asegurado y el Hecho
* **Fecha, hora y lugar exacto** del siniestro (Intersección, calle, localidad).
* **Relato circunstanciado:** Descripción breve de cómo ocurrió el hecho (quién circulaba por dónde, sentido de giro, velocidad estimada).
* **Daños propios:** Fotos claras de los daños del vehículo del asegurado.

### 2. Variables Agravantes (NUEVO)
* **¿Hubo Lesionados?:** En caso afirmativo (ya sea del asegurado, acompañantes o terceros), es de carácter **obligatorio** adjuntar la Denuncia Policial / Exposición Civil.
* **Testigos:** Nombre completo, DNI y teléfono de cualquier persona que haya presenciado el hecho (vital para disputas de responsabilidad).

### 3. Datos del Tercero (Vital para el Reclamo)
* **Datos Personales:** Nombre completo, DNI y teléfono de contacto.
* **Datos del Vehículo:** Marca, modelo y **Patente**.
* **Seguro del Tercero:** Nombre de la compañía aseguradora (fundamental para verificar solvencia y cobertura).
* **Licencia y Cédula:** Foto de la licencia de conducir del tercero y de la Cédula Verde/Título (ambos lados).

### 4. Evidencia Visual (Fotos obligatorias)
* **Posición de los vehículos:** Fotos de ambos autos tal como quedaron tras el impacto (antes de moverlos, si es seguro hacerlo).
* **Entorno:** Foto panorámica donde se vea la calle, semáforos o señales de tránsito (disco PARE, ceda el paso).

## ⏱️ Plazos Legales Críticos
* **Denuncia Administrativa:** Debe realizarse dentro de las **72 horas hábiles** de ocurrido el hecho o de que el asegurado haya tenido conocimiento (Art. 46 Ley 17.418).
* **Advertencia al PAS:** El bot debe recordar siempre al PAS que el incumplimiento de este plazo faculta a la aseguradora a declinar el siniestro por extemporáneo.

## 🤖 Instrucción para la IA (Acción del Bot)
Cuando un PAS consulte por un choque, el bot deberá:
1.  **Triage de Gravedad:** Lo primero que debe preguntar el bot es: *"¿Hubo heridos o intervención policial?"* para determinar la urgencia del caso.
2.  **Escuchar y Explicar:** Explicar con tono protector pero firme por qué se necesita cada dato (para evitar rechazos y ganar el reclamo de RC).
3.  **Redactar Borrador:** Una vez que el PAS provea los datos, el bot redactará el cuerpo del mail estructurado y listo para que el PAS lo copie y envíe a `siniestros@lumina-org.com`.
