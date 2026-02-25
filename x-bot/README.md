# LUMINA X Bot

Bot de publicacion automatica para X (Twitter) que difunde la propuesta de valor de LUMINA para captar Productores Asesores de Seguros (PAS).

## Que hace

- Publica tweets automaticos sobre LUMINA con contenido categorizado (propuesta de valor, confianza, Hub, servicios, educativos, mindset)
- Respeta un horario de publicacion configurable (default: 9:00 a 22:00 hora Argentina)
- Rota el contenido sin repetir tweets hasta agotar el banco completo
- Modo DRY_RUN para testear sin publicar

## Contenido

El bot tiene **30+ tweets** organizados en 6 categorias:

| Categoria | Descripcion |
|---|---|
| `valor` | Propuesta de valor core: 100% comision autos, 97% otros ramos |
| `confianza` | Objeciones comunes, contratos, seguridad de cartera |
| `hub` | Lumina Hub: coworking, Media Hub, networking |
| `servicios` | Contabilidad y marketing on-demand |
| `educativos` | Datos legales, plazos, industria de seguros |
| `mindset` | Mentalidad, motivacion para productores |

---

## Setup paso a paso

### 1. Configurar la API de X (Developer Portal)

Este es el paso mas importante. Segui estas instrucciones al pie de la letra:

#### a) Crear cuenta de desarrollador

1. Ir a https://developer.x.com/en/portal/dashboard
2. Si no tenes cuenta de desarrollador, completar el formulario de registro
3. Seleccionar el plan **Free** (permite 1,500 tweets/mes - suficiente para el bot)

#### b) Crear un PROYECTO (esto es obligatorio desde 2023)

**IMPORTANTE:** X requiere que tu app este dentro de un Proyecto. Sin Proyecto, la API devuelve error 403.

1. En el Developer Portal, ir a la seccion **"Projects & Apps"** en el menu lateral izquierdo
2. Click en **"+ New Project"** (o "Add Project")
3. Completar:
   - **Project Name:** `LUMINA Bot` (o el nombre que quieras)
   - **Use case:** Seleccionar "Making a bot"
   - **Project description:** "Bot de publicacion automatica de contenido para LUMINA"
4. Confirmar la creacion del proyecto

> **Si no ves el boton "New Project":** Es posible que ya tengas un proyecto con una app standalone. En ese caso:
> - Busca tu app existente en "Projects & Apps"
> - Si esta fuera de un proyecto (aparece como "Standalone App"), necesitas eliminarla y recrearla dentro de un proyecto
> - Alternativamente, en algunos casos podes arrastrar/migrar la app al proyecto desde el dashboard

#### c) Crear una App dentro del Proyecto

1. Despues de crear el proyecto, te pedira crear una App
2. **App name:** `lumina-x-bot` (debe ser unico en toda la plataforma de X)
3. Guardar las **API Key** y **API Key Secret** que te muestra (son las Consumer Keys)

#### d) Configurar permisos de la App

1. Ir a tu App > **Settings**
2. En **"User authentication settings"**, click en **"Set up"**
3. Configurar:
   - **App permissions:** Seleccionar **"Read and Write"** (NO solo Read)
   - **Type of App:** "Web App, Automated App or Bot"
   - **Callback URL:** `https://localhost` (no lo usamos pero es obligatorio)
   - **Website URL:** `https://lumina.com.ar` (o tu sitio)
4. Guardar

#### e) Generar Access Token y Secret

**CRITICO: Hacer esto DESPUES de configurar permisos Read and Write.**
Si generaste los tokens antes de poner Read and Write, tenes que regenerarlos.

1. Ir a tu App > **"Keys and Tokens"**
2. En la seccion **"Access Token and Secret"**, click en **"Regenerate"**
3. Guardar el **Access Token** y **Access Token Secret**

Ahora tenes las 4 claves necesarias:
- API Key (Consumer Key)
- API Key Secret (Consumer Secret)
- Access Token
- Access Token Secret

### 2. Instalar dependencias

```bash
cd x-bot
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

```bash
cp .env.example .env
```

Editar `.env` con tus credenciales:

```
X_API_KEY=tu_api_key_real
X_API_SECRET=tu_api_secret_real
X_ACCESS_TOKEN=tu_access_token_real
X_ACCESS_TOKEN_SECRET=tu_access_token_secret_real
```

### 4. Probar en modo DRY RUN

Antes de publicar de verdad, testear que todo funcione:

```bash
# En .env, poner DRY_RUN=true

# Ver un preview del siguiente tweet
python bot.py preview

# Simular una publicacion
python bot.py post

# Ver estadisticas
python bot.py stats
```

### 5. Publicar de verdad

```bash
# En .env, cambiar a DRY_RUN=false

# Publicar un tweet individual
python bot.py post

# O publicar de una categoria especifica
python bot.py post --category valor
```

### 6. Ejecutar el scheduler (publicacion continua)

```bash
python scheduler.py
```

El scheduler:
- Publica un tweet al iniciar
- Luego publica cada N horas (configurable con `TWEET_INTERVAL_HOURS`)
- Solo publica dentro del horario configurado
- Se detiene con Ctrl+C

---

## Uso del CLI

```bash
# Publicar el siguiente tweet
python bot.py post

# Publicar de una categoria especifica
python bot.py post --category hub

# Ver preview sin publicar
python bot.py preview

# Ver estadisticas de publicacion
python bot.py stats

# Iniciar publicacion automatica continua
python scheduler.py
```

## Configuracion

Todas las opciones se configuran via `.env`:

| Variable | Default | Descripcion |
|---|---|---|
| `TWEET_INTERVAL_HOURS` | 4 | Horas entre cada tweet |
| `PUBLISH_HOUR_START` | 9 | Hora de inicio de publicacion |
| `PUBLISH_HOUR_END` | 22 | Hora de fin de publicacion |
| `TIMEZONE` | America/Argentina/Buenos_Aires | Zona horaria |
| `DRY_RUN` | false | Si es true, solo imprime sin publicar |

## Estructura de archivos

```
x-bot/
├── .env.example      # Template de credenciales
├── .env              # Tus credenciales (no se commitea)
├── requirements.txt  # Dependencias Python
├── config.py         # Carga de configuracion
├── content.py        # Banco de 30+ tweets por categoria
├── bot.py            # Bot principal (publicar, preview, stats)
├── scheduler.py      # Publicacion automatica programada
├── tweet_history.json # Historial de tweets publicados (auto-generado)
└── README.md         # Este archivo
```

## Troubleshooting

### Error 403 Forbidden
- Tu app NO esta dentro de un Proyecto en el Developer Portal
- O los permisos de la app no incluyen "Write"
- Solucion: seguir los pasos de setup del punto 1

### Error 401 Unauthorized
- Credenciales invalidas
- Regenera los tokens en el Developer Portal

### Error 429 Too Many Requests
- Excediste el rate limit del plan Free (1,500 tweets/mes)
- Espera o upgradea tu plan

### Los tokens no funcionan despues de cambiar permisos
- Si cambiaste de "Read" a "Read and Write", DEBES regenerar los tokens
- Los tokens viejos siguen con los permisos anteriores

## Agregar nuevos tweets

Editar `content.py` y agregar tweets a la lista correspondiente. Cada tweet debe respetar el limite de 280 caracteres.
