# clients.py
import os
from typing import Any, Dict, List, Optional, Union
import requests

DEFAULT_MESSAGES_URL = "https://owpublic.blob.core.windows.net/tech-task/messages/current-period"
DEFAULT_REPORT_URL_TMPL = "https://owpublic.blob.core.windows.net/tech-task/reports/{id}"


class Error(RuntimeError):
    """Raised when an upstream dependency fails in a way we can't safely recover from."""


def timeout_secs() -> float:
    return float(os.getenv("HTTP_TIMEOUT_SECS", "5"))


def messages_url() -> str:
    return os.getenv("MESSAGES_URL", DEFAULT_MESSAGES_URL)


def report_url(report_id: Union[str, int]) -> str:
    tmpl = os.getenv("REPORT_URL_TMPL", DEFAULT_REPORT_URL_TMPL)
    return tmpl.format(id=report_id)


def fetch_messages_current_period() -> List[Dict[str, Any]]:
    """
    Fetches messages and validates upstream contract.
    Raises Error if upstream response is malformed.
    """
    try:
        resp = requests.get(messages_url(), timeout=timeout_secs())
    except requests.RequestException as e:
        raise Error(f"Failed to fetch messages: {e}") from e

    if resp.status_code != 200:
        raise Error(f"Messages endpoint returned {resp.status_code}")

    data = resp.json()

    if not isinstance(data, list):
        raise Error("Messages endpoint returned non-list JSON")

    for msg in data:
        if not isinstance(msg, dict):
            raise Error("Message item must be an object")

        if "id" not in msg or not isinstance(msg["id"], int):
            raise Error("Message missing valid 'id'")

        if "timestamp" not in msg or not isinstance(msg["timestamp"], str):
            raise Error("Message missing valid 'timestamp'")

        if "text" not in msg or not isinstance(msg["text"], str):
            raise Error("Message missing valid 'text'")

        if "report_id" in msg and msg["report_id"] is not None:
            if not isinstance(msg["report_id"], (int, str)):
                raise Error("report_id must be int or str")

    return data


def fetch_report_by_id(report_id: Union[str, int]) -> Optional[Dict[str, Any]]:
    """
    Fetches report metadata.

    Returns:
        {"name": str, "credit_cost": number} when report exists
        None when report does not exist (404) -> caller falls back to pricing

    Raises:
        Error if upstream response is malformed or unexpected.
    """
    try:
        resp = requests.get(report_url(report_id), timeout=timeout_secs())
    except requests.RequestException as e:
        raise Error(f"Failed to fetch report {report_id}: {e}") from e

    if resp.status_code == 404:
        return None

    if resp.status_code != 200:
        raise Error(f"Report {report_id} endpoint returned {resp.status_code}")

    data = resp.json()

    if not isinstance(data, dict):
        raise Error("Report endpoint returned non-object JSON")

    if "name" not in data or not isinstance(data["name"], str):
        raise Error("Report missing valid 'name'")

    if "credit_cost" not in data or not isinstance(data["credit_cost"], (int, float)):
        raise Error("Report missing valid 'credit_cost'")

    return {
        "name": data["name"],
        "credit_cost": data["credit_cost"]
    }