#!/bin/bash

set -e

echo "Criando containers e infraestrutura..."
docker-compose down
sleep 2
docker-compose up --build -d

sleep 10

echo "Aguardando PostgreSQL iniciar..."
docker exec fire_postgres psql -U $POSTGRES_USER -d $POSTGRES_DB -c "SELECT 1"

echo "Ambiente iniciado com sucesso. Acesse o Airflow em http://localhost:8080 (login: admin/admin)"
