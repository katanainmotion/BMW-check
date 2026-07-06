# Ladestation-Watcher

Überwacht die TOTAL-Ladestation (EnBW-Netzwerk, Stations-ID 102073) und
schickt dir eine Push-Benachrichtigung, sobald sich der Status ändert.

## Einrichtung (einmalig, ca. 10 Minuten)

### 1. ntfy-App installieren (Push-Benachrichtigungen)
1. Installiere die App **ntfy** aus dem App Store (iOS) – kostenlos, Anbieter: ntfy.sh
2. Öffne die App, tippe auf **„+"** um ein neues Thema (Topic) zu abonnieren
3. Wähle einen **einzigartigen, geheimen Namen** als Topic, z. B. `ladestation-<zufallszahl>-max`
   (Wichtig: Themen bei ntfy.sh sind öffentlich einsehbar, wenn man den Namen kennt –
   darum einen langen, zufälligen Namen wählen, keinen leicht zu erratenden!)
4. Merke dir diesen Namen, du brauchst ihn gleich

### 2. GitHub-Repository anlegen
1. Gehe zu github.com → **New repository**
2. Name z. B. `ladestation-watcher`, Sichtbarkeit **Private**
3. Lade alle Dateien aus diesem Ordner hoch (`check_charger.py`, `.github/workflows/check-charger.yml`, dieses `README.md`)
   – z. B. per Drag & Drop im Browser (Add file → Upload files)

### 3. Secrets hinterlegen
Im Repository: **Settings → Secrets and variables → Actions → New repository secret**

Lege zwei Secrets an:
| Name | Wert |
|---|---|
| `ENBW_SUBSCRIPTION_KEY` | `d4954e8b2e444fc89a89a463788c0a72` |
| `NTFY_TOPIC` | dein gewählter Topic-Name aus Schritt 1 |

### 4. Fertig!
Der Workflow läuft automatisch alle 5 Minuten. Du kannst ihn auch manuell testen:
**Actions-Tab → „Ladestation prüfen" → Run workflow**

Sobald sich der Status der Station ändert, bekommst du eine Push-Nachricht aufs Handy.

## Hinweise
- GitHub Actions ist für private Repos kostenlos im Rahmen von 2.000 Minuten/Monat –
  ein Lauf alle 5 Minuten verbraucht davon nur einen kleinen Bruchteil.
- Cron-Zeitpläne in GitHub Actions sind "best effort" und können sich bei hoher
  Last um ein paar Minuten verzögern – für diesen Zweck unkritisch.
- Falls du eine andere Station überwachen willst: die `STATION_ID` im Skript anpassen
  (auslesen wie beim ersten Mal über die Netzwerk-Analyse im Browser).
