import os
import time
from typing import Mapping, Optional

import httpx
from cacheout import Cache


token_cache = Cache(maxsize=1000, ttl=300, timer=time.monotonic)


def _get_request_data(client):
    if client:
        return {
            "grant_type": "client_credentials",
            "client_id": os.environ[f"AUTH_CLIENT_ID_{client}"],
            "client_secret": os.environ[f"AUTH_CLIENT_SECRET_{client}"],
            "scopes": os.environ[f"AUTH_CLIENT_SCOPE_{client}"],
        }
    return {
        "grant_type": "client_credentials",
        "client_id": os.environ["AUTH_CLIENT_ID_DEFAULT"],
        "client_secret": os.environ["AUTH_CLIENT_SECRET_DEFAULT"],
        "scopes": os.environ["AUTH_CLIENT_SCOPE_DEFAULT"],
    }


def _fetch_token(data):
    cache_key = tuple(data.values())
    if cache_key in token_cache:
        return token_cache.get(cache_key)
    response = httpx.post(os.environ["AUTH_TOKEN_URL"], data=data)
    token_json = response.json()
    token_cache.set(cache_key, token_json, ttl=token_json["expires_in"])
    return token_json["access_token"]


def get_token(
    client: Optional[str] = None, headers: Optional[Mapping[str, str]] = None
) -> str:
    if headers and "Authorization" in headers:
        return headers["Authorization"].replace("Bearer ", "", 1)
    return _fetch_token(_get_request_data(client))
