from django.test.client import Client


def test_root_not_found(client: Client) -> None:
    response = client.get("/")
    assert response.status_code == 404
