import logging
from scripts.extract import extract_all_cities
from scripts.db import init_raw_tables, load_to_postgres

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    logger.info("=== [START] Menjalankan Pipeline EL Data Cuaca ===")
    init_raw_tables()
    records = extract_all_cities()
    logger.info("Berhasil mengekstrak %d kota.", len(records))
    load_to_postgres(records)
    logger.info("=== [FINISH] Pipeline EL Selesai dengan Sukses ===")


if __name__ == "__main__":
    main()
