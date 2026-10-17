{{ config(materialized='view') }}

WITH unnested_readings AS (
    SELECT
        id AS raw_payload_id,
        city_name,
        province,
        island_group,
        latitude,
        longitude,
        extracted_at,
        (time_elem)::timestamp AS reading_time,
        (payload->'hourly'->'temperature_2m'->>((ord - 1)::int))::numeric(4, 1) AS temperature_c,
        (payload->'hourly'->'relative_humidity_2m'->>((ord - 1)::int))::numeric(5, 1) AS relative_humidity_pct,
        (payload->'hourly'->'precipitation'->>((ord - 1)::int))::numeric(5, 2) AS precipitation_mm,
        (payload->'hourly'->'wind_speed_10m'->>((ord - 1)::int))::numeric(5, 2) AS wind_speed_kmh
    FROM {{ source('raw', 'raw_weather_payloads') }},
    jsonb_array_elements_text(payload->'hourly'->'time') WITH ORDINALITY AS t(time_elem, ord)
),

deduplicated AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY city_name, reading_time 
            ORDER BY extracted_at DESC
        ) AS row_num
    FROM unnested_readings
)

SELECT
    raw_payload_id,
    city_name,
    province,
    island_group,
    latitude,
    longitude,
    reading_time,
    temperature_c,
    relative_humidity_pct,
    precipitation_mm,
    wind_speed_kmh,
    extracted_at
FROM deduplicated
WHERE row_num = 1
