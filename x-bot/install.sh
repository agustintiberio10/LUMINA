#!/bin/bash
# ============================================================
# Script de instalacion del LUMINA X Bot
#
# Instala el bot como servicio de systemd para que arranque
# solo al encender el servidor y se reinicie si se cae.
#
# Uso:
#   sudo bash install.sh
#
# Despues de instalar:
#   sudo systemctl status lumina-bot   (ver estado)
#   sudo journalctl -u lumina-bot -f   (ver logs en vivo)
#   sudo systemctl stop lumina-bot     (detener)
#   sudo systemctl start lumina-bot    (iniciar)
#   sudo systemctl restart lumina-bot  (reiniciar)
# ============================================================

set -e

INSTALL_DIR="/opt/lumina-bot"
SERVICE_NAME="lumina-bot"
BOT_USER="lumina"

echo "========================================="
echo " Instalando LUMINA X Bot"
echo "========================================="

# 1. Crear usuario del sistema si no existe
if ! id "$BOT_USER" &>/dev/null; then
    echo "[1/6] Creando usuario '$BOT_USER'..."
    useradd --system --no-create-home --shell /usr/sbin/nologin "$BOT_USER"
else
    echo "[1/6] Usuario '$BOT_USER' ya existe."
fi

# 2. Copiar archivos al directorio de instalacion
echo "[2/6] Copiando archivos a $INSTALL_DIR..."
mkdir -p "$INSTALL_DIR"
cp -r ./*.py "$INSTALL_DIR/"
cp requirements.txt "$INSTALL_DIR/"

# 3. Verificar que exista el .env
if [ ! -f "$INSTALL_DIR/.env" ]; then
    if [ -f .env ]; then
        cp .env "$INSTALL_DIR/.env"
        echo "  .env copiado desde directorio actual."
    else
        cp .env.example "$INSTALL_DIR/.env"
        echo ""
        echo "  ATENCION: Se copio .env.example como .env"
        echo "  Edita $INSTALL_DIR/.env con tus credenciales:"
        echo "    sudo nano $INSTALL_DIR/.env"
        echo ""
    fi
fi

# 4. Crear entorno virtual e instalar dependencias
echo "[3/6] Creando entorno virtual..."
python3 -m venv "$INSTALL_DIR/venv"
"$INSTALL_DIR/venv/bin/pip" install --quiet --upgrade pip
echo "[4/6] Instalando dependencias..."
"$INSTALL_DIR/venv/bin/pip" install --quiet -r "$INSTALL_DIR/requirements.txt"

# 5. Ajustar permisos
echo "[5/6] Ajustando permisos..."
chown -R "$BOT_USER":"$BOT_USER" "$INSTALL_DIR"
chmod 600 "$INSTALL_DIR/.env"

# 6. Instalar y activar servicio de systemd
echo "[6/6] Instalando servicio de systemd..."
cp lumina-bot.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable "$SERVICE_NAME"
systemctl start "$SERVICE_NAME"

echo ""
echo "========================================="
echo " LUMINA X Bot instalado correctamente"
echo "========================================="
echo ""
echo " Estado:    sudo systemctl status $SERVICE_NAME"
echo " Logs:      sudo journalctl -u $SERVICE_NAME -f"
echo " Detener:   sudo systemctl stop $SERVICE_NAME"
echo " Reiniciar: sudo systemctl restart $SERVICE_NAME"
echo " Config:    sudo nano $INSTALL_DIR/.env"
echo ""
echo " El bot arranca automaticamente al encender el servidor."
echo " Si se cae, se reinicia solo en 30 segundos."
echo "========================================="
