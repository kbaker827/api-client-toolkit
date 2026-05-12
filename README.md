# api-client-toolkit

OpenClaw skill toolkit with reusable API client patterns extracted from 5+ tools via Ralph Loop.

## Contents

- `scripts/api_client_base.py` - Base class for building API clients with session management and error handling
- `scripts/auth_handlers.py` - Authentication helpers (Bearer token, API key, OAuth)
- `scripts/rate_limiter.py` - Rate limiting and retry logic with exponential backoff

## Usage

Import these patterns into your OpenClaw skills or standalone Python projects:

```python
from scripts.api_client_base import APIClientBase
from scripts.auth_handlers import BearerTokenAuth
from scripts.rate_limiter import RateLimiter
```

## Related

- [cli-template-toolkit](https://github.com/kbaker827/cli-template-toolkit)
- [gui-template-toolkit](https://github.com/kbaker827/gui-template-toolkit)
- [ralph-loop](https://github.com/kbaker827/ralph-loop)
