from fastapi.testclient import TestClient

from main import app
from .stubs import file_text


client = TestClient(app)


def test_ping():
    response = client.get("/api/ping")
    assert response.status_code == 200
    assert response.json() == 'pong'


def test_create_documentation():
    response = client.post("/api/documentation/create", json={'code_text': file_text})
    def assert_tag_closed(tag: str) -> None:
        assert response.json().count(f'<{tag}') == response.json().count(f'</{tag}>')

    assert response.status_code == 200
    assert_tag_closed('summary')
    assert_tag_closed('permission')
    assert_tag_closed('param')
    assert_tag_closed('returns')
