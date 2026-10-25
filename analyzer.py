"""Rule-based CI/CD log analyzer using synthetic/general error patterns."""

RULES = [
    {
        "key": "dependency",
        "patterns": ["modulenotfounderror", "no module named", "package not found",
                     "could not resolve dependency", "npm err!"],
        "title": "Dependency installation or resolution failure",
        "cause": "A required package may be missing, unavailable, or incompatible with the configured version.",
        "steps": [
            "Check the dependency manifest and lockfile for the missing package.",
            "Confirm the runtime/package-manager version matches the project requirements.",
            "Re-run dependency installation from a clean environment."
        ],
    },
    {
        "key": "test",
        "patterns": ["assertionerror", "failed", "tests failed", "pytest"],
        "title": "Automated test failure",
        "cause": "One or more tests may be failing because of a regression, incorrect test data, or an environment difference.",
        "steps": [
            "Open the first failing test and read the assertion or traceback above the summary.",
            "Reproduce the test locally with the same runtime and environment variables.",
            "Fix the underlying behaviour or update the test only if its expectation is genuinely outdated."
        ],
    },
    {
        "key": "permission",
        "patterns": ["permission denied", "eacces", "operation not permitted"],
        "title": "Permission or access failure",
        "cause": "The process may not have permission to read, write, execute, or access a required resource.",
        "steps": [
            "Identify the exact file, directory, command, or resource named in the error.",
            "Check file ownership and the minimum permissions required by the workflow.",
            "Avoid broad privileged permissions; grant only the access needed."
        ],
    },
    {
        "key": "network",
        "patterns": ["connection timed out", "connection refused", "temporary failure in name resolution",
                     "could not resolve host", "network is unreachable"],
        "title": "Network connectivity or service availability issue",
        "cause": "A service may be unreachable, DNS resolution may have failed, or a connection may have timed out.",
        "steps": [
            "Check the target hostname, port, and service health.",
            "Verify DNS, firewall rules, and network access from the runner environment.",
            "Retry only if the failure appears transient; investigate repeated failures."
        ],
    },
    {
        "key": "docker",
        "patterns": ["docker daemon", "cannot connect to the docker daemon",
                     "error response from daemon", "image pull"],
        "title": "Container build or image issue",
        "cause": "The container engine may be unavailable, or an image build/pull may have failed.",
        "steps": [
            "Review the Dockerfile and the exact build/pull error.",
            "Check image name, tag, registry authentication, and runner support.",
            "Rebuild with clear logs and avoid exposing credentials in output."
        ],
    },
    {
        "key": "memory",
        "patterns": ["out of memory", "oomkilled", "killed process", "exit code 137"],
        "title": "Possible memory exhaustion",
        "cause": "The process or container may have exceeded its available memory limit.",
        "steps": [
            "Inspect memory usage and container/job limits near the failure timestamp.",
            "Check for unusually large inputs, parallel jobs, or memory leaks.",
            "Tune resource limits or workload size based on measured usage."
        ],
    },
]

def analyze_log(log_text: str) -> dict:
    """Return a transparent, rule-based diagnosis for a CI/CD log snippet."""
    if not isinstance(log_text, str) or not log_text.strip():
        return {
            "status": "empty",
            "summary": "Paste a CI/CD log snippet to begin.",
            "matches": [],
            "note": "PipelinePilot uses simple text patterns; it does not execute code or modify repositories."
        }

    lower = log_text.lower()
    matches = []
    for rule in RULES:
        found = [pattern for pattern in rule["patterns"] if pattern in lower]
        if found:
            matches.append({
                "key": rule["key"],
                "title": rule["title"],
                "cause": rule["cause"],
                "steps": rule["steps"],
                "signals": found,
            })

    if matches:
        return {
            "status": "matched",
            "summary": f"Found {len(matches)} possible failure pattern(s).",
            "matches": matches,
            "note": "These are troubleshooting leads, not a definitive root-cause analysis. Verify against the full logs and environment."
        }

    return {
        "status": "unknown",
        "summary": "No known failure pattern was detected.",
        "matches": [],
        "note": "Review the lines immediately before the failure, exit code, timestamps, and environment details. Add new rules as you learn from real examples."
    }
