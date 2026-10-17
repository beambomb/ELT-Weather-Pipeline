{{ config(materialized='table') }}

WITH distinct_timestamps AS (
    SELECT DISTINCT reading_time
    FROM {{ ref('stg_weather_measurements') }}
)

SELECT
    TO_CHAR(reading_time, 'YYYYMMDDHH24')::bigint AS date_id,
    reading_time,
    reading_time::date AS full_date,
    EXTRACT(HOUR FROM reading_time)::int AS hour_of_day,
    TRIM(TO_CHAR(reading_time, 'Day')) AS day_name,
    EXTRACT(DOW FROM reading_time)::int AS day_of_week,
    EXTRACT(DAY FROM reading_time)::int AS day_of_month,
    TRIM(TO_CHAR(reading_time, 'Month')) AS month_name,
    EXTRACT(MONTH FROM reading_time)::int AS month_number,
    EXTRACT(YEAR FROM reading_time)::int AS year,
    CASE 
        WHEN EXTRACT(DOW FROM reading_time) IN (0, 6) THEN TRUE 
        ELSE FALSE 
    END AS is_weekend
FROM distinct_timestamps
ORDER BY reading_time
