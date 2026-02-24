#!/usr/bin/env python3
"""
Authentication handlers for API clients
"""

import base64
import hashlib
import hmac
import time
from requests.auth import HTTPBasicAuth, AuthBase


class BearerAuth(AuthBase):
    """Bearer token authentication"""
    
    def __init__(self, token):
        self.token = token
    
    def __call__(self, request):
        request.headers['Authorization'] = f'Bearer {self.token}'
        return request


class APIKeyAuth(AuthBase):
    """API Key authentication (header or query param)"""
    
    def __init__(self, api_key, key_name='X-API-Key', location='header'):
        self.api_key = api_key
        self.key_name = key_name
        self.location = location
    
    def __call__(self, request):
        if self.location == 'header':
            request.headers[self.key_name] = self.api_key
        elif self.location == 'query':
            request.prepare_url(request.url, {self.key_name: self.api_key})
        return request


class HMACAuth(AuthBase):
    """HMAC signature authentication"""
    
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
    
    def __call__(self, request):
        timestamp = str(int(time.time()))
        message = f"{timestamp}{request.method}{request.path_url}"
        
        signature = hmac.new(
            self.api_secret.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        
        request.headers['X-API-Key'] = self.api_key
        request.headers['X-Timestamp'] = timestamp
        request.headers['X-Signature'] = signature
        
        return request


# Example usage
if __name__ == '__main__':
    import requests
    
    # Bearer token auth
    response = requests.get(
        'https://api.example.com/data',
        auth=BearerAuth('your-token-here')
    )
    
    # API Key in header
    response = requests.get(
        'https://api.example.com/data',
        auth=APIKeyAuth('your-api-key', 'X-API-Key', 'header')
    )
