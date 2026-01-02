---
description: Autonomous browser navigation with HAR capture and API client generation
argument-hint: "[task] [url]"
allowed-tools: ["MCP:rae-playwright-mcp", "Read", "Write", "Bash"]
---

# Agent Mode - Autonomous Browser Navigation

Fully autonomous browser navigation using Playwright MCP. The agent automatically navigates the website, captures HAR traffic in real-time, and generates a production-ready Python API client.

## Prerequisites

Ensure the `reverse-engineering-api` skill is loaded for guidance on HAR analysis and code generation.

## Command Arguments

- `task` (required): Description of what to automate (e.g., "find all job listings", "search for products")
- `url` (optional): Starting URL for the browser

If arguments are not provided, prompt the user interactively.

## Workflow

### Step 1: Gather Task Information

If `task` argument is not provided:
```
Ask: "What would you like the agent to do? (e.g., 'navigate to jobs page and list all postings')"
```

If `url` argument is not provided:
```
Ask: "What URL should I start from? (optional, press Enter to skip)"
```

### Step 2: Generate Run ID and Setup Paths

Generate a unique run ID using UUID format:
```
run_id = uuid4() (e.g., "abc-123-def-456")
```

Setup paths:
```
har_dir = ~/.reverse-api/runs/har/{run_id}
har_path = {har_dir}/recording.har
```

Ensure directory exists:
```bash
mkdir -p ~/.reverse-api/runs/har/{run_id}
```

### Step 3: Launch Browser with HAR Recording

Use the Playwright MCP `rae-playwright-mcp` to launch a browser with HAR recording enabled:

```
Call MCP tool: playwright_navigate
Parameters:
  - url: {url} or "about:blank" if no URL provided
  - options:
      - record_har: true
      - har_path: ~/.reverse-api/runs/har/{run_id}/recording.har
```

Inform the user:
```
Agent mode started with HAR recording enabled.
Task: {task}
Starting URL: {url}

I'll navigate autonomously and capture all API traffic.
HAR will be saved to: ~/.reverse-api/runs/har/{run_id}/recording.har
```

### Step 4: Autonomous Navigation

Use Playwright MCP tools to autonomously navigate and complete the task:

**Available Playwright MCP actions:**
- `playwright_navigate(url)` - Navigate to URL
- `playwright_click(selector)` - Click element
- `playwright_fill(selector, text)` - Fill form field
- `playwright_get_text(selector)` - Extract text
- `playwright_wait_for_selector(selector)` - Wait for element
- `playwright_screenshot()` - Take screenshot
- `playwright_evaluate(script)` - Execute JavaScript
- `playwright_get_har_entries()` - Get captured HAR entries in real-time

**Navigation strategy:**

1. **Analyze the page**: Use `playwright_get_text()` to understand page structure
2. **Plan actions**: Based on task, determine what elements to interact with
3. **Execute actions**: Use `playwright_click()`, `playwright_fill()` to navigate
4. **Monitor traffic**: Periodically check `playwright_get_har_entries()` to see captured API calls
5. **Iterate**: Continue until task is complete or sufficient API traffic captured

**Real-time monitoring:**
```
Progress update:
- Navigated to: {current_url}
- Actions taken: {count}
- API calls captured: {har_entry_count}
- Current step: {description}
```

**Example navigation for "find all job listings":**
```
1. Navigate to homepage
2. Look for "Careers" or "Jobs" link
3. Click to navigate to jobs page
4. Wait for job listings to load
5. Capture API calls for job data
6. Check for pagination
7. If pagination exists, load next pages to capture all API patterns
8. Close browser when done
```

### Step 5: Verify HAR Capture

When navigation is complete, verify HAR file exists and contains data:

```bash
if [ -f ~/.reverse-api/runs/har/{run_id}/recording.har ]; then
    size=$(ls -lh ~/.reverse-api/runs/har/{run_id}/recording.har | awk '{print $5}')
    echo "HAR file captured: $size"
else
    echo "Error: HAR file not found"
    exit 1
fi
```

Read HAR file to count entries:
```python
import json
with open("~/.reverse-api/runs/har/{run_id}/recording.har", "r") as f:
    har_data = json.load(f)
    entry_count = len(har_data["log"]["entries"])
```

Display:
```
Browser session completed.
Captured {entry_count} network requests in HAR file.
Analyzing for API endpoints...
```

