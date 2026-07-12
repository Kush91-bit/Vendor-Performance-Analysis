import pandas as pd
import os
from sqlalchemy import create_engine, inspect
import logging
import time

logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

engine = create_engine("sqlite:///inventory.db")


def load_raw_data():
    """Load all CSV files and ingest them into SQLite database."""

    path = r"C:\Users\HP\OneDrive\Desktop\Vendor\Data\data"

    if not os.path.exists(path):
        print("Data folder not found!")
        return

    print("Path Exists:", os.path.exists(path))
    print("Files:", os.listdir(path))

    start = time.time()

    for file in os.listdir(path):

        if file.endswith(".csv"):

            file_path = os.path.join(path, file)

            logging.info(f"Started ingesting {file}")
            print(f"Ingesting {file}...")

            for i, chunk in enumerate(pd.read_csv(file_path, chunksize=5000)):

                if_exists = "replace" if i == 0 else "append"

                chunk.to_sql(
                    name=file[:-4],
                    con=engine,
                    if_exists=if_exists,
                    index=False
                )

            logging.info(f"Finished ingesting {file}")

    end = time.time()

    logging.info("---------------- Ingestion Complete ----------------")
    logging.info(f"Total Time Taken: {(end-start)/60:.2f} minutes")

    print(f"\nIngestion completed in {(end-start)/60:.2f} minutes")

    inspector = inspect(engine)
    print("\nTables Created:")
    print(inspector.get_table_names())
if __name__ == "__main__":
    load_raw_data()