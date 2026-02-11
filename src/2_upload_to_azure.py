import os
from datetime import datetime
from pathlib import Path
from azure.storage.blob import BlobServiceClient
from urllib.parse import unquote
from dotenv import load_dotenv

load_dotenv()


class AzureUploader:
    def __init__(self, account: str, container: str, sas_token: str):
        sas_url = f"https://{account}.blob.core.windows.net/?{sas_token}"
        self.container_client = BlobServiceClient(account_url=sas_url).get_container_client(container)

    def upload(self, local_file: Path, blob_folder: str):
        if not local_file.exists():
            raise FileNotFoundError(f"{local_file} does not exist!")
        blob_path = f"{blob_folder}/{local_file.name}"
        with open(local_file, "rb") as f:
            self.container_client.upload_blob(name=blob_path, data=f, overwrite=True)
        print(f"Uploaded {local_file} → {blob_path}")


if __name__ == "__main__":
    # Load Azure settings
    account = os.getenv("AZURE_STORAGE_ACCOUNT")
    container = os.getenv("AZURE_STORAGE_CONTAINER")
    sas_token = os.getenv("AZURE_STORAGE_SAS").strip()

    # Instantiate uploader
    uploader = AzureUploader(account, container, sas_token)

    # File to upload
    file_path = Path(os.getenv("RESULTS_DIR", "./results")) / "1_insights" / "top_3_countries.csv"

    # Blob folder with date + initials
    today = datetime.today().strftime("%Y%m%d")
    initials = "JK"
    blob_folder = f"ingest-assessment-{today}-{initials}"

    # Upload
    uploader.upload(file_path, blob_folder)