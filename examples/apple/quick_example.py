#!/usr/bin/env python3
"""
Quick example script to demonstrate Apple Jobs API usage.

This script fetches job listings and extracts:
- URL
- Title
- Location
- Description

As requested by the user.
"""

from api_client import AppleJobsAPI
import json
import sys


def main():
    """Fetch and display Apple jobs with requested fields."""

    print("Initializing Apple Jobs API client...\n")
    client = AppleJobsAPI(locale="en-us")

    # Get first page of jobs
    print("Fetching jobs from Apple...\n")
    jobs = client.search_jobs(page=1)

    if not jobs:
        print("No jobs found!")
        return

    print(f"Found {len(jobs)} jobs on page 1\n")
    print("=" * 100)

    # Extract requested fields: URL, Title, Location, Description
    results = []
    for i, job in enumerate(jobs, 1):
        job_data = {
            "url": job.url,
            "title": job.postingTitle,
            "location": job.locations[0].name if job.locations else "N/A",
            "description": job.jobSummary
        }
        results.append(job_data)

        # Print in readable format
        print(f"\n[Job {i}]")
        print(f"Title: {job_data['title']}")
        print(f"Location: {job_data['location']}")
        print(f"URL: {job_data['url']}")
        print(f"Description: {job_data['description'][:150]}...")
        print("-" * 100)

    # Option to save as JSON
    print("\n" + "=" * 100)
    save_choice = input("\nWould you like to save results to JSON? (y/n): ").strip().lower()

    if save_choice == 'y':
        filename = "apple_jobs.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Results saved to {filename}")

    # Option to fetch more pages
    print("\n" + "=" * 100)
    more_choice = input("\nWould you like to fetch more pages? (y/n): ").strip().lower()

    if more_choice == 'y':
        try:
            pages = int(input("How many pages to fetch? (max 20 recommended): ").strip())
            pages = min(pages, 20)  # Limit to 20 pages

            print(f"\nFetching {pages} pages of jobs...")
            all_jobs = client.search_all_jobs(max_pages=pages)

            # Extract all jobs
            all_results = []
            for job in all_jobs:
                all_results.append({
                    "url": job.url,
                    "title": job.postingTitle,
                    "location": job.locations[0].name if job.locations else "N/A",
                    "description": job.jobSummary
                })

            filename = f"apple_jobs_{pages}_pages.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(all_results, f, indent=2, ensure_ascii=False)

            print(f"\n✓ Fetched {len(all_jobs)} jobs from {pages} pages")
            print(f"✓ Results saved to {filename}")

        except ValueError:
            print("Invalid input. Skipping.")

    print("\nDone!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
