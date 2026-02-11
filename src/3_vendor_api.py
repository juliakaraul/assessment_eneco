import os
import requests
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Configuration
HOST = os.getenv("VENDOR_API_HOST", "http://code001.ecsbdp.com")
CLIENT_ID = os.getenv("VENDOR_API_CLIENT_ID")
DATA_DIR = os.getenv("DATA_DIR")

# Load airports and get unique country codes
airports = pd.read_csv(os.path.join(DATA_DIR, "airports.csv"))
iso_codes = sorted(airports["iso_country"].dropna().unique())

# Fetch country data from API
countries = []
missing = []

for iso_code in iso_codes:
    try:
        response = requests.get(f"{HOST}/countries/{iso_code}",
                                timeout=10)
        if response.status_code == 200:
            countries.append(response.json())
        else:
            missing.append(iso_code)
    except requests.RequestException:
        missing.append(iso_code)

# Save results
output_dir = Path("results/3_vendor_api")
output_dir.mkdir(parents=True, exist_ok=True)

open(output_dir / "missing_countries.txt", "w").write("\n".join(missing))

print(f"Fetched {len(countries)} countries")
print(f"Missing: {len(missing)} countries (see missing_countries.txt)")

# Upload empty revenues file
revenues_file = output_dir / "revenues.txt"
revenues_file.touch()

try:
    with open(revenues_file, "rb") as f:
        response = requests.post(
            f"{HOST}/revenues?client={CLIENT_ID}",
            files={"file": ("revenues.txt", f)},
            timeout=10
        )
    print(f"Uploaded revenues.txt" if response.ok else f"✗ Upload failed ({response.status_code})")
except requests.RequestException as e:
    print(f"Upload error: {e}")