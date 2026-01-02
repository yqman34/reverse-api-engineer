# Quick Start Guide

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Basic Usage

```python
from api_client import AshbyAPIClient

# Create client
client = AshbyAPIClient()

# Get all jobs from OpenAI
jobs = client.get_all_jobs("openai")

# Print results
for job in jobs:
    print(f"{job['title']} - {job['locationName']}")
```

## Run Examples

```bash
python3 example_usage.py
```

## Common Tasks

### Get All Jobs
```python
from api_client import AshbyAPIClient

with AshbyAPIClient() as client:
    jobs = client.get_all_jobs("openai")
    print(f"Found {len(jobs)} jobs")
```

### Filter Remote Jobs
```python
remote_jobs = [j for j in jobs if j['workplaceType'] == 'Remote']
```

### Get Job Details
```python
with AshbyAPIClient() as client:
    jobs = client.get_all_jobs("openai")
    job_id = jobs[0]['id']

    details = client.get_job_posting_details("openai", job_id)
    print(details.description_html)
```

### Get Organization Info
```python
with AshbyAPIClient() as client:
    org = client.get_organization_info("openai")
    print(f"{org.name} - {org.public_website}")
```

## Other Companies

Works with any company using Ashby ATS:

```python
companies = ["openai", "anthropic", "stripe", "vercel"]

with AshbyAPIClient() as client:
    for company in companies:
        jobs = client.get_all_jobs(company)
        print(f"{company}: {len(jobs)} jobs")
```

## See Full Documentation

Check `README.md` for complete API documentation and advanced usage.
