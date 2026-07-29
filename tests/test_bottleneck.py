from factory_twin.bottleneck import explain_line_status


def test_explain_line_status_describes_overloaded_lines():
    row = {"line_status": "overloaded"}

    explanation = explain_line_status(row)

    assert "Backlog is growing" in explanation
    assert "processing capacity" in explanation


def test_explain_line_status_describes_underused_lines():
    row = {"line_status": "underused"}

    explanation = explain_line_status(row)

    assert "underused" in explanation
    assert "demand is too low" in explanation


def test_explain_line_status_describes_stable_lines():
    row = {"line_status": "stable"}

    explanation = explain_line_status(row)

    assert "stable" in explanation
    assert "balanced" in explanation
