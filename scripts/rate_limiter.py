#!/usr/bin/env python3
"""
Rate limiting utilities for API clients
"""

import time
from collections import deque
from functools import wraps


class RateLimiter:
    """Simple rate limiter using token bucket algorithm"""
    
    def __init__(self, max_requests, time_window):
        """
        Args:
            max_requests: Maximum number of requests allowed
            time_window: Time window in seconds
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = deque()
    
    def wait_if_needed(self):
        """Wait if rate limit would be exceeded"""
        now = time.time()
        
        # Remove old requests outside the window
        while self.requests and self.requests[0] < now - self.time_window:
            self.requests.popleft()
        
        # Check if we need to wait
        if len(self.requests) >= self.max_requests:
            sleep_time = self.requests[0] - (now - self.time_window)
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        # Record this request
        self.requests.append(now)


class RateLimitedClient:
    """API client with built-in rate limiting"""
    
    def __init__(self, base_url, rate_limit=100, time_window=60):
        import requests
        self.session = requests.Session()
        self.base_url = base_url
        self.limiter = RateLimiter(rate_limit, time_window)
    
    def request(self, method, endpoint, **kwargs):
        """Make rate-limited request"""
        self.limiter.wait_if_needed()
        url = f"{self.base_url}{endpoint}"
        return self.session.request(method, url, **kwargs)


def rate_limited(max_per_second):
    """Decorator to rate limit function calls"""
    min_interval = 1.0 / max_per_second
    last_call = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_call[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            result = func(*args, **kwargs)
            last_call[0] = time.time()
            return result
        return wrapper
    return decorator


# Example usage
if __name__ == '__main__':
    # Rate limiter example
    limiter = RateLimiter(max_requests=5, time_window=10)
    
    for i in range(10):
        limiter.wait_if_needed()
        print(f"Request {i+1} at {time.time():.2f}")
    
    # Decorator example
    @rate_limited(max_per_second=2)
    def api_call():
        print(f"API call at {time.time():.2f}")
    
    for i in range(5):
        api_call()
