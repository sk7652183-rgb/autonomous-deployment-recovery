
import json
from datetime import datetime, timezone
from pathlib import Path

import requests

BASE_URL = "http://127.0.0.1:8000"

def check_endpoint(path):
    url = f"{BASE_URL}{path}"

    try:
        response = requests.get(url, timeout=5)
        return {
            "url": url,
            "http_status": response.status_code,
            "healthy": response.status_code == 200,
            "details": response.text,
        }
    except requests.RequestException as error:
        return {
            "url": url,
            "http_status": None,
            "healthy": False,
            "details": str(error),
        }

def main():
    results = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "health_endpoint": check_endpoint("/health"),
        "failure_endpoint": check_endpoint("/failure"),
    }

    output = Path("reports/diagnostics.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(results, indent=2))

    print(json.dumps(results, indent=2))
    print(f"\nDiagnostic report saved to {output}")

if __name__ == "__main__":
    main()
