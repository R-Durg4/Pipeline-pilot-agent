from analyzer import analyze_log

def test_empty_log_prompts_for_input():
    result = analyze_log("  ")
    assert result["status"] == "empty"
    assert result["matches"] == []

def test_detects_test_failure():
    result = analyze_log("AssertionError: test failed")
    assert result["status"] == "matched"
    assert any(item["key"] == "test" for item in result["matches"])

def test_detects_dependency_failure():
    result = analyze_log("ModuleNotFoundError: No module named 'requests'")
    assert any(item["key"] == "dependency" for item in result["matches"])

def test_unknown_log_returns_no_match():
    result = analyze_log("Build completed with an unusual internal message")
    assert result["status"] == "unknown"
    assert result["matches"] == []

def test_multiple_patterns_can_be_reported():
    result = analyze_log("ModuleNotFoundError and AssertionError")
    keys = {item["key"] for item in result["matches"]}
    assert "dependency" in keys
    assert "test" in keys
