"""Tests for admin authentication login flow.

Regression suite for the admin login endpoint using ADMIN_USERNAME/ADMIN_PASSWORD
seeded by seed_admin() on startup. Defaults: 'donas' / 'Seinao10@@' (see
/app/backend/admin_routes.py). Override via env vars if the deployed .env
sets different credentials.
"""
import os
import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "http://localhost:8001").rstrip("/")

ADMIN_USER = os.environ.get("ADMIN_USERNAME", "donas")
ADMIN_PASS = os.environ.get("ADMIN_PASSWORD", "Seinao10@@")


@pytest.fixture(scope="module")
def api():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


class TestAdminLogin:
    """POST /api/admin/auth/login"""

    def test_login_success_returns_token_and_user(self, api):
        r = api.post(
            f"{BASE_URL}/api/admin/auth/login",
            json={"username": ADMIN_USER, "password": ADMIN_PASS},
            timeout=15,
        )
        assert r.status_code == 200, f"Expected 200, got {r.status_code}: {r.text}"
        data = r.json()
        # Data structure assertions
        assert "token" in data
        assert isinstance(data["token"], str)
        # JWTs are three base64 segments separated by dots
        assert data["token"].count(".") == 2
        assert len(data["token"]) > 20
        assert "user" in data
        assert data["user"].get("username") == ADMIN_USER

    def test_login_wrong_password_returns_401(self, api):
        r = api.post(
            f"{BASE_URL}/api/admin/auth/login",
            json={"username": ADMIN_USER, "password": "WrongPassword123"},
            timeout=15,
        )
        assert r.status_code == 401
        body = r.json()
        # FastAPI's HTTPException default field is 'detail'
        assert "detail" in body
        assert "invalid" in body["detail"].lower() or "credenciais" in body["detail"].lower()

    def test_login_unknown_username_returns_401(self, api):
        r = api.post(
            f"{BASE_URL}/api/admin/auth/login",
            json={"username": "nonexistent_user_xyz", "password": "irrelevant"},
            timeout=15,
        )
        assert r.status_code == 401


class TestAdminProtectedRoutes:
    """Authenticated calls to protected admin endpoints using the JWT."""

    @pytest.fixture(scope="class")
    def auth_headers(self):
        r = requests.post(
            f"{BASE_URL}/api/admin/auth/login",
            json={"username": ADMIN_USER, "password": ADMIN_PASS},
            timeout=15,
        )
        if r.status_code != 200:
            pytest.skip(f"Login failed: {r.status_code} {r.text}")
        token = r.json()["token"]
        return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    def test_get_admin_me(self, auth_headers):
        r = requests.get(f"{BASE_URL}/api/admin/auth/me", headers=auth_headers, timeout=15)
        assert r.status_code == 200
        data = r.json()
        assert data.get("username") == ADMIN_USER
        assert data.get("role") in ("root", "admin")

    def test_list_admins_with_token(self, auth_headers):
        r = requests.get(f"{BASE_URL}/api/admin/admins", headers=auth_headers, timeout=15)
        assert r.status_code == 200
        data = r.json()
        assert "items" in data
        assert "total" in data
        assert isinstance(data["items"], list)
        # donas must be present in the admins list
        usernames = [a.get("username") for a in data["items"]]
        assert ADMIN_USER in usernames, f"'donas' missing from admins list: {usernames}"

    def test_list_admins_without_token_returns_401(self):
        r = requests.get(f"{BASE_URL}/api/admin/admins", timeout=15)
        assert r.status_code == 401

    def test_list_admins_with_invalid_token_returns_401(self):
        r = requests.get(
            f"{BASE_URL}/api/admin/admins",
            headers={"Authorization": "Bearer invalid.jwt.token"},
            timeout=15,
        )
        assert r.status_code == 401

    def test_kpis_endpoint_authenticated(self, auth_headers):
        r = requests.get(f"{BASE_URL}/api/admin/dashboard/kpis", headers=auth_headers, timeout=15)
        assert r.status_code == 200
        data = r.json()
        # KPIs structure sanity
        for k in ("acessos", "inscricoes", "pix_gerados", "pix_copiados", "pix_baixados"):
            assert k in data
