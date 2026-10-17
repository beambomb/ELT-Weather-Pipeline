import logging
import psycopg2
from psycopg2.extras import Json
from scripts.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

logger = logging.getLogger(__name__)


def get_db_connection():
    """Buka koneksi ke PostgreSQL."""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def init_raw_tables():
    """Inisialisasi skema raw dan tabel raw_weather_payloads."""
    ddl_query = """
    CREATE SCHEMA IF NOT EXISTS raw;

    CREATE TABLE IF NOT EXISTS raw.raw_weather_payloads (
        id SERIAL PRIMARY KEY,
        city_name VARCHAR(100) NOT NULL,
        province VARCHAR(100) NOT NULL,
        island_group VARCHAR(100) NOT NULL,
        latitude NUMERIC(8, 4) NOT NULL,
        longitude NUMERIC(8, 4) NOT NULL,
        extracted_at TIMESTAMPTZ NOT NULL,
        payload JSONB NOT NULL,
        loaded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    );
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(ddl_query)
        conn.commit()
    logger.info("Tabel raw.raw_weather_payloads siap.")


def load_to_postgres(weather_records: list[dict]):
    """Insert data mentah ke tabel raw PostgreSQL."""
    insert_query = """
    INSERT INTO raw.raw_weather_payloads (
        city_name,
        province,
        island_group,
        latitude,
        longitude,
        extracted_at,
        payload
    ) VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            for record in weather_records:
                cur.execute(
                    insert_query,
                    (
                        record["city_name"],
                        record["province"],
                        record["island_group"],
                        record["latitude"],
                        record["longitude"],
                        record["extracted_at"],
                        Json(record["payload"]),
                    ),
                )
        conn.commit()
        logger.info("Sukses memuat %d data kota ke raw.raw_weather_payloads.", len(weather_records))
    except Exception as e:
        conn.rollback()
        logger.error("Gagal memuat data ke DB: %s", e)
        raise
    finally:
        conn.close()
