import pytest

from app import create_app


@pytest.fixture
def client(monkeypatch):
    monkeypatch.delenv("APP_VERSION", raising=False)
    app = create_app({"TESTING": True})
    return app.test_client()


def test_home_page_returns_200(client):
    assert client.get("/").status_code == 200


def test_about_page_returns_200(client):
    assert client.get("/about").status_code == 200


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy", "version": "1.0.0"}


def test_readiness_endpoint(client):
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ready"}


def test_application_version_is_displayed(client):
    page = client.get("/").get_data(as_text=True)
    assert "Version 1.0.0" in page


def test_neon_ui_and_navigation_are_rendered(client):
    page = client.get("/").get_data(as_text=True)
    assert "NeonOps Console" in page
    assert "DEPLOYMENT" in page
    assert 'href="/about"' in page
    assert 'href="/health"' in page


def test_security_headers_are_set(client):
    response = client.get("/")
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"
