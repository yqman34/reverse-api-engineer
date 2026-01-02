#!/usr/bin/env python3
"""
Example Usage of the Ashby API Client
======================================

This script demonstrates how to use the AshbyAPIClient to fetch jobs from OpenAI.
"""

from api_client import AshbyAPIClient
import json


def example_1_get_all_jobs():
    """Example 1: Fetch all jobs from OpenAI."""
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Fetching All Jobs from OpenAI")
    print("=" * 80)

    with AshbyAPIClient() as client:
        # Fetch all jobs
        jobs = client.get_all_jobs("openai")

        print(f"\nFound {len(jobs)} open positions at OpenAI\n")

        # Display first 10 jobs
        for i, job in enumerate(jobs[:10], 1):
            print(f"{i}. {job['title']}")
            print(f"   Location: {job['locationName']} ({job['workplaceType']})")
            if job.get('compensationTierSummary'):
                print(f"   Compensation: {job['compensationTierSummary']}")
            print()


def example_2_filter_jobs():
    """Example 2: Filter jobs by various criteria."""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Filtering Jobs")
    print("=" * 80)

    with AshbyAPIClient() as client:
        jobs = client.get_all_jobs("openai")

        # Filter by workplace type
        remote_jobs = [j for j in jobs if j['workplaceType'] == 'Remote']
        hybrid_jobs = [j for j in jobs if j['workplaceType'] == 'Hybrid']

        print(f"\nWorkplace Type Breakdown:")
        print(f"  Remote: {len(remote_jobs)} jobs")
        print(f"  Hybrid: {len(hybrid_jobs)} jobs")

        # Filter by location
        sf_jobs = [j for j in jobs if 'San Francisco' in j['locationName']]
        nyc_jobs = [j for j in jobs if 'New York' in j['locationName']]

        print(f"\nLocation Breakdown:")
        print(f"  San Francisco: {len(sf_jobs)} jobs")
        print(f"  New York City: {len(nyc_jobs)} jobs")

        # Show some remote jobs
        print(f"\nSample Remote Positions:")
        for job in remote_jobs[:5]:
            print(f"  • {job['title']}")


def example_3_job_details():
    """Example 3: Get detailed information for a specific job."""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Fetching Job Details")
    print("=" * 80)

    with AshbyAPIClient() as client:
        # Get first job
        jobs = client.get_all_jobs("openai")
        if not jobs:
            print("No jobs found!")
            return

        first_job = jobs[0]
        print(f"\nFetching details for: {first_job['title']}\n")

        # Get detailed information
        details = client.get_job_posting_details("openai", first_job['id'])

        print(f"Title: {details.title}")
        print(f"Department: {details.department_name}")
        print(f"Teams: {', '.join(details.team_names)}")
        print(f"Location: {details.location_name}")
        print(f"Workplace Type: {details.workplace_type}")
        print(f"Employment Type: {details.employment_type}")

        if details.compensation_tier_summary:
            print(f"Compensation: {details.compensation_tier_summary}")

        # Show application form fields
        print("\nRequired Application Fields:")
        for section in details.application_form.get("sections", []):
            for field_entry in section.get("fieldEntries", []):
                if field_entry.get("isRequired"):
                    field = field_entry.get("field", {})
                    print(f"  • {field.get('title')} ({field.get('type')})")


def example_4_organization_info():
    """Example 4: Get organization metadata."""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Organization Information")
    print("=" * 80)

    with AshbyAPIClient() as client:
        org = client.get_organization_info("openai")

        print(f"\nCompany Name: {org.name}")
        print(f"Website: {org.public_website}")
        print(f"Job Board Slug: {org.hosted_jobs_page_slug}")
        print(f"Timezone: {org.timezone}")
        print(f"Allow Indexing: {org.allow_job_post_indexing}")

        print(f"\nActive Feature Flags ({len(org.active_feature_flags)}):")
        for flag in org.active_feature_flags[:10]:
            print(f"  • {flag}")


def example_5_export_to_json():
    """Example 5: Export all jobs to a JSON file."""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Export Jobs to JSON")
    print("=" * 80)

    with AshbyAPIClient() as client:
        jobs = client.get_all_jobs("openai")

        # Export to JSON file
        output_file = "openai_jobs.json"
        with open(output_file, 'w') as f:
            json.dump(jobs, f, indent=2)

        print(f"\nExported {len(jobs)} jobs to {output_file}")
        print(f"File size: {len(json.dumps(jobs, indent=2))} bytes")


def example_6_multiple_companies():
    """Example 6: Fetch jobs from multiple companies."""
    print("\n" + "=" * 80)
    print("EXAMPLE 6: Multiple Companies")
    print("=" * 80)

    companies = ["openai", "anthropic", "stripe"]

    with AshbyAPIClient() as client:
        print("\nFetching jobs from multiple companies...\n")

        for company in companies:
            try:
                jobs = client.get_all_jobs(company)
                print(f"{company.upper()}: {len(jobs)} open positions")
            except Exception as e:
                print(f"{company.upper()}: Error - {e}")


def main():
    """Run all examples."""
    print("\n" + "=" * 80)
    print("ASHBY API CLIENT - USAGE EXAMPLES")
    print("=" * 80)

    try:
        # Run examples
        # example_1_get_all_jobs()
        # example_2_filter_jobs()
        # example_3_job_details()
        # example_4_organization_info()
        # example_5_export_to_json()
        # example_6_multiple_companies()

        print("\n" + "=" * 80)
        print("All examples completed successfully!")
        print("=" * 80 + "\n")

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
