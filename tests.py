import client_credentials

TOKEN = {"access_token": "1234", "expires_in": 100, "token_type": "Bearer"}


def test_get_token(httpx_mock):
    httpx_mock.add_response(json=TOKEN)
    headers = client_credentials.get_token()
    assert headers == {"Authorization": "Bearer 1234"}

    # Try again - should be cached.
    headers = client_credentials.get_token()
    assert headers == {"Authorization": "Bearer 1234"}


def test_token_with_headers(httpx_mock):
    headers = {"Content-Length": 100, "Authorization": "Bearer 5678"}
    assert client_credentials.get_token(headers=headers) == headers
