# Eneco Data Analytics Assessment – Solutions

**Submission**: Full Stack Data Engineer Assessment (5 assignments)

**Overview**: Solutions to airport market analysis, cloud data ingestion, vendor API integration, eCommerce analytics, and HTTP API troubleshooting.

---

## Assignment 1: Acquire Data & Derive Insights

**Questions**: 
- Top 3 & bottom 10 countries by airport count?
- Longest runway per country?

**Solution** → `src/1_insights.py`

**Results** (see `results/1_insights/`):

**Top 3 Countries**:
United States, Brazil, Canada

**Bottom 10 Countries** (all have exactly 1 airport):
Saint Barthélemy, Curaçao, Christmas Island, Cocos Islands, British Indian Ocean Territory, Jersey, Gibraltar, Gambia, Sint Maarten, Niue

**Longest Runways**: 238 countries analyzed  
**Deliverable**: `results/1_insights/longest_runways.csv`

---

## Assignment 2: Upload to Azure Blob Storage

**Question**: Upload dataset to Azure for Data Warehouse ingestion

**Solution** → `src/2_upload_to_azure.py`

**Status**: Uploads `top_3_countries.csv` and `longest_runways.csv` to Azure Blob

**Target path**: `/ingest-assessment-{date:yyyyMMdd}-{initials}`

---

## Assignment 3: Vendor API – Country Data Acquisition

**Questions**:
- Gather country data for all airports' ISO codes via API
- Upload revenues.txt to POST endpoint  
- Which countries are missing?

**Solution** → `src/3_vendor_api.py`

**Status**:
- Country data fetched successfully
- `revenues.txt` uploaded to vendor API

**Output**: 
- `results/3_vendor_api/missing_countries.txt` — missing countries out of fetched data
- `results/3_vendor_api/revenues.txt` — Upload confirmation

---

## Assignment 4: eCommerce RDBMS – Chinook Analytics

**Questions**:
- Do jazz customers spend more than non-jazz customers?
- Suggest query optimization for track name lookup

**Solution** → `sql/4_chinook_analysis.sql`

**Query Optimization Recommendation**:
```sql
-- Problem: Current query does full table scan (LOWER is not indexed)
SELECT album.title FROM track 
JOIN album ON (track.album_id = album.album_id) 
WHERE LOWER(track.name) = LOWER('Enter Sandman');

-- Solution: Create functional index on LOWER(name)
CREATE INDEX idx_track_name_ci ON track(LOWER(name));
```

**Status**: 
- **Complete**:
- Non‑jazz customers have a slightly higher average spend — 40.06 vs 38.96
- Index creation failed: (psycopg2.errors.InsufficientPrivilege) must be owner of table track

---

## Assignment 5: HTTP API Integration – JWT Troubleshooting

**Question**:
1. What could this snippet represent and how is it typically used?
2. Describe the steps you would take to further analyze Bob's issue

**Solution** → `docs/5_http_analysis.md` (detailed analysis) + `src/5_http_analysis.py` (code)

**Answer 1 - What is the snippet:**
This is a JWT (JSON Web Token) used for API authentication via Azure AD. It's sent in the `Authorization: Bearer <token>` header for API requests.

**Answer 2 - Root Cause:**
Token expired on March 22, 2021 14:43 UTC, but Bob's email is from March 23, 2021 10:21 CET (~19 hours later). Bob is reusing yesterday's demo token.

**Solution for Bob:**
Request a new token from Azure AD before making API calls. Tokens typically expire after 1 hour.

**Full analysis:** See `docs/5_http_analysis.md`

---

## How to Run

### Prerequisites
- Python 3.12+
- Virtual environment

### Run All Pipelines

```powershell
python src/1_insights.py      # Local analysis (always works)
python src/2_upload_to_azure.py  # Requires AZURE_STORAGE_* env vars
python src/3_vendor_api.py    # Requires VENDOR_API_HOST env vars
jupyter notebook sql/4_chinook_analysis.ipynb  # Requires PG_* env vars set
python src/5_http_analysis.py  # JWT analysis
```

---

## Project Structure

```
results/
├── 1_insights/
│   ├── airports_by_country.csv         # All countries, airport counts
│   ├── longest_runways.csv             # Longest runways per country
│   ├── top_3_countries.csv             # US, Brazil, Canada
│   └── bottom_10_countries.csv         # Countries with elast airports
├── 3_vendor_api/
│   ├── countries_data.csv              # API response (or empty if unreachable)
│   └── missing_countries.txt           # Missing countries from the endpoint
│   └── revenues.txt                    # Upload confirmation file
src/
├── 1_insights.py                       # Airport analysis 
├── 2_upload_to_azure.py                # Azure Blob integration
├── 3_vendor_api.py                     # REST client with retry logic
├── 5_http_analysis.py                  # HTTP utilities
data/
├── airports.csv                        
├── countries.csv                       
└── runways.csv                         
sql/
└── 4_chinook_analysis.sql              # Sample Chinook queries
```

---

## Dependencies

```
pandas>=3.0.0           # Data manipulation
azure-storage-blob      # Azure integration (optional)
requests>=2.31.0        # HTTP client
psycopg2-binary         # PostgreSQL (optional)
fastapi                 # API framework (optional)
python-dotenv           # Env config
```

Install: `pip install -r requirements.txt`

---