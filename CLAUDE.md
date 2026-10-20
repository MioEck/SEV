# CLAUDE.md – SEV Fahrtbericht App

## App-Überblick
- PWA (Progressive Web App) für DB Schienenersatzverkehr (SEV) Fahrtberichte
- Hosted: mioeck.github.io/sev
- Repository: MioEck/SEV
- Einzel-Datei-App: `index.html` enthält alles (HTML, CSS, JS, eingebettetes PDF)

---

## Dateistruktur

| Datei | Zweck |
|---|---|
| `index.html` | Haupt-App (alles in einer Datei) |
| `sw.js` | Service Worker – Cache-Versionierung |
| `manifest.json` | PWA-Manifest (Name, Icons, Theme) |
| `icon-192.png` | App-Icon 192×192 |
| `icon-512.png` | App-Icon 512×512 (maskable) |
| `CLAUDE.md` | Diese Datei |

---

## Verwendete Bibliotheken
- **pdf-lib** (CDN): Schreibt Daten als Text-Overlay auf das PDF-Template
- Keine weiteren externen Frameworks – reines HTML/CSS/JS

---

## PDF-Koordinatensystem
- y=0 ist **unten** in PDF-Koordinaten
- Interne Umrechnung: `pdfY = height - y - size`
- In der `txt()`-Funktion ist y in Screen-Koordinaten (oben = klein, unten = groß)
- **Größeres y in `txt()` = weiter unten auf der Seite**
- Zwei Formate werden erkannt:
  - **Neues Format** (A4, ~595pt Breite): DB SEV GmbH Fahrtbericht
  - **Altes Format** (≥620pt, 661pt Breite): DB Regio

---

## Aktuelles PDF-Template
- Eingebettet als Base64 in `index.html` als `const PDF_B64 = '...'`
- Datei: `sev_Bla_tter_.pdf` (leeres Blankoformular, **kein vorgedrucktes Datum**)
- Wichtig: Kein iPhone-Markup verwenden zum „Weißmalen" – Annotations-Ebene wird von pdf-lib ignoriert, Original scheint durch

---

## Koordinaten (Neues Format)

### Kopfbereich
```javascript
txt(data.fplo,         109, 128, 11)   // Fplo Nummer
txt(data.datum,        358, 112, 12, true) // Datum
txt(data.umlauf,       130, 160, 11)   // Umlaufnummer
txt(data.bef_personen, 350, 196, 11)   // beförderte Personen
txt(data.beginn,       103, 248, 11)   // Beginn Uhr
txt(data.ende,         103, 282, 11)   // Ende Uhr
txt(getGesamtzeit(),   103, 316, 11)   // Gesamtzeit
txt(data.km_ende,      370, 248, 11)   // Km-Ende
txt(data.km_anfang,    370, 282, 11)   // Km-Anfang
txt(getKmGesamt(),     370, 316, 11)   // Km-Gesamt
txt(data.sitzplaetze,  456, 248, 11)   // Sitz+Stehplätze
txt(data.kennzeichen,  452, 305, 10)   // amtl. Kennzeichen
```

### Fahrtentabelle
```javascript
cols = {abfahrt:24, strecke:88, ankunft:387, km:458, pers:524}
rowTops = [394,410,426,442,459,475,491,507,523,540,556,572,588,604,620,637,653,669,685,701]
// Alle Spalten: y - 3 (leicht nach oben für Zeilenmitte)
```

---

## Funktionen

### Kernfunktionen
- **`save()`** – Speichert alle Felder in localStorage
- **`load()`** – Lädt Daten aus localStorage beim Start
- **`generatePDF()`** – Erstellt PDF mit pdf-lib, schreibt Daten als Overlay
- **`txt(text, x, y, size, center?)`** – Schreibt Text an Position im PDF

### PDF-Upload / Vorlage
- **`loadPDF(input)`** – Lädt benutzerdefiniertes PDF; speichert synchron in localStorage (base64) und async in IndexedDB
- **`setPDFLabel(name, isCustom)`** – Aktualisiert UI-Label; zeigt Reset-Button wenn `isCustom=true`
- **`resetVorlage()`** – Löscht `sev_pdf_b64` und `sev_pdf_name` aus localStorage und IndexedDB, setzt `uploadedPDFBytes = null`, stellt Standard-Vorlage wieder her
- **`savePDFtoDB(bytes, name)`** – Speichert PDF in IndexedDB
- **`loadPDFfromDB()`** – Lädt PDF aus IndexedDB (mit boolean-Flags `bytesReady`/`nameReady` statt `!== undefined`)

