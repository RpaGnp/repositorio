#!/bin/bash

# Ruta al directorio del entorno virtual
ENV_DIR="/home/SystemGNP/OperacionCND/CNDWeb/CrmCND/"

# Activa el entorno virtual
source "${ENV_DIR}/bin/activate"

# Ruta al archivo app.py
APP_PATH="${ENV_DIR}/src/app.py"

# Ejecuta el archivo app.py en segundo plano
nohup python3.8 "$APP_PATH" > /dev/null 2>&1 &
