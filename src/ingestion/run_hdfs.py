from hdfs import InsecureClient
from pathlib import Path
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("hdfs-upload")

hdfs_local_raw = Path("/app/data/raw")
hdfs_root = "/chess-data/raw"
max_retries = 5

def get_hdfs_client():
    for attempt in range(1, max_retries + 1):
        try:
            hdfs_client = InsecureClient("http://namenode:9870", user="root")
            return hdfs_client
        except Exception as e:
            logger.error(f"Connection failed (attempt {attempt}): {e}")

    logger.error("Failed to connect to HDFS after multiple attempts")
    raise ConnectionError("Unable to connect to HDFS")


# Uploads files
def upload_all_files(client):
    client.delete("/chess-data/raw/OTB_databases", recursive=True)
    files = list(hdfs_local_raw.rglob("*.pgn"))

    if not files:
        logger.warning("No PGN files found")
        return

    for file in files:
        relative_path = file.relative_to(hdfs_local_raw)
        hdfs_path = f"{hdfs_root}/{relative_path.as_posix()}"
        hdfs_dir = str(Path(hdfs_path).parent)

        # ensure directory exists
        try:
            client.makedirs(hdfs_dir, permission=755)
        except Exception as e:
            logger.warning(f"Failed to create directory {hdfs_dir}: {e}")

        # upload file to hdfs
        for attempt in range(1, max_retries + 1):
            try:
                client.upload(
                    hdfs_path,
                    str(file),
                    overwrite=False)
                break
            except Exception as e:
                logger.warning(f"Uploading {file} failed: {e}")

client = get_hdfs_client()
upload_all_files(client)