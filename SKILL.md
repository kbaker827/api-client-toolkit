---
name: api-client-toolkit
description: API client patterns and utilities for Python. Use when building REST API clients - includes authentication, retries, error handling, rate limiting, and response parsing. Extracted from 5+ API tools via Ralph Loop analysis.
---

# API Client Toolkit

**Reusable API client patterns extracted from Ralph Loop analysis.**

## What It Provides

Ready-to-use API patterns including:
- ✅ REST client base class
- ✅ Authentication handlers (Bearer, API Key, OAuth)
- ✅ Retry logic with backoff
- ✅ Rate limiting
- ✅ Error handling
- ✅ Response caching
- ✅ Async support patterns

## Quick Start

### Basic API Client Template

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class APIClient:
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url
        self.session = requests.Session()
        
        # Add retries
        retry = Retry(total=3, backoff_factor=1)
        self.session.mount('https://', HTTPAdapter(max_retries=retry))
        
        # Add auth
        if api_key:
            self.session.headers['Authorization'] = f'Bearer {api_key}'
    
    def get(self, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, timeout=30, **kwargs)
        response.raise_for_status()
        return response.json()
```

### With Error Handling

```python
from requests.exceptions import RequestException, HTTPError

class RobustAPIClient:
    def request(self, method, endpoint, **kwargs):
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            print(f"HTTP Error: {e.response.status_code}")
            raise
        except RequestException as e:
            print(f"Request failed: {e}")
            raise
```

## Scripts

- `scripts/api_client_base.py` - Base client with retries
- `scripts/auth_handlers.py` - Authentication patterns
- `scripts/rate_limiter.py` - Rate limiting utilities

## Usage Examples

"Create an API client for a REST service with retries and auth"

→ Use this skill to generate the boilerplate instantly.

## Ralph Loop Origin

Extracted from API patterns in:
- tempest-weather-skill
- github-skill-publisher
- And 3 more API tools...
