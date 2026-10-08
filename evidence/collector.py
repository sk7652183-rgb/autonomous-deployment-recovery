import json
import os
from datetime import datetime


def collect_evidence(incident):
    evidence = {
        "incident": incident,
        "collected_at": datetime.now().isoformat(),
        "system": {
            "hostname": os.uname().nodename,
            "platform": os.uname().sysname,
        },
        "logs": [
            incident.get("reason", "Unknown error")
        ]
    }

    with open("incident-evidence.json", "w") as file:
        json.dump(evidence, file, indent=2)

    print("\n📦 Evidence collected")
    print(json.dumps(evidence, indent=2))


if __name__ == "__main__":

    if not os.path.exists("incident.json"):
        print("No active incident found.")
    else:
        with open("incident.json", "r") as file:
            incident = json.load(file)

        collect_evidence(incident)
