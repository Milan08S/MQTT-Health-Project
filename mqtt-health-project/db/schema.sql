CREATE ROLE iotuser WITH LOGIN PASSWORD 'iotpassword';
CREATE DATABASE healthdata OWNER iotuser ENCODING 'UTF8';
\connect healthdata;
CREATE TABLE health_readings (
  id SERIAL PRIMARY KEY,
  sensor_id TEXT NOT NULL,
  temperature NUMERIC NOT NULL,
  heart_rate INTEGER NOT NULL,
  blood_pressure TEXT NOT NULL,
  recorded_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX ON health_readings(recorded_at);
