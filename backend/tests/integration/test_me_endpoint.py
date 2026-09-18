"""현재 사용자 조회 (W3, FR11.1, AC9.2.1).

기술적 동작이므로 시험 이름은 영어다.
"""

from __future__ import annotations

import time

import pytest

pytestmark = pytest.mark.integration


@pytest.mark.ac("AC9.2.1")
def test_fixed_user_is_returned_without_any_credential(api_client, seed_user) -> None:
    response = api_client.get("/api/v1/me")

    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == str(seed_user.id)
    assert payload["displayName"] == seed_user.display_name
    assert payload["role"] == "USER"
    assert set(payload) == {"id", "displayName", "role", "consentedAt"}


@pytest.mark.ac("AC9.2.1")
def test_consented_at_is_empty_before_consent(api_client, seed_user) -> None:
    assert api_client.get("/api/v1/me").json()["consentedAt"] is None


def test_me_responds_within_200ms(api_client, seed_user) -> None:
    api_client.get("/api/v1/me")

    started = time.monotonic()
    response = api_client.get("/api/v1/me")
    elapsed_ms = (time.monotonic() - started) * 1000

    assert response.status_code == 200
    assert elapsed_ms < 200, f"사용자 조회가 {elapsed_ms:.0f}ms 걸렸다"
