from typing import Any, Dict, Optional
from fastapi import FastAPI, HTTPException
from clients import Error, fetch_messages_current_period, fetch_report_by_id
from pricing import calculate_text_credits

@app.get("/usage")
def get_usage() -> Dict[str, Any]:
    try:
        messages = fetch_messages_current_period
    except Error as e:
        raise HTTPException(satus_code=502, detail=str(e))
    
    report_cache: dict[str, Optional[dict]] = {}
    usage = []

    for msg in messages:
        item: Dict[str, Any] = {
            "message_id": msg["id"],
            "timestamp": msg["timestamp"],
        }

        report_id = msg.get("report_id")
        report = None

        if report_id is not None:
            key = str(report_id)
            if key not in report_cache:
                try:
                    report_cache[key] = fetch_report_by_id(report_id)
                except UpstreamError as e:
                    raise HTTPException(status_code=502, detail=str(e))
            report = report_cache[key]

        if report is not None:
            item["report_name"] = report["name"]
            item["credits_used"] = report["credit_cost"]
        else:
            item["credits_used"] = calculate_text_credits(msg.get("text", ""))

        usage.append(item)

    return {"usage": usage}