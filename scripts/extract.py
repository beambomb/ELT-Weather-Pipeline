import logging
from datetime import datetime, timezone
import requests
from scripts.config import OPEN_METEO_URL, CITIES

logger = logging.getLogger(__name__)


def fetch_weather_for_city(city: dict) -> dict:
    """Ambil data cuaca per jam untuk satu kota."""
    params = {
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "wind_speed_10m",
        ],
        "timezone": "Asia/Jakarta",
        "forecast_days": 1,
    }

    logger.info("Fetch cuaca: %s (%s)", city["city_name"], city["province"])
    response = requests.get(OPEN_METEO_URL, params=params, timeout=10)
    response.raise_for_status()

    return {
        "city_name": city["city_name"],
        "province": city["province"],
        "island_group": city["island_group"],
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "payload": response.json(),
    }


def extract_all_cities() -> list[dict]:
    """Ekstraksi data untuk seluruh 20 kota."""
    results = []
    for city in CITIES:
        try:
            results.append(fetch_weather_for_city(city))
        except requests.RequestException as e:
            logger.error("Gagal menarik data %s: %s", city["city_name"], e)
            raise
    return results
