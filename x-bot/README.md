# LUMINA X Bot

Bot de publicacion automatica para X (Twitter) que difunde la propuesta de valor de LUMINA para captar Productores Asesores de Seguros (PAS).

## Que hace

- **Publica tweets** automaticos cada 20 min (9:00-22:00 AR) con hashtags #seguros #productordeseguros #pas
- **Scrapea noticias** de 100seguro.com.ar 1 vez al dia (11:00 AM) y las publica filtradas por relevancia
- **Responde menciones** cada 5 min con base de conocimiento de 32 temas de seguros
- **Sigue automaticamente** a quien mencione al bot
- **Invita a www.lumina-org.com** solo 1 vez por usuario
- Se reinicia solo si se cae. Arranca automatico al encender el servidor.

## Contenido

**36 tweets** organizados en 6 categorias:

| Categoria | Descripcion |
|---|---|
| `valor` | Propuesta de valor: 100% comision autos, 97% otros ramos |
| `confianza` | Contratos, seguridad de cartera, objeciones |
| `hub` | Lumina Hub: coworking, Media Hub, networking |
| `servicios` | Contabilidad y marketing on-demand |
| `educativos` | Datos legales, plazos, industria de seguros |
| `crecimiento` | Oportunidad y mentalidad para productores |

**32 temas de respuesta** a consultas (LUMINA + seguros general):
Comisiones, cartera, Hub, marketing, contabilidad, siniestros, plazos legales, Ley 17.418, Ley 22.400, ART, franquicia, infraseguro, subrogacion, caucion, fraude, cross-selling, etc.

---

## Instalacion rapida (servidor/VPS)

### 1. Configurar credenciales de X

Seguir las instrucciones de la seccion "Setup de API de X" mas abajo.

### 2. Instalar como servicio automatico

```bash
cd x-bot
cp .env.example .env
nano .env  # completar con tus credenciales

sudo bash install.sh
```

Listo. El bot:
- Arranca automaticamente al encender el servidor
- Se reinicia solo si se cae (en 30 segundos)
- Logs en: `sudo journalctl -u lumina-bot -f`

### Comandos utiles

```bash
sudo systemctl status lumina-bot    # ver estado
sudo journalctl -u lumina-bot -f    # ver logs en vivo
sudo systemctl stop lumina-bot      # detener
sudo systemctl start lumina-bot     # iniciar
sudo systemctl restart lumina-bot   # reiniciar
sudo nano /opt/lumina-bot/.env      # editar config
```

---

## Setup de API de X (Developer Portal)

### a) Crear cuenta de desarrollador

1. Ir a https://developer.x.com/en/portal/dashboard
2. Si no tenes cuenta de desarrollador, completar el formulario de registro
3. Seleccionar el plan **Free** (permite 1,500 tweets/mes - suficiente para el bot)

### b) Crear un PROYECTO

**IMPORTANTE:** X requiere que tu app este dentro de un Proyecto. Sin Proyecto, la API devuelve error 403.

1. En el Developer Portal, ir a **"Projects & Apps"**
2. Click en **"+ New Project"**
3. Completar:
   - **Project Name:** `LUMINA Bot`
   - **Use case:** "Making a bot"
   - **Description:** "Bot de publicacion automatica de contenido para LUMINA"

### c) Crear una App dentro del Proyecto

1. Despues de crear el proyecto, crear una App
2. **App name:** `lumina-x-bot` (debe ser unico en X)
3. Guardar las **API Key** y **API Key Secret**

### d) Configurar permisos

1. Ir a tu App > **Settings** > **"User authentication settings"** > **"Set up"**
2. Configurar:
   - **App permissions:** **"Read and Write"** (NO solo Read)
   - **Type of App:** "Web App, Automated App or Bot"
   - **Callback URL:** `https://localhost`
   - **Website URL:** `https://lumina-org.com`

### e) Generar Access Token y Secret

**CRITICO: Hacer esto DESPUES de configurar permisos Read and Write.**

1. Ir a tu App > **"Keys and Tokens"**
2. **"Access Token and Secret"** > **"Regenerate"**
3. Guardar el **Access Token** y **Access Token Secret**

---

## Modo manual (sin instalar como servicio)

```bash
cd x-bot
pip install -r requirements.txt
cp .env.example .env
nano .env  # completar credenciales

# Probar sin publicar
DRY_RUN=true python scheduler.py

# Produccion
python scheduler.py
```

### CLI

```bash
python bot.py post                     # publicar siguiente tweet
python bot.py post --category valor    # publicar de una categoria
python bot.py preview                  # ver preview sin publicar
python bot.py stats                    # ver estadisticas
python news_scraper.py                 # testear scraper de noticias
python responder.py                    # testear respuestas a consultas
```

---

## Configuracion

Todas las opciones via `.env`:

| Variable | Default | Descripcion |
|---|---|---|
| `TWEET_INTERVAL_MINUTES` | 20 | Minutos entre cada tweet |
| `PUBLISH_HOUR_START` | 9 | Hora de inicio de publicacion |
| `PUBLISH_HOUR_END` | 22 | Hora de fin de publicacion |
| `TIMEZONE` | America/Argentina/Buenos_Aires | Zona horaria |
| `DRY_RUN` | false | Si es true, solo imprime sin publicar |
| `MENTIONS_CHECK_MINUTES` | 5 | Cada cuantos minutos chequear menciones |
| `MENTIONS_MAX_RESULTS` | 10 | Menciones a procesar por chequeo |

## Estructura de archivos

```
x-bot/
├── bot.py              # Motor: publica tweets + hashtags
├── content.py          # 36 tweets en 6 categorias
├── news_scraper.py     # Scraper 100seguro.com.ar con cache diario
├── mentions.py         # Monitor menciones + follow + auto-reply
├── responder.py        # Base de conocimiento (32 temas) + replies
├── scheduler.py        # Scheduler: tweets, noticias, menciones + logging
├── config.py           # Configuracion desde .env
├── .env.example        # Template de credenciales
├── requirements.txt    # Dependencias Python
├── install.sh          # Instalador como servicio de systemd
├── lumina-bot.service  # Archivo de servicio systemd
└── logs/               # Logs del bot (auto-generado)
```

## Troubleshooting

### Error 403 Forbidden
- Tu app NO esta dentro de un Proyecto en el Developer Portal
- O los permisos de la app no incluyen "Write"

### Error 401 Unauthorized
- Credenciales invalidas. Regenera los tokens.

### Error 429 Too Many Requests
- Excediste el rate limit del plan Free (1,500 tweets/mes)

### Los tokens no funcionan despues de cambiar permisos
- Si cambiaste de "Read" a "Read and Write", DEBES regenerar los tokens