### Step 6: Analyze HAR File

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
Analysis complete!

Found {count} relevant API endpoints:
- {method} {endpoint} ({description})
- {method} {endpoint} ({description})
...

Authentication detected: {auth_type} (Bearer token / API key / None)
Base URL: {base_url}
```

### Step 7: Generate API Client

Generate a descriptive name for the script based on the task:
```
task_name = sanitize(task)  # e.g., "job_listings_api"
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
Generated from autonomous agent capture on {date}

Task: {task}
Run ID: {run_id}
HAR file: ~/.reverse-api/runs/har/{run_id}/recording.har
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

Auto-generated Python API client from autonomous browser agent.

## Generated From

- **Run ID**: {run_id}
- **HAR File**: ~/.reverse-api/runs/har/{run_id}/recording.har
- **Date**: {date}
- **Task**: {task}
- **Base URL**: {base_url}
- **Mode**: Agent (autonomous navigation)

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

## Agent Navigation Path

The agent autonomously performed these actions:
{List navigation steps taken by agent}

## Notes

- Generated from autonomous agent capture
- Agent task: {task}
- Endpoints based on observed API calls during navigation
- May require authentication tokens/API keys
- Test thoroughly before production use
```

### Step 8: Save Run History

Update `~/.reverse-api/history.json` with run metadata:

```json
{
  "run_id": "{run_id}",
  "mode": "agent",
  "task": "{task}",
  "url": "{url}",
  "timestamp": "{ISO timestamp}",
  "har_path": "~/.reverse-api/runs/har/{run_id}/recording.har",
  "output_dir": "./scripts/{task_name}/",
  "navigation_steps": {count},
  "status": "completed"
}
```

### Step 9: Summary

Present final summary to user:
```
Agent completed task successfully!

Task: {task}
Run ID: {run_id}
HAR file: ~/.reverse-api/runs/har/{run_id}/recording.har

Agent navigation:
- Pages visited: {page_count}
- Actions taken: {action_count}
- API calls captured: {entry_count}

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

- **Navigation fails**: Agent couldn't complete task (suggest manual mode or retry with clearer instructions)
- **HAR file empty**: No network traffic captured (check if site has API endpoints)
- **No API endpoints found**: All entries were filtered out (adjust filters or try different navigation)
- **Agent stuck**: Navigation loop detected (suggest manual mode for complex interactions)

## Tips for Users

- **Clear tasks**: Provide specific, actionable task descriptions
- **Starting URL**: Provide URL when possible to speed up navigation
- **Complex sites**: Use manual mode for sites with heavy JavaScript or complex auth flows
- **Simple tasks**: Agent works best for straightforward navigation patterns
- **Re-engineer**: Use `/reverse-api-engineer:engineer {run_id}` to regenerate if needed

## Real-time Monitoring Benefits

Agent mode with Playwright MCP offers unique advantages:

1. **Live HAR access**: Can check captured API calls during navigation via `playwright_get_har_entries()`
2. **Adaptive navigation**: Can adjust strategy based on observed API patterns
3. **Early termination**: Can stop once sufficient endpoints are captured
4. **Smart pagination**: Can detect when all data patterns are captured

## Examples

```
# Full specification
/reverse-api-engineer:agent "find all job listings" https://jobs.apple.com

# Task only (agent will search for starting page)
/reverse-api-engineer:agent "scrape product catalog"

# Interactive mode
/reverse-api-engineer:agent
> "navigate to pricing page and capture API calls"
> "https://example.com"
```

## Agent vs Manual Mode

**Use Agent Mode when:**
- Task is straightforward and automatable
- Site structure is simple
- You want hands-off operation
- Real-time HAR monitoring is beneficial

**Use Manual Mode when:**
- Site requires complex interactions
- Custom authentication flows
- Need precise control over captured endpoints
- Site has bot detection
- Task involves manual judgment

## Advanced: Real-time HAR Monitoring

During navigation, you can periodically check captured HAR entries:

```
# Check every few actions
entries = playwright_get_har_entries()

# Analyze on-the-fly
api_calls = filter_api_endpoints(entries)

# Decide if done
if len(api_calls) >= 5 and pagination_pattern_detected:
    stop_navigation()
    proceed_to_analysis()
```

This allows intelligent navigation that adapts based on captured API patterns.
