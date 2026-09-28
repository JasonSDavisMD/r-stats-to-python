"""The environment check passes inside the project .venv."""

from psl import envcheck


def test_all_checks_pass():
    results = envcheck.run_checks()
    failures = [message for ok, message in results if not ok]
    assert failures == []
