import pandas as pd
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]  # ai-service/
INPUT_CSV = BASE_DIR / "data" / "africa-who-contraceptive-prevalence-modern-and-traditional-methods.csv"
OUTPUT_JSON = BASE_DIR / "data" / "who_africa_prevalence.json"

if not INPUT_CSV.exists():
    print(f"❌ CSV not found. Place it at: {INPUT_CSV}")
    exit(1)

print("📥 Loading WHO Africa CSV...")
df = pd.read_csv(INPUT_CSV)
df = df.dropna(subset=["value_numeric", "country_iso3", "dim1", "year"])
df = df[df["year"] >= 2015]

docs = []
for _, row in df.iterrows():
    docs.append({
        "id": f"who_{row['country_iso3']}_{row['year']}_{str(row['dim1']).replace(' ', '_')}",
        "title": f"{row['country_iso3']} - {row['dim1']} ({row['year']})",
        "content": f"In {row['country_iso3']} ({row['year']}), {row['value_display']} of women ages 15-49 use {row['dim1']}. Region: {row['who_region']}.",
        "metadata": {
            "country_iso3": str(row["country_iso3"]),
            "year": int(row["year"]),
            "method": str(row["dim1"]),
            "prevalence_percent": float(row["value_numeric"]),
            "who_region": str(row["who_region"])
        }
    })

OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(docs, f, indent=2, ensure_ascii=False)

print(f"✅ Saved {len(docs)} regional records to {OUTPUT_JSON}")