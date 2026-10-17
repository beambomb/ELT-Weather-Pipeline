import logging
from datetime import datetime, timezone
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from scripts.config import OPEN_METEO_URL, CITIES

logger = logging.getLogger(__name__)


def get_http_session() -> requests.Session:
    """Membuat session HTTP dengan connection pooling dan retry otomatis."""
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,  # jeda 1s, 2s, 4s antar percobaan ulang
        status_forcelist=[429, 500, 502, 503, 504],
        raise_on_status=False
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def fetch_weather_for_city(city: dict, session: requests.Session) -> dict:
    """Ambil data cuaca per jam untuk satu kota menggunakan session aktif."""
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
    response = session.get(OPEN_METEO_URL, params=params, timeout=(5, 20))
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
    """Ekstraksi data seluruh kota dengan connection pooling & retry."""
    results = []
    with get_http_session() as session:
        for city in CITIES:
            try:
                results.append(fetch_weather_for_city(city, session))
            except requests.RequestException as e:
                logger.error("Gagal menarik data %s setelah retry: %s", city["city_name"], e)
                raise
    return results


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )
    print("Mulai ekstraksi 20 kota dengan connection pooling & retry...")
    data = extract_all_cities()
    print(f"\nSukses! Berhasil menarik data {len(data)} kota.")
