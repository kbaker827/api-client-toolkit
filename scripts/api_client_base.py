#!/usr/bin/env python3
"""
Base API client with retries and error handling
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from requests.exceptions import RequestException, HTTPError, Timeout
import json


class APIClient:
    """Base API client with retry logic"""
    
    def __init__(self, base_url, api_key=None, timeout=30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        
        # Configure retries
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        
        # Set default headers
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'APIClient/1.0'
        })
        
        # Add auth if provided
        if api_key:
            self.session.headers['Authorization'] = f'Bearer {api_key}'
    
    def request(self, method, endpoint, **kwargs):
        """Make HTTP request"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.request(
                method=method.upper(),
                url=url,
                timeout=self.timeout,
                **kwargs
            )
            response.raise_for_status()
            
            # Try to parse JSON
            if response.content:
                return response.json()
            return None
            
        except HTTPError as e:
            print(f"HTTP Error {e.response.status_code}: {e.response.text}")
            raise
        except Timeout:
            print(f"Request timeout after {self.timeout}s")
            raise
        except RequestException as e:
            print(f"Request failed: {e}")
            raise
    
    def get(self, endpoint, params=None):
        """GET request"""
        return self.request('GET', endpoint, params=params)
    
    def post(self, endpoint, data=None, json_data=None):
        """POST request"""
        return self.request('POST', endpoint, data=data, json=json_data)
    
    def put(self, endpoint, data=None, json_data=None):
        """PUT request"""
        return self.request('PUT', endpoint, data=data, json=json_data)
    
    def delete(self, endpoint):
        """DELETE request"""
        return self.request('DELETE', endpoint)


# Example usage
if __name__ == '__main__':
    # Example: JSONPlaceholder API
    client = APIClient('https://jsonplaceholder.typicode.com')
    
    # GET request
    posts = client.get('/posts')
    print(f"Retrieved {len(posts)} posts")
    
    # POST request
    new_post = client.post('/posts', json_data={
        'title': 'Test Post',
        'body': 'This is a test',
        'userId': 1
    })
    print(f"Created post: {new_post}")
