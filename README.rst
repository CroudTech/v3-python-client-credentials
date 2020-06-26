Client Credentials Grant Helpers
================================

Provides two functions to fetch an auth token from the identity service.
Uses a simple in-memory cache for tokens based on their expiry time.

From synchronous contexts (Django)::

    import client_credentials
    client_credentials.get_token()

From asynchronous contexts (fastapi)::

    import client_credentials
    await client_credentials.get_token_async()


These functions return the token and take two optional arguments:

- client: An ID specifying the environment variable to take OAuth config from.
- headers: A dict of request headers.
  If provided, will return the token without making a request.
