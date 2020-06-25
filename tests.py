import client_credentials


class MockResponse:
    def json(self):
        return {
            "access_token": "1234",
            "expires_in": 100,
            "token_type": "Bearer",
        }


def test_get_token(mocker):
    mock_post = mocker.patch("client_credentials.httpx.post")
    mock_post.return_value = MockResponse()
    token = client_credentials.get_token()
    mock_post.assert_called_once()
    assert token == "1234"

    # Try again - should be cached.
    mock_post = mocker.patch("client_credentials.httpx.post")
    token = client_credentials.get_token()
    mock_post.assert_not_called()


def test_token_with_headers(mocker):
    mock_post = mocker.patch("client_credentials.httpx.post")
    token = client_credentials.get_token(
        headers={"Content-Length": 100, "Authorization": "Bearer 5678"}
    )
    mock_post.assert_not_called()
    assert token == "5678"
