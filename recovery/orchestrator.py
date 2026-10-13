
import json
from pathlib import Path
from datetime import datetime, timezone

import requests


RCA_REPORT = Path("reports/rca-report.json")
RECOVERY_LOG = Path("reports/recovery-log.json")
HEALTH_URL = "http://127.0.0.1:8000/health"


def load_report():
    if not RCA_REPORT.exists():
        raise FileNotFoundError(
            f"RCA report not found: {RCA_REPORT}"
        )

    with RCA_REPORT.open() as file:
        report = json.load(file)

    if report.get("status") != "analysis_complete":
        raise ValueError("RCA analysis is not complete.")

    return report


def recommend_recovery(report):
    root_cause = report.get("root_cause", "").lower()

    if "startup" in root_cause or "port" in root_cause:
        return {
            "action": "inspect_application_startup",
            "description": (
                "Inspect application logs, startup configuration, "
                "environment variables, and port 8000."
            ),
        }

    return {
        "action": "manual_investigation",
        "description": (
            "Review the RCA report and investigate "
            "the incident manually."
        ),
    }


def save_result(result):
    RECOVERY_LOG.parent.mkdir(parents=True, exist_ok=True)
    RECOVERY_LOG.write_text(json.dumps(result, indent=2))
    print(f"\nRecovery decision saved to: {RECOVERY_LOG}")


def check_application_health():
    try:
        response = requests.get(HEALTH_URL, timeout=5)
        healthy = (
            response.status_code == 200
            and response.json().get("status") == "healthy"
        )

        return {
            "url": HEALTH_URL,
            "healthy": healthy,
            "http_status": response.status_code,
            "details": response.text,
        }

    except (requests.RequestException, ValueError) as error:
        return {
            "url": HEALTH_URL,
            "healthy": False,
            "http_status": None,
            "details": str(error),
        }


def record_health_check(result):
    health = check_application_health()

    result["health_check"] = health
    result["application_healthy"] = health["healthy"]

    if health["healthy"]:
        print("Application health check: HEALTHY")
    else:
        print("Application health check: UNHEALTHY")

    save_result(result)
    return health


def main():
    report = load_report()
    recommendation = recommend_recovery(report)

    print("\n=== Recovery Orchestrator ===")
    print(f"Root cause: {report.get('root_cause', 'Unknown')}")
    print(f"Confidence: {report.get('confidence', 'N/A')}")
    print(f"Recommended action: {recommendation['action']}")
    print(f"Details: {recommendation['description']}")

    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "pending_approval",
        "root_cause": report.get("root_cause"),
        "recommended_action": recommendation["action"],
        "requires_human_approval": True,
        "executed": False,
    }

    if report.get("requires_human_approval") is not True:
        print("\nApproval policy is not explicitly enabled. Stopping.")
        result["status"] = "blocked"
        save_result(result)
        return

    approval = input(
        "\nApprove this recovery step? (yes/no): "
    ).strip().lower()

    if approval != "yes":
        result["status"] = "rejected"
        print("Recovery step rejected. No action was executed.")
        save_result(result)
        return

    # Approval is recorded, but no recovery action is executed yet.
    result["status"] = "approved_not_executed"
    result["approval"] = "human_approved"

    print("\nApproved! No infrastructure changes were made.")
    print("Actual recovery execution will be implemented next.")

    record_health_check(result)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Orchestrator error: {error}")

