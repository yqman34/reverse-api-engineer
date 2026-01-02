from api_client import AppleJobsAPI
import json
import sys

client = AppleJobsAPI(locale="en-us")

print("Fetching all jobs...")
all_jobs = client.search_all_jobs()

if not all_jobs:
    print("No jobs found!")
    sys.exit(1)

print(f"Found {len(all_jobs)} total jobs\n")
print("=" * 100)

# Extract requested fields: URL, Title, Location, Description
results = []
for i, job in enumerate(all_jobs, 1):
    job_data = {
        "url": job.url,
        "title": job.postingTitle,
        "location": job.locations[0].name if job.locations else "N/A",
        "description": job.jobSummary,
    }
    results.append(job_data)

    if i % 50 == 0:
        print(f"Processed {i}/{len(all_jobs)} jobs...")

# Save to file
output_file = "all_jobs.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\nSaved {len(results)} jobs to {output_file}")
