# Inicialización de la base de datos

## Con Docker‑Compose
El servicio `db` monta este script en `/docker-entrypoint-initdb.d/`, se ejecuta la primera vez que arranca Postgres.

## Manual
sudo -u postgres psql
\i schema.sql
\l
\c healthdata
\dt