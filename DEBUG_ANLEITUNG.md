# Remote-Debugging Anleitung für Paperless-ngx Postprocessor

## Voraussetzungen

- VS Code mit Python Extension
- Docker Container läuft
- Port 5678 ist freigegeben

## Einrichtung

### Option 1: Automatisch (Empfohlen)

1. **Debug-Konfiguration auswählen**: 
   - Öffnen Sie VS Code
   - Gehen Sie zu "Run and Debug" (Strg+Shift+D)
   - Wählen Sie "Remote Debug: Docker Container (Auto)" aus der Dropdown-Liste

2. **Debugger starten**:
   - Klicken Sie auf den grünen Play-Button oder drücken Sie F5
   - VS Code startet automatisch das Debug-Script im Docker-Container
   - Der Debugger verbindet sich automatisch, sobald das Script bereit ist

### Option 2: Manuell

1. **Debug-Konfiguration auswählen**: 
   - Wählen Sie "Remote Debug: Docker Container (Manual)" aus der Dropdown-Liste

2. **Debug-Script manuell starten**:
   ```bash
   docker exec -it paperless-ngx-postprocessor-paperless-ngx-1 python3 /usr/src/paperless-ngx-postprocessor/paperlessngx_postprocessor_debug.py --verbose DEBUG process --tag auto
   ```

3. **Debugger verbinden**:
   - Das Script wartet auf den Debugger (zeigt "⏳ Waiting for debugger to attach...")
   - Klicken Sie in VS Code auf den grünen Play-Button oder drücken Sie F5
   - Der Debugger verbindet sich automatisch (zeigt "🔗 Debugger attached!")

## Verwendung

- **Breakpoints setzen**: Klicken Sie in den Code, um Breakpoints zu setzen
- **Step-by-Step**: Verwenden Sie F10 (Step Over), F11 (Step Into), Shift+F11 (Step Out)
- **Variablen inspizieren**: Schauen Sie sich den Debug-Explorer an
- **Call Stack**: Verfolgen Sie den Aufruf-Stack

## Automatische Tasks

Die Konfiguration verwendet automatische Tasks:

- **preLaunchTask**: Startet das Debug-Script im Docker-Container
- **postDebugTask**: Stoppt das Debug-Script nach dem Debugging

## Fehlerbehebung

- **Port 5678 nicht erreichbar**: Stellen Sie sicher, dass der Container läuft und der Port freigegeben ist
- **Debugger verbindet nicht**: Überprüfen Sie, ob das Script auf den Debugger wartet
- **Path Mapping Probleme**: Überprüfen Sie die `pathMappings` in der launch.json
- **Task-Fehler**: Überprüfen Sie, ob der Docker-Container läuft und der Name korrekt ist

## Beispiel-Breakpoints

Gute Stellen für Breakpoints:
- Zeile 84: Vor der API-Initialisierung
- Zeile 95: Vor der Postprocessor-Initialisierung  
- Zeile 120: Vor der Dokumentenverarbeitung

## Hinweise

- **Automatische Konfiguration**: Startet und stoppt das Script automatisch
- **Manuelle Konfiguration**: Für mehr Kontrolle über den Debug-Prozess
- Das Debug-Script stoppt bei jedem Fehler
- Alle Umgebungsvariablen sind korrekt gesetzt
- Der Container hat Zugriff auf alle notwendigen Python-Module
