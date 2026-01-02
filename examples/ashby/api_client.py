"""
Ashby ATS API Client - Reverse Engineered from HAR Analysis
===========================================================

This client provides programmatic access to Ashby's public job board APIs,
specifically for retrieving job postings from companies using Ashby as their ATS.

Original Use Case: Fetching all jobs from OpenAI's career page
HAR Analysis Date: 2024
API Base URL: https://jobs.ashbyhq.com/api/non-user-graphql

Authentication: None required (public API)
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import requests
import json
from enum import Enum

try:
    import brotli

    HAS_BROTLI = True
except ImportError:
    HAS_BROTLI = False


class WorkplaceType(str, Enum):
    """Employment workplace type enumeration."""

    HYBRID = "Hybrid"
    REMOTE = "Remote"
    ONSITE = "Onsite"


class EmploymentType(str, Enum):
    """Employment type enumeration."""

    FULL_TIME = "FullTime"
    PART_TIME = "PartTime"
    CONTRACT = "Contract"
    INTERNSHIP = "Internship"


class GeoLocationType(str, Enum):
    """Geographic location type enumeration."""

    COUNTRY = "Country"
    REGION = "Region"
    CITY = "City"


@dataclass
class Team:
    """Represents an organizational team."""

    id: str
    name: str
    external_name: Optional[str]
    parent_team_id: Optional[str]


@dataclass
class JobPosting:
    """Represents a job posting summary."""

    id: str
    title: str
    team_id: str
    location_id: str
    location_name: str
    workplace_type: str
    employment_type: str
    compensation_tier_summary: Optional[str]
    secondary_locations: List[Dict[str, str]]


@dataclass
class JobPostingDetails:
    """Represents detailed job posting information."""

    id: str
    title: str
    department_name: str
    department_external_name: Optional[str]
    location_name: str
    location_address: Optional[str]
    workplace_type: str
    employment_type: str
    description_html: str
    is_listed: bool
    is_confidential: bool
    team_names: List[str]
    secondary_location_names: List[str]
    compensation_tier_summary: Optional[str]
    compensation_tiers: List[Dict[str, Any]]
    application_deadline: Optional[str]
    compensation_tier_guide_url: Optional[str]
    scrapeable_compensation_salary_summary: Optional[str]
    compensation_philosophy_html: Optional[str]
    application_limit_callout_html: Optional[str]
    application_form: Dict[str, Any]
    survey_forms: List[Dict[str, Any]]


@dataclass
class Organization:
    """Represents organization metadata and branding."""

    name: str
    public_website: str
    hosted_jobs_page_slug: str
    allow_job_post_indexing: bool
    timezone: str
    theme: Dict[str, Any]
    active_feature_flags: List[str]


class AshbyAPIClient:
    """
    Client for interacting with Ashby's public job board GraphQL API.

    This client provides methods to:
    - Fetch organization metadata
    - List all jobs and teams for an organization
    - Get detailed job posting information
    - Autocomplete geographic locations for application forms

    Example:
        >>> client = AshbyAPIClient()
        >>> jobs = client.get_job_board("openai")
        >>> print(f"Found {len(jobs['jobPostings'])} jobs at {jobs['organization']['name']}")
    """

    BASE_URL = "https://jobs.ashbyhq.com/api/non-user-graphql"

    # Apollo GraphQL client headers (mimics frontend behavior)
    DEFAULT_HEADERS = {
        "apollographql-client-name": "frontend_non_user",
        "apollographql-client-version": "0.1.0",
        "content-type": "application/json",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "origin": "https://jobs.ashbyhq.com",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
    }

    def __init__(self, timeout: int = 30):
        """
        Initialize the Ashby API client.

        Args:
            timeout: Request timeout in seconds (default: 30)
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(self.DEFAULT_HEADERS)

    def _make_request(
        self,
        operation_name: str,
        query: str,
        variables: Dict[str, Any],
        referer: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Make a GraphQL request to the Ashby API.

        Args:
            operation_name: GraphQL operation name
            query: GraphQL query string
            variables: Query variables
            referer: Optional referer URL for the request

        Returns:
            Parsed JSON response data

        Raises:
            requests.exceptions.RequestException: On network errors
            ValueError: On invalid JSON responses or GraphQL errors
        """
        url = f"{self.BASE_URL}?op={operation_name}"

        headers = {}
        if referer:
            headers["referer"] = referer

        payload = {
            "operationName": operation_name,
            "variables": variables,
            "query": query,
        }

        try:
            response = self.session.post(
                url, json=payload, headers=headers, timeout=self.timeout
            )
            response.raise_for_status()

            # Check if response has content
            if not response.content:
                raise ValueError(
                    f"Empty response from {operation_name}. "
                    f"Status: {response.status_code}, URL: {url}"
                )

            content_encoding = response.headers.get("content-encoding", "").lower()
            content_type = response.headers.get("content-type", "").lower()

            # Try parsing JSON first (requests may have already decompressed it)
            # Only manually decompress if parsing fails and content-encoding indicates compression
            response_data = None

            # Ensure proper encoding for text-based parsing
            if response.encoding is None or response.encoding == "ISO-8859-1":
                response.encoding = "utf-8"

            # First, try parsing JSON directly (works if requests auto-decompressed)
            try:
                response_data = response.json()
            except (json.JSONDecodeError, requests.exceptions.JSONDecodeError):
                # JSON parsing failed - might need manual decompression
                if content_encoding == "br" and HAS_BROTLI:
                    content_bytes = response.content
                    try:
                        # Try brotli decompression
                        decompressed = brotli.decompress(content_bytes)
                        response_data = json.loads(decompressed.decode("utf-8"))
                    except Exception:
                        # Decompression failed - content might already be decompressed
                        # Try parsing the raw content as JSON
                        try:
                            response_data = json.loads(content_bytes.decode("utf-8"))
                        except Exception as e:
                            raise ValueError(
                                f"Failed to parse JSON response from {operation_name}. "
                                f"Status: {response.status_code}, "
                                f"Content-Encoding: {content_encoding}, "
                                f"Error: {str(e)}"
                            ) from e
                elif content_encoding == "br" and not HAS_BROTLI:
                    raise ValueError(
                        f"Response is compressed with brotli but brotli library is not installed. "
                        f"Install it with: pip install brotli"
                    )
                else:
                    # Not brotli or parsing failed for other reason
                    try:
                        response_text = response.text[:500]
                    except Exception:
                        response_text = (
                            response.content[:500]
                            if isinstance(response.content, bytes)
                            else str(response.content)[:500]
                        )
                    raise ValueError(
                        f"Invalid JSON response from {operation_name}. "
                        f"Status: {response.status_code}, "
                        f"Content-Type: {content_type}, "
                        f"Content-Encoding: {content_encoding}, "
                        f"Response preview: {response_text}"
                    )

            # Check content type if we successfully parsed JSON
            if (
                response_data is not None
                and content_type
                and "application/json" not in content_type
            ):
                # Warn but don't fail - we already have valid JSON
                pass

            # At this point, response_data should be set if we got here
            # (otherwise an exception would have been raised)
            data = response_data

            # Check for GraphQL errors
            if "errors" in data:
                error_messages = [e.get("message", str(e)) for e in data["errors"]]
                raise ValueError(f"GraphQL errors: {', '.join(error_messages)}")

            return data.get("data", {})

        except requests.exceptions.Timeout:
            raise requests.exceptions.Timeout(
                f"Request to {operation_name} timed out after {self.timeout}s"
            )
        except ValueError as e:
            # Re-raise ValueError as-is (these are our custom errors)
            raise
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(
                f"Request to {operation_name} failed: {str(e)}"
            )

    def get_organization_info(
        self, organization_slug: str, search_context: str = "JobBoard"
    ) -> Organization:
        """
        Fetch organization metadata, branding, and configuration.

        This endpoint returns:
        - Organization name and public website
        - Theme configuration (colors, logos, branding)
        - Feature flags and settings
        - Timezone information

        Args:
            organization_slug: The organization's job board slug (e.g., "openai")
            search_context: Search context (default: "JobBoard")

        Returns:
            Organization object with metadata

        Example:
            >>> client = AshbyAPIClient()
            >>> org = client.get_organization_info("openai")
            >>> print(f"Company: {org.name}")
            >>> print(f"Website: {org.public_website}")
            >>> print(f"Timezone: {org.timezone}")
        """
        query = """
        query ApiOrganizationFromHostedJobsPageName($organizationHostedJobsPageName: String!, $searchContext: OrganizationSearchContext) {
          organization: organizationFromHostedJobsPageName(
            organizationHostedJobsPageName: $organizationHostedJobsPageName
            searchContext: $searchContext
          ) {
            ...OrganizationParts
            __typename
          }
        }

        fragment OrganizationParts on Organization {
          name
          publicWebsite
          customJobsPageUrl
          hostedJobsPageSlug
          allowJobPostIndexing
          theme {
            colors
            showJobFilters
            showLocationAddress
            showTeams
            showAutofillApplicationsBox
            logoWordmarkImageUrl
            logoSquareImageUrl
            applicationSubmittedSuccessMessage
            jobBoardTopDescriptionHtml
            jobBoardBottomDescriptionHtml
            jobPostingBackUrl
            __typename
          }
          appConfirmationTrackingPixelHtml
          recruitingPrivacyPolicyUrl
          activeFeatureFlags
          timezone
          candidateScheduleCancellationReasonRequirementStatus
          __typename
        }
        """

        variables = {
            "organizationHostedJobsPageName": organization_slug,
            "searchContext": search_context,
        }

        referer = f"https://jobs.ashbyhq.com/{organization_slug}"

        data = self._make_request(
            "ApiOrganizationFromHostedJobsPageName", query, variables, referer
        )

        org_data = data.get("organization", {})
        return Organization(
            name=org_data.get("name"),
            public_website=org_data.get("publicWebsite"),
            hosted_jobs_page_slug=org_data.get("hostedJobsPageSlug"),
            allow_job_post_indexing=org_data.get("allowJobPostIndexing"),
            timezone=org_data.get("timezone"),
            theme=org_data.get("theme", {}),
            active_feature_flags=org_data.get("activeFeatureFlags", []),
        )

    def get_job_board_with_teams(self, organization_slug: str) -> Dict[str, Any]:
        """
        Fetch complete job board including all teams and job postings.

        This is the primary endpoint for retrieving all available jobs at an organization.
        Returns both the organizational team structure and a list of all job postings.

        Args:
            organization_slug: The organization's job board slug (e.g., "openai")

        Returns:
            Dictionary containing:
                - teams: List of Team objects with hierarchy
                - jobPostings: List of JobPosting summaries

        Example:
            >>> client = AshbyAPIClient()
            >>> board = client.get_job_board_with_teams("openai")
            >>> print(f"Teams: {len(board['teams'])}")
            >>> print(f"Open positions: {len(board['jobPostings'])}")
            >>>
            >>> for job in board['jobPostings']:
            >>>     print(f"{job['title']} - {job['locationName']} ({job['workplaceType']})")
            >>>     if job['compensationTierSummary']:
            >>>         print(f"  Compensation: {job['compensationTierSummary']}")
        """
        query = """
        query ApiJobBoardWithTeams($organizationHostedJobsPageName: String!) {
          jobBoard: jobBoardWithTeams(
            organizationHostedJobsPageName: $organizationHostedJobsPageName
          ) {
            teams {
              id
              name
              externalName
              parentTeamId
              __typename
            }
            jobPostings {
              id
              title
              teamId
              locationId
              locationName
              workplaceType
              employmentType
              secondaryLocations {
                ...JobPostingSecondaryLocationParts
                __typename
              }
              compensationTierSummary
              __typename
            }
            __typename
          }
        }

        fragment JobPostingSecondaryLocationParts on JobPostingSecondaryLocation {
          locationId
          locationName
          __typename
        }
        """

        variables = {"organizationHostedJobsPageName": organization_slug}

        referer = f"https://jobs.ashbyhq.com/{organization_slug}"

        data = self._make_request("ApiJobBoardWithTeams", query, variables, referer)

        return data.get("jobBoard", {})

    def get_job_posting_details(
        self, organization_slug: str, job_posting_id: str
    ) -> JobPostingDetails:
        """
        Fetch detailed information for a specific job posting.

        This endpoint returns:
        - Full job description HTML
        - Complete compensation information
        - Application form structure and fields
        - Team and location details
        - EEOC survey forms

        Args:
            organization_slug: The organization's job board slug (e.g., "openai")
            job_posting_id: The unique job posting ID

        Returns:
            JobPostingDetails object with complete job information

        Example:
            >>> client = AshbyAPIClient()
            >>> job = client.get_job_posting_details("openai", "73eb1b69-095d-4f27-84ba-54f5df9bc230")
            >>> print(f"Title: {job.title}")
            >>> print(f"Department: {job.department_name}")
            >>> print(f"Compensation: {job.compensation_tier_summary}")
            >>> print(f"\\nDescription:\\n{job.description_html}")
            >>>
            >>> # Access application form fields
            >>> for section in job.application_form['sections']:
            >>>     for field in section['fieldEntries']:
            >>>         print(f"Field: {field['field']['title']} (Required: {field['isRequired']})")
        """
        query = """
        query ApiJobPosting($organizationHostedJobsPageName: String!, $jobPostingId: String!) {
          jobPosting(
            organizationHostedJobsPageName: $organizationHostedJobsPageName
            jobPostingId: $jobPostingId
          ) {
            id
            title
            departmentName
            departmentExternalName
            locationName
            locationAddress
            workplaceType
            employmentType
            descriptionHtml
            isListed
            isConfidential
            teamNames
            applicationForm {
              ...FormRenderParts
              __typename
            }
            surveyForms {
              ...FormRenderParts
              __typename
            }
            secondaryLocationNames
            compensationTierSummary
            compensationTiers {
              id
              title
              tierSummary
              __typename
            }
            applicationDeadline
            compensationTierGuideUrl
            scrapeableCompensationSalarySummary
            compensationPhilosophyHtml
            applicationLimitCalloutHtml
            shouldAskForTextingConsent
            candidateTextingPrivacyPolicyUrl
            legalEntityNameForTextingConsent
            automatedProcessingLegalNotice {
              automatedProcessingLegalNoticeRuleId
              automatedProcessingLegalNoticeHtml
              __typename
            }
            __typename
          }
        }

        fragment JSONBoxParts on JSONBox {
          value
          __typename
        }

        fragment FileParts on File {
          id
          filename
          __typename
        }

        fragment FormFieldEntryParts on FormFieldEntry {
          id
          field
          fieldValue {
            ... on JSONBox {
              ...JSONBoxParts
              __typename
            }
            ... on File {
              ...FileParts
              __typename
            }
            ... on FileList {
              files {
                ...FileParts
                __typename
              }
              __typename
            }
            __typename
          }
          isRequired
          descriptionHtml
          isHidden
          __typename
        }

        fragment FormRenderParts on FormRender {
          id
          formControls {
            identifier
            title
            __typename
          }
          errorMessages
          sections {
            title
            descriptionHtml
            fieldEntries {
              ...FormFieldEntryParts
              __typename
            }
            isHidden
            __typename
          }
          sourceFormDefinitionId
          __typename
        }
        """

        variables = {
            "organizationHostedJobsPageName": organization_slug,
            "jobPostingId": job_posting_id,
        }

        referer = f"https://jobs.ashbyhq.com/{organization_slug}/{job_posting_id}"

        data = self._make_request("ApiJobPosting", query, variables, referer)

        job_data = data.get("jobPosting", {})
        return JobPostingDetails(
            id=job_data.get("id"),
            title=job_data.get("title"),
            department_name=job_data.get("departmentName"),
            department_external_name=job_data.get("departmentExternalName"),
            location_name=job_data.get("locationName"),
            location_address=job_data.get("locationAddress"),
            workplace_type=job_data.get("workplaceType"),
            employment_type=job_data.get("employmentType"),
            description_html=job_data.get("descriptionHtml"),
            is_listed=job_data.get("isListed"),
            is_confidential=job_data.get("isConfidential"),
            team_names=job_data.get("teamNames", []),
            secondary_location_names=job_data.get("secondaryLocationNames", []),
            compensation_tier_summary=job_data.get("compensationTierSummary"),
            compensation_tiers=job_data.get("compensationTiers", []),
            application_deadline=job_data.get("applicationDeadline"),
            compensation_tier_guide_url=job_data.get("compensationTierGuideUrl"),
            scrapeable_compensation_salary_summary=job_data.get(
                "scrapeableCompensationSalarySummary"
            ),
            compensation_philosophy_html=job_data.get("compensationPhilosophyHtml"),
            application_limit_callout_html=job_data.get("applicationLimitCalloutHtml"),
            application_form=job_data.get("applicationForm", {}),
            survey_forms=job_data.get("surveyForms", []),
        )

    def autocomplete_location(
        self, text: str, location_types: Optional[List[GeoLocationType]] = None
    ) -> List[Dict[str, Any]]:
        """
        Autocomplete geographic locations for application forms.

        This endpoint provides location suggestions as users type into location fields
        during the job application process.

        Args:
            text: Search text to autocomplete (minimum 1 character)
            location_types: List of location types to search for
                           (default: [Country, Region, City])

        Returns:
            List of location suggestions with geographic hierarchy

        Example:
            >>> client = AshbyAPIClient()
            >>> suggestions = client.autocomplete_location("San Fr")
            >>> for suggestion in suggestions:
            >>>     print(f"{suggestion['name']}")
            >>>     for geo in suggestion['geoLocationPath']:
            >>>         print(f"  - {geo['name']} ({geo['type']})")
        """
        if location_types is None:
            location_types = [
                GeoLocationType.COUNTRY,
                GeoLocationType.REGION,
                GeoLocationType.CITY,
            ]

        query = """
        query ApiAutocompleteGeoLocation($text: String!, $locationTypes: [GeoLocationType!]) {
          result: autocompleteGeoLocation(text: $text, locationTypes: $locationTypes) {
            ...AutocompleteLocationResultParts
            __typename
          }
        }

        fragment AutocompleteGeoLocationParts on GeoLocation {
          name
          type
          providerLocationId
          __typename
        }

        fragment AutocompleteLocationParts on AutocompleteLocation {
          name
          geoLocationPath {
            ...AutocompleteGeoLocationParts
            __typename
          }
          __typename
        }

        fragment AutocompleteLocationResultParts on AutocompleteLocationResult {
          suggestions {
            ...AutocompleteLocationParts
            __typename
          }
          __typename
        }
        """

        variables = {"text": text, "locationTypes": [lt.value for lt in location_types]}

        data = self._make_request("ApiAutocompleteGeoLocation", query, variables)

        result = data.get("result", {})
        return result.get("suggestions", [])

    def get_all_jobs(self, organization_slug: str) -> List[Dict[str, Any]]:
        """
        Convenience method to fetch all jobs for an organization.

        This is a high-level helper that combines organization info and job board data.

        Args:
            organization_slug: The organization's job board slug (e.g., "openai")

        Returns:
            List of all job postings with basic information

        Example:
            >>> client = AshbyAPIClient()
            >>> jobs = client.get_all_jobs("openai")
            >>> print(f"Found {len(jobs)} open positions")
            >>>
            >>> # Filter by location
            >>> sf_jobs = [j for j in jobs if "San Francisco" in j['locationName']]
            >>> print(f"{len(sf_jobs)} jobs in San Francisco")
            >>>
            >>> # Filter by workplace type
            >>> remote_jobs = [j for j in jobs if j['workplaceType'] == 'Remote']
            >>> print(f"{len(remote_jobs)} remote positions")
        """
        board = self.get_job_board_with_teams(organization_slug)
        if not board:
            return []
        return board.get("jobPostings", []) or []

    def close(self):
        """Close the HTTP session."""
        self.session.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Example usage and demonstration
if __name__ == "__main__":
    # Example 1: Get all jobs from OpenAI
    print("=" * 80)
    print("Example 1: Fetching all jobs from OpenAI")
    print("=" * 80)

    with AshbyAPIClient() as client:
        # Get organization info
        org = client.get_organization_info("openai")
        print(f"\nCompany: {org.name}")
        print(f"Website: {org.public_website}")
        print(f"Timezone: {org.timezone}")
        print(f"Job Indexing Allowed: {org.allow_job_post_indexing}")

        # Get all jobs
        jobs = client.get_all_jobs("openai")
        print(f"\nFound {len(jobs)} open positions at {org.name}")

        # Display summary statistics
        workplace_types = {}
        locations = {}

        for job in jobs:
            # Count by workplace type
            wt = job.get("workplaceType", "Unknown")
            workplace_types[wt] = workplace_types.get(wt, 0) + 1

            # Count by location
            loc = job.get("locationName", "Unknown")
            locations[loc] = locations.get(loc, 0) + 1

        print("\nBreakdown by Workplace Type:")
        for wt, count in sorted(
            workplace_types.items(), key=lambda x: x[1], reverse=True
        ):
            print(f"  {wt}: {count}")

        print("\nTop Locations:")
        for loc, count in sorted(locations.items(), key=lambda x: x[1], reverse=True)[
            :5
        ]:
            print(f"  {loc}: {count}")

        # Display first 5 jobs
        print("\n" + "=" * 80)
        print("Sample Job Listings (first 5):")
        print("=" * 80)

        for i, job in enumerate(jobs[:5], 1):
            print(f"\n{i}. {job['title']}")
            print(f"   Location: {job['locationName']} ({job['workplaceType']})")
            print(f"   Team ID: {job['teamId']}")
            if job.get("compensationTierSummary"):
                print(f"   Compensation: {job['compensationTierSummary']}")
            if job.get("secondaryLocations"):
                sec_locs = [sl["locationName"] for sl in job["secondaryLocations"]]
                print(f"   Also available in: {', '.join(sec_locs)}")

    print("\n" + "=" * 80)
    print("Example 2: Get detailed job posting")
    print("=" * 80)

    with AshbyAPIClient() as client:
        # Get first job ID from the list
        jobs = client.get_all_jobs("openai")
        if jobs:
            first_job = jobs[0]
            job_id = first_job["id"]

            # Fetch detailed information
            details = client.get_job_posting_details("openai", job_id)

            print(f"\nJob Title: {details.title}")
            print(f"Department: {details.department_name}")
            print(f"Teams: {', '.join(details.team_names)}")
            print(f"Location: {details.location_name}")
            print(f"Workplace Type: {details.workplace_type}")
            print(f"Employment Type: {details.employment_type}")

            if details.compensation_tier_summary:
                print(f"Compensation: {details.compensation_tier_summary}")

            if details.scrapeable_compensation_salary_summary:
                print(f"Salary Range: {details.scrapeable_compensation_salary_summary}")

            # Show application form fields
            print("\nApplication Form Fields:")
            for section in details.application_form.get("sections", []):
                for field_entry in section.get("fieldEntries", []):
                    field = field_entry.get("field", {})
                    field_title = field.get("title", "Unknown")
                    is_required = field_entry.get("isRequired", False)
                    field_type = field.get("type", "Unknown")

                    required_marker = "*" if is_required else " "
                    print(f"  {required_marker} {field_title} ({field_type})")

            # Show description preview (first 500 characters)
            if details.description_html:
                # Simple HTML tag removal for preview
                import re

                text_preview = re.sub("<[^<]+?>", "", details.description_html)
                text_preview = " ".join(text_preview.split())[:500]
                print(f"\nJob Description Preview:")
                print(f"{text_preview}...")

    print("\n" + "=" * 80)
    print("Example 3: Location autocomplete")
    print("=" * 80)

    with AshbyAPIClient() as client:
        suggestions = client.autocomplete_location("San Francisco")

        print(f"\nLocation suggestions for 'San Francisco':")
        for suggestion in suggestions[:5]:
            print(f"\n  {suggestion['name']}")
            for geo in suggestion.get("geoLocationPath", []):
                print(f"    - {geo['name']} ({geo['type']})")

    print("\n" + "=" * 80)
    print("All examples completed successfully!")
    print("=" * 80)
