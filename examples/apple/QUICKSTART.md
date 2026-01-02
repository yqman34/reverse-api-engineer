# Quick Start Guide - Apple Jobs API Client

Get started in 3 simple steps to extract Apple job listings!

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install requests
# or
pip install -r requirements.txt
```

### 2. Run the Extraction Script

**Get all jobs (first 5 pages):**
```bash
python extract_job_fields.py
```

**Search for specific jobs:**
```bash
python extract_job_fields.py --query "software engineer"
python extract_job_fields.py --query "designer"
python extract_job_fields.py --query "manager"
```

### 3. Find Your Results

The script automatically creates:
- `apple_jobs_[N]_jobs.json` - JSON format
- `apple_jobs_[N]_jobs.csv` - CSV format

---

## 📦 What You Get

Each job includes exactly what was requested:

```json
{
  "url": "https://jobs.apple.com/en-us/details/200125391/software-engineer",
  "title": "Software Engineer",
  "location": "United States",
  "description": "Full job description text here..."
}
```

---

## 💻 Code Examples

### Example 1: Basic Usage

```python
from api_client import AppleJobsAPI

# Initialize
client = AppleJobsAPI(locale="en-us")

# Get jobs
jobs = client.search_jobs(page=1)

# Extract fields
for job in jobs:
    print(f"URL: {job.url}")
    print(f"Title: {job.postingTitle}")
    print(f"Location: {job.locations[0].name}")
    print(f"Description: {job.jobSummary}")
```

### Example 2: Search with Query

```python
from api_client import AppleJobsAPI

client = AppleJobsAPI()

# Search for engineering jobs
jobs = client.search_jobs(query="engineer")

print(f"Found {len(jobs)} engineering jobs")
```

### Example 3: Get All Jobs

```python
from api_client import AppleJobsAPI

client = AppleJobsAPI()

# Get all jobs (with pagination)
all_jobs = client.search_all_jobs(max_pages=10)

print(f"Retrieved {len(all_jobs)} total jobs")
```

### Example 4: Export to JSON

```python
from api_client import AppleJobsAPI
import json

client = AppleJobsAPI()
jobs = client.search_all_jobs(max_pages=5)

# Extract fields
data = []
for job in jobs:
    data.append({
        "url": job.url,
        "title": job.postingTitle,
        "location": job.locations[0].name if job.locations else "N/A",
        "description": job.jobSummary
    })

# Save to file
with open('jobs.json', 'w') as f:
    json.dump(data, f, indent=2)
```

### Example 5: Export to CSV

```python
from api_client import AppleJobsAPI
import csv

client = AppleJobsAPI()
jobs = client.search_all_jobs(max_pages=5)

with open('jobs.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['url', 'title', 'location', 'description'])
    writer.writeheader()

    for job in jobs:
        writer.writerow({
            'url': job.url,
            'title': job.postingTitle,
            'location': job.locations[0].name if job.locations else 'N/A',
            'description': job.jobSummary
        })
```

---

## 🎯 Common Tasks

### Get total job count
```python
client = AppleJobsAPI()
total = client.get_total_jobs()
print(f"Total jobs: {total}")
```

### Search by keyword
```python
client = AppleJobsAPI()
jobs = client.search_jobs(query="software engineer")
```

### Get multiple pages
```python
client = AppleJobsAPI()
jobs = client.search_all_jobs(max_pages=10)
```

### Change locale
```python
client = AppleJobsAPI(locale="fr-fr")  # French
jobs = client.search_jobs(page=1)
```

---

## 📁 Available Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `api_client.py` | Main API client library | Import in your code |
| `extract_job_fields.py` | Extract jobs to JSON/CSV | `python extract_job_fields.py` |
| `quick_example.py` | Interactive example | `python quick_example.py` |

---

## ✅ Verified Output

The API client has been tested and successfully extracts:

✓ **URL** - Full job posting URL
✓ **Title** - Job posting title
✓ **Location** - Geographic location
✓ **Description** - Complete job description

Example output:
```
Title: Software Engineer
Location: United States
URL: https://jobs.apple.com/en-us/details/200125391/software-engineer
Description: We are looking for a talented software engineer...
```

---

## 📊 Current Statistics

- **Total Jobs Available:** ~6,179 (as of Dec 22, 2025)
- **Jobs Per Page:** ~20
- **Supported Locales:** en-us, fr-fr, and more
- **API Version:** v1

---

## 🛠️ Troubleshooting

**Issue:** `ModuleNotFoundError: No module named 'requests'`
**Solution:** Run `pip install requests`

**Issue:** No jobs returned
**Solution:** Check your internet connection and try again

**Issue:** CSRF token error
**Solution:** The client automatically handles this, but if it persists, restart your script

---

## 📚 More Information

- See `README.md` for full API documentation
- See `SUMMARY.md` for technical details
- See `api_client.py` for implementation details

---

## 🎉 You're Ready!

Run this command to get started:

```bash
python extract_job_fields.py --query "engineer"
```

This will fetch engineering jobs and save them to JSON and CSV files with the exact fields you requested: **URL, Title, Location, Description**.

Happy job hunting! 🍎
