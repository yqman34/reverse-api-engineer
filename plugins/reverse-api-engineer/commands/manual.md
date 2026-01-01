---
description: Launch browser with HAR recording, capture traffic manually, then generate Python API client
argument-hint: "[task] [url]"
allowed-tools: ["MCP:rae-playwright-mcp", "Read", "Write", "Bash"]
---

# Manual Mode - Browser Capture and API Generation

Launch a browser with HAR recording enabled. The user will navigate manually to trigger the desired API calls. When the browser closes, analyze the captured HAR file and generate a production-ready Python API client.

## Prerequisites

Ensure the `reverse-engineering-api` skill is loaded for guidance on HAR analysis and code generation.

## Command Arguments

- `task` (optional): Description of what to reverse engineer (e.g., "fetch Apple jobs", "scrape product data")
- `url` (optional): Starting URL for the browser

If arguments are not provided, prompt the user interactively.

## Workflow

### Step 1: Gather Task Information

If `task` argument is not provided:
```
Ask: "What would you like to reverse engineer? (e.g., 'fetch job listings from Company X')"
```

If `url` argument is not provided:
```
Ask: "What URL should I open? (optional, press Enter to skip)"
```

### Step 2: Generate Run ID and Setup Paths

Generate a unique run ID using UUID format:
```
run_id = uuid4() (e.g., "abc-123-def-456")
```

Setup paths:
```
har_dir = ~/.reverse-api/runs/har/{run_id}/
har_path = {har_dir}/network.har
```

Ensure directory exists:
```bash
mkdir -p ~/.reverse-api/runs/har/{run_id}/
```

### Step 3: Launch Browser with HAR Recording

Use the Playwright MCP `rae-playwright-mcp` to launch a browser with HAR recording:

```
Call MCP tool: playwright_navigate
Parameters:
  - url: {url} or "about:blank" if no URL provided
  - options:
      - record_har: true
      - har_path: ~/.reverse-api/runs/har/{run_id}/network.har
```

Inform the user:
```
Browser launched with HAR recording enabled.
Navigate to the website and interact with it to trigger API calls.
Close the browser when you're done to proceed with analysis.

HAR will be saved to: ~/.reverse-api/runs/har/{run_id}/network.har
```

### Step 4: Wait for Browser to Close

Monitor the browser session. When it closes, the HAR file will be saved automatically.

Verify HAR file exists:
```bash
ls -lh ~/.reverse-api/runs/har/{run_id}/network.har
```

If file doesn't exist or is empty:
```
Error: "HAR file not found or empty. Please ensure you interacted with the website before closing the browser."
Exit with error
```

### Step 5: Analyze HAR File

Read and parse the HAR file:
```python
import json
with open("~/.reverse-api/runs/har/{run_id}/network.har", "r") as f:
    har_data = json.load(f)
```

Use the `reverse-engineering-api` skill guidance to:

1. **Filter relevant entries**: Exclude static assets, analytics, ads, CDN resources
2. **Identify API endpoints**: Look for `/api/`, `/v1/`, `/graphql`, XHR/Fetch requests
3. **Extract patterns**:
   - URL patterns and query parameters
   - HTTP methods (GET, POST, PUT, DELETE)
   - Request/response headers
   - Authentication mechanisms
   - Request body schemas
   - Response structures

Summarize findings:
```
Found {count} relevant API endpoints:
- {method} {endpoint} ({description})
- {method} {endpoint} ({description})
...

Authentication detected: {auth_type} (Bearer token / API key / None)
Base URL: {base_url}
```

### Step 6: Generate API Client

Generate a descriptive name for the script based on the task:
```
task_name = sanitize(task)  # e.g., "apple_jobs_api"
output_dir = ./scripts/{task_name}/
```

Create output directory:
```bash
mkdir -p ./scripts/{task_name}/
```

Generate `api_client.py` with the following structure:

```python
"""
Auto-generated API client for {domain}
Generated from HAR capture on {date}

Run ID: {run_id}
HAR file: ~/.reverse-api/runs/har/{run_id}/network.har
"""

import requests
from typing import Optional, Dict, Any, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class {ClassName}Client:
    """API client for {domain}."""

    def __init__(
        self,
        base_url: str = "{base_url}",
        session: Optional[requests.Session] = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.session = session or requests.Session()
        self._setup_session()

    def _setup_session(self):
        """Configure session with default headers."""
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (compatible)",
            "Accept": "application/json",
            # Add detected required headers
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs,
    ) -> requests.Response:
        """Make an HTTP request with error handling."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise

    # Generated endpoint methods
    # For each detected endpoint, create a method like:

    def get_example(self, param: str) -> Dict[str, Any]:
        """
        {Method description based on endpoint}.

        Args:
            param: {Parameter description}

        Returns:
            JSON response data

        Raises:
            requests.exceptions.RequestException: If request fails
        """
        response = self._request("GET", f"/api/example/{param}")
        return response.json()


# Example usage
if __name__ == "__main__":
    client = {ClassName}Client()
    # Add example calls based on captured endpoints
```

Generate `README.md`:
```markdown
# {Task Name} API Client

Auto-generated Python API client from browser traffic capture.

## Generated From

- **Run ID**: {run_id}
- **HAR File**: ~/.reverse-api/runs/har/{run_id}/network.har
- **Date**: {date}
- **Base URL**: {base_url}

## Installation

```bash
pip install requests
```

## Usage

```python
from api_client import {ClassName}Client

client = {ClassName}Client()

# Example: {endpoint_1}
result = client.{method_1}({params})
print(result)
```

## Available Methods

{List all generated methods with descriptions}

## Authentication

{Describe detected authentication mechanism and how to configure}

## Notes

- Generated from captured browser traffic
- Endpoints based on observed API calls
- May require authentication tokens/API keys
- Test thoroughly before production use
```

### Step 7: Save Run History

Update `~/.reverse-api/history.json` with run metadata:

```json
{
  "run_id": "{run_id}",
  "mode": "manual",
  "task": "{task}",
  "url": "{url}",
  "timestamp": "{ISO timestamp}",
  "har_path": "~/.reverse-api/runs/har/{run_id}/network.har",
  "output_dir": "./scripts/{task_name}/",
  "status": "completed"
}
```

### Step 8: Summary

Present final summary to user:
```
API client generated successfully!

Run ID: {run_id}
HAR file: ~/.reverse-api/runs/har/{run_id}/network.har

Generated files:
- ./scripts/{task_name}/api_client.py
- ./scripts/{task_name}/README.md

Detected endpoints: {count}
Authentication: {auth_type}

Next steps:
1. Review the generated code
2. Test with: python ./scripts/{task_name}/api_client.py
3. Integrate into your project
```

## Error Handling

- **Browser launch fails**: Check Playwright MCP is running and accessible
- **HAR file empty**: User didn't interact with website, or no network traffic captured
- **No API endpoints found**: All entries were filtered out (adjust filters or capture more traffic)
- **Generation fails**: Use `/reverse-api-engineer:engineer {run_id}` to retry with different approach

## Tips for Users

- **Login flows**: Log in during capture to record authentication
- **Pagination**: Navigate through pages to capture query parameter patterns
- **Different actions**: Create, read, update, delete to capture all CRUD endpoints
- **Multiple captures**: You can run manual mode multiple times for different flows
- **Re-engineer**: Use `/reverse-api-engineer:engineer {run_id}` to regenerate from same capture

## Examples

```
/reverse-api-engineer:manual "fetch Apple jobs" https://jobs.apple.com
/reverse-api-engineer:manual "scrape product data"
/reverse-api-engineer:manual
```
