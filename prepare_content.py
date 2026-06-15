#!/usr/bin/env python3
"""Extract and prepare book chapters as JSON for the app."""
import json

with open('book_content.txt') as f:
    content = f.read()

toc = content[14248:28099]
ch1 = content[28099:41013]
ch2 = content[41013:104212]
ch3 = content[104212:]

chapters = {
    "Inhaltsübersicht": toc,
    "Schnelleinstieg & Überblick": ch1,
    "Grundlagen": ch2,
    "Arbeitszeitrechtliche Grundlagen": ch3,
    "Lenk- und Ruhezeiten (EU-Recht)": "(Volltext in dieser Version nicht verfügbar — bitte spezifische Fragen stellen, werden aus verfügbarem Kontext beantwortet)",
    "Sonderregelungen": "(Volltext in dieser Version nicht verfügbar — bitte spezifische Fragen stellen, werden aus verfügbarem Kontext beantwortet)",
    "Ausnahmen": "(Volltext in dieser Version nicht verfügbar — bitte spezifische Fragen stellen, werden aus verfügbarem Kontext beantwortet)",
    "Nachweisführung": "(Volltext in dieser Version nicht verfügbar — bitte spezifische Fragen stellen, werden aus verfügbarem Kontext beantwortet)",
    "Rechte und Pflichten": "(Volltext in dieser Version nicht verfügbar — bitte spezifische Fragen stellen, werden aus verfügbarem Kontext beantwortet)",
    "Überwachung & Kontrolle": "(Volltext in dieser Version nicht verfügbar — bitte spezifische Fragen stellen, werden aus verfügbarem Kontext beantwortet)",
}

with open('chapters_data.json', 'w') as f:
    json.dump(chapters, f, ensure_ascii=False, indent=2)

print("Done. Sizes:")
for k, v in chapters.items():
    print(f"  {k}: {len(v)} chars")