### Hilfsfunktionen
- **`reverseRoute(strecke)`** – Kehrt Strecke um für Rückfahrt-Vorschlag (z.B. „Kiel - Neumünster" → „Neumünster - Kiel")
- **`autoSumPersonen()`** – Summiert `personen` aller Fahrten und trägt Summe in `bef_personen` ein
- **`getGesamtzeit()`** – Berechnet Gesamtzeit aus Beginn/Ende
- **`getKmGesamt()`** – Berechnet Km-Gesamt aus Km-Ende minus Km-Anfang
- **`uint8ToBase64(bytes)`** / **`base64ToUint8(b64)`** – iOS-sichere Base64-Konvertierung in 8192-Byte-Chunks

### iOS-Fix
- Problem: iOS PWA lädt beim Schließen des Datei-Pickers neu → in-memory-Daten verloren
- Lösung: PDF wird in `reader.onload` **synchron** in `localStorage` als Base64 gespeichert, bevor async-Operationen starten
- Beim Start: Wiederherstellung aus localStorage hat Vorrang vor IndexedDB

---

## Design-Vorgaben

### Farben (CSS Custom Properties)
```css
--primary:      #00c8e8  /* Cyan – Hauptfarbe */
--primary-dark: #0099bb
--orange:       #ff8c1a
--dark:         #0a1628  /* Sehr dunkles Blau (Hintergrund) */
--navy:         #132843
--bg:           #0d1e35
--card:         #1a3350
--border:       #1e4070
--text:         #e0f0f8
--muted:        #6a9ab8
--green:        #00c87a
```

### Manifest
```json
{
  "background_color": "#0a1628",
  "theme_color": "#0a1628"
}
```

### Icons
- `icon-192.png` und `icon-512.png` – vom Nutzer bereitgestellt
- Design der App soll zum Icon passen (dunkles Blau / Cyan)

---

## Nutzer-Wünsche und Entscheidungen

### Was gewünscht wurde
- PDF-Feldpositionen iterativ kalibriert anhand von Screenshots
- iOS-PWA-Bug gefixt (Datei-Picker lädt App neu)
- Rückfahrt-Vorschlag: Wenn neue Fahrt hinzugefügt, Strecke automatisch umkehren
- Auto-Summe beförderte Personen: Summe aus allen Einzelfahrten
- Dark-Theme in Dunkelblau/Cyan passend zum App-Icon
- Standard-PDF einbetten (kein Upload nötig)
- Reset-Button: „↩ Zurück zur Standard-Vorlage" (erscheint nur bei benutzerdefiniertem PDF)
- Dateiname beim Speichern: `SEV_Fahrtbericht_YYYY-MM-DD.pdf`

### Was ausdrücklich NICHT vorausgefüllt werden soll
- Fplo-Nummer
- Umlaufnummer
- Fahrauftrag

### Was NICHT geändert werden soll
- Das Datum wird weiterhin ins PDF geschrieben (das Template hat kein vorgedrucktes Datum)
- Service Worker Cache-Name muss bei jeder Änderung inkrementiert werden (`sev-vXX`)

---

## Bekannte Probleme / Offene Punkte

### Gelöst
- iPhone-Markup macht PDFs nicht wirklich leer (Annotations-Ebene ≠ Content-Stream) → echtes Blanko-PDF verwenden
- IndexedDB Race Condition bei leerem Ergebnis → boolean-Flags statt `!== undefined`
- Dark Theme ließ Upload-Box unsichtbar werden → Farbe auf `#00c8e8` geändert

### Offen / Zu beachten
- Koordinaten wurden durch viele Iterationen gefunden – nicht ohne Grund ändern
- Bei neuem PDF-Template müssen alle Koordinaten neu kalibriert werden
- `rowTops` Offset-Richtung beachten: **y - N = nach oben**, **y + N = nach unten**

---

## Service Worker / Versionierung
- Cache-Name in `sw.js`: immer bei Änderungen erhöhen → `const CACHE = 'sev-vXX'`
- Versionsnummer in `index.html` synchron halten
- Aktuelle Version: **v4.12**

---

## Git-Workflow
- Feature-Branch: `claude/great-bell-Wq2A0`
- Merge immer via PR in `main`
- GitHub Pages deployed automatisch aus `main`
