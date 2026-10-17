{{ config(materialized='table') }}

SELECT
    MD5(city_name || '-' || reading_time::text) AS reading_id,
    MD5(city_name) AS location_id,
    TO_CHAR(reading_time, 'YYYYMMDDHH24')::bigint AS date_id,
    reading_time,
    temperature_c,
    relative_humidity_pct,
    precipitation_mm,
    wind_speed_kmh,
    extracted_at
FROM {{ ref('stg_weather_measurements') }}
