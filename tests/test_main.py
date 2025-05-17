import pytest
from httpx import AsyncClient, ASGITransport
from postmanlite.main import app


@pytest.mark.asyncio
async def test_get_request_success():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/send-request", json={
            "url": "https://jsonplaceholder.typicode.com/posts/1",
            "method": "GET"
        })
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status_code"] == 200
    assert "body" in json_data
    assert "headers" in json_data


@pytest.mark.asyncio
async def test_post_request_success():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/send-request", json={
            "url": "https://jsonplaceholder.typicode.com/posts",
            "method": "POST",
            "headers": {
                "Content-Type": "application/json"
            },
            "body": {
                "title": "Test",
                "body": "This is a test",
                "userId": 1
            }
        })
    assert response.status_code == 200
    data = response.json()
    assert data["status_code"] == 201
    assert data["body"]["title"] == "Test"


@pytest.mark.asyncio
async def test_invalid_url():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/send-request", json={
            "url": "http://invalid.local",
            "method": "GET"
        })
    assert response.status_code == 200
    data = response.json()
    assert data["status_code"] == 500
    assert "Request failed" in data["body"]


@pytest.mark.asyncio
async def test_invalid_json_headers():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/send-request", json={
            "url": "https://jsonplaceholder.typicode.com/posts",
            "method": "GET",
            "headers": "INVALID"
        })
    assert response.status_code == 422 