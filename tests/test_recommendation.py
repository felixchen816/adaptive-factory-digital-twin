import pytest

from factory_twin.recommendation import recommend_action


def test_recommend_action_for_overloaded_lines():
    row = {"line_status": "overloaded"}

    recommendation = recommend_action(row)

    assert "Increase capacity" in recommendation
    assert "backlog growth" in recommendation


def test_recommend_action_for_underused_lines():
    row = {"line_status": "underused"}

    recommendation = recommend_action(row)

    assert "Reallocate capacity" in recommendation
    assert "idle" in recommendation


def test_recommend_action_for_stable_lines():
    row = {"line_status": "stable"}

    recommendation = recommend_action(row)

    assert "Keep the current setup" in recommendation
    assert "monitor queue growth" in recommendation


def test_recommend_action_rejects_unknown_status():
    row = {"line_status": "blocked"}

    with pytest.raises(ValueError, match="unknown line status"):
        recommend_action(row)
