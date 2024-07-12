#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <number_of_bots>"
  exit 1
fi

NUM_BOTS=$1

# Crear un archivo docker-compose.override.yml con el número de bots
echo "version: '3'" > docker-compose.override.yml
echo "" >> docker-compose.override.yml
echo "services:" >> docker-compose.override.yml
echo "  app:" >> docker-compose.override.yml
echo "    scale: ${NUM_BOTS}" >> docker-compose.override.yml

# Levantar los servicios de docker-compose con la escala especificada
docker-compose up -d --scale app=${NUM_BOTS}
