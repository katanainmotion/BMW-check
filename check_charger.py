#!/usr/bin/env python3
"""
Prüft den Status einer EnBW-Ladestation und sendet bei Änderung
eine Push-Benachrichtigung über ntfy.sh.

Läuft typischerweise als GitHub-Actions-Workflow alle 5 Minuten.
Der letzte bekannte Status wird in state.json gespeichert (im Repo).
"""

import json
import os
import sys
import urllib.request
import urllib.error

# ---- Konfiguration ----------------------------------------------------
STATION_ID = "102073"
SUBSCRIPTION_KEY = os.environ["ENBW_SUBSCRIPTION_KEY"]  # kommt aus GitHub Secret
NTFY_TOPIC = os.environ["NTFY_TOPIC"]                    # kommt aus GitHub Secret
STATE_FILE = "state.json"

API_URL = f"https://enbw-emp.azure-api.net/emobility-public-api/api/v1/chargestations/{STATION_ID}"
NTFY_URL = f"https://ntfy.sh/{NTFY_TOPIC}"


def get_station_status():
    """Fragt die EnBW-API ab und gibt (frei, gesamt) zurück."""
    req = urllib.request.Request(
        API_URL,
        headers={
            "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
            "User-Agent": "Mozilla/5.0",
            "Accept": "*/*",
            "Origin": "https://www.enbw.com",
            "Referer": "https://www.enbw.com/",
        },
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    available = data.get("availableChargePoints")
    total = data.get("numberOfChargePoints")
    return available, total


def load_last_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"available": None}


def save_state(available):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({"available": available}, f)


def send_push(title, message):
    req = urllib.request.Request(
        NTFY_URL,
        data=message.encode("utf-8"),
        headers={"Title": title.encode("utf-8"), "Priority": "high"},
        method="POST",
    )
    try:
        urllib.request.urlopen(req, timeout=15)
    except urllib.error.URLError as e:
        print(f"Warnung: Push konnte nicht gesendet werden: {e}", file=sys.stderr)


def main():
    try:
        available, total = get_station_status()
    except Exception as e:
        print(f"Fehler beim Abfragen der API: {e}", file=sys.stderr)
        sys.exit(1)

    last = load_last_state()
    last_available = last.get("available")

    print(f"Aktuell frei: {available}/{total} | Zuletzt bekannt: {last_available}")

    if last_available is not None and available != last_available:
        if available > last_available:
            send_push(
                "Ladestation frei geworden! 🔌",
                f"{available} von {total} Ladepunkten jetzt verfügbar.",
            )
        else:
            send_push(
                "Ladestation jetzt belegt",
                f"Nur noch {available} von {total} Ladepunkten frei.",
            )

    save_state(available)


if __name__ == "__main__":
    main()
