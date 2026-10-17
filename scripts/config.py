import os
from dotenv import load_dotenv

load_dotenv()

# Konfigurasi Database PostgreSQL
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "weather_dwh")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

# 20 Kota Strategis di Indonesia
CITIES = [
    # Pulau Jawa
    {"city_name": "Jakarta", "province": "DKI Jakarta", "island_group": "Jawa", "latitude": -6.2088, "longitude": 106.8456},
    {"city_name": "Surabaya", "province": "Jawa Timur", "island_group": "Jawa", "latitude": -7.2575, "longitude": 112.7521},
    {"city_name": "Bandung", "province": "Jawa Barat", "island_group": "Jawa", "latitude": -6.9175, "longitude": 107.6191},
    {"city_name": "Bogor", "province": "Jawa Barat", "island_group": "Jawa", "latitude": -6.5971, "longitude": 106.8060},
    {"city_name": "Semarang", "province": "Jawa Tengah", "island_group": "Jawa", "latitude": -6.9667, "longitude": 110.4167},
    {"city_name": "Yogyakarta", "province": "DI Yogyakarta", "island_group": "Jawa", "latitude": -7.7956, "longitude": 110.3695},

    # Sumatera
    {"city_name": "Medan", "province": "Sumatera Utara", "island_group": "Sumatera", "latitude": 3.5952, "longitude": 98.6722},
    {"city_name": "Palembang", "province": "Sumatera Selatan", "island_group": "Sumatera", "latitude": -2.9761, "longitude": 104.7754},
    {"city_name": "Padang", "province": "Sumatera Barat", "island_group": "Sumatera", "latitude": -0.9471, "longitude": 100.4172},
    {"city_name": "Banda Aceh", "province": "Aceh", "island_group": "Sumatera", "latitude": 5.5483, "longitude": 95.3238},

    # Kalimantan
    {"city_name": "Balikpapan", "province": "Kalimantan Timur", "island_group": "Kalimantan", "latitude": -1.2379, "longitude": 116.8529},
    {"city_name": "Pontianak", "province": "Kalimantan Barat", "island_group": "Kalimantan", "latitude": -0.0263, "longitude": 109.3425},
    {"city_name": "Banjarmasin", "province": "Kalimantan Selatan", "island_group": "Kalimantan", "latitude": -3.3194, "longitude": 114.5908},

    # Sulawesi
    {"city_name": "Makassar", "province": "Sulawesi Selatan", "island_group": "Sulawesi", "latitude": -5.1477, "longitude": 119.4327},
    {"city_name": "Manado", "province": "Sulawesi Utara", "island_group": "Sulawesi", "latitude": 1.4748, "longitude": 124.8421},

    # Bali & Nusa Tenggara
    {"city_name": "Denpasar", "province": "Bali", "island_group": "Bali-Nusa Tenggara", "latitude": -8.6705, "longitude": 115.2126},
    {"city_name": "Mataram", "province": "Nusa Tenggara Barat", "island_group": "Bali-Nusa Tenggara", "latitude": -8.5833, "longitude": 116.1167},
    {"city_name": "Kupang", "province": "Nusa Tenggara Timur", "island_group": "Bali-Nusa Tenggara", "latitude": -10.1772, "longitude": 123.6070},

    # Maluku & Papua
    {"city_name": "Ambon", "province": "Maluku", "island_group": "Maluku-Papua", "latitude": -3.6547, "longitude": 128.1906},
    {"city_name": "Jayapura", "province": "Papua", "island_group": "Maluku-Papua", "latitude": -2.5489, "longitude": 140.7137},
]
