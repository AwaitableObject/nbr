from nbr.utils.client import prepare_headers


def test__prepare_empty_headers() -> None:
    headers = prepare_headers(token="")
    assert not headers


def test__prepare_headers_with_token() -> None:
    headers = prepare_headers(token="token")
    assert headers == {"Authorization": "token token"}
