{{ config(materialized='table') }}

SELECT DISTINCT
    MD5(city_name) AS location_id,
    city_name,
    province,
    island_group,
    latitude,
    longitude
FROM {{ ref('stg_weather_measurements') }}
