"""첫 방문 동의 (W4, BR2.2, AC9.2.1).

동의 규칙 자체를 검증하는 것은 한국어, 배관 동작은 영어로 이름을 쓴다.
"""

from __future__ import annotations

import time

import pytest

pytestmark = pytest.mark.integration


@pytest.mark.ac("AC9.2.1")
def test_first_consent_is_stored(api_client, seed_user) -> None:
    response = api_client.post("/api/v1/me/consent", json={"agreed": True})

    assert response.status_code == 200
    assert response.json()["consentedAt"] is not None


def test_두_번째_동의는_시각을_갱신하지_않는다(api_client, seed_user) -> None:
    first = api_client.post("/api/v1/me/consent", json={"agreed": True}).json()
    time.sleep(0.01)
    second = api_client.post("/api/v1/me/consent", json={"agreed": True}).json()

    assert second["consentedAt"] == first["consentedAt"]


def test_invalid_body_is_rejected_with_details(api_client, seed_user) -> None:
    response = api_client.post("/api/v1/me/consent", json={"agreed": False})

    assert response.status_code == 422
    error = response.json()["error"]
    assert error["code"] == "VALIDATION_ERROR"
    assert error["details"][0]["field"] == "agreed"


def test_consent_responds_within_200ms(api_client, seed_user) -> None:
    api_client.get("/api/v1/me")

    started = time.monotonic()
    response = api_client.post("/api/v1/me/consent", json={"agreed": True})
    elapsed_ms = (time.monotonic() - started) * 1000

    assert response.status_code == 200
    assert elapsed_ms < 200, f"동의 저장이 {elapsed_ms:.0f}ms 걸렸다"
