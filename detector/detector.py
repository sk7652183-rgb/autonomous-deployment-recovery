import requests
import json
from datetime import datetime

HEALTH_URL = "http://54.244.44.237:8000/health"


def check_application():
    try:
        response = requests.get(HEALTH_URL, timeout=5)

        if response.status_code == 200:
            print("✅ Application is healthy")
            return True

        create_incident(
            reason=f"Health check returned HTTP {response.status_code}"
        )
        return False

    except requests.RequestException as e:
        create_incident(
            reason=f"Application is unreachable: {str(e)}"
        )
        return False


def create_incident(reason):
    incident = {
        "incident_id": f"INC-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "type": "APPLICATION_FAILURE",
        "severity": "HIGH",
        "status": "OPEN",
        "reason": reason,
        "timestamp": datetime.now().isoformat()
    }

    print("\n🚨 INCIDENT DETECTED")
    print(json.dumps(incident, indent=2))

    with open("incident.json", "w") as file:
        json.dump(incident, file, indent=2)


if __name__ == "__main__":
    check_application()
