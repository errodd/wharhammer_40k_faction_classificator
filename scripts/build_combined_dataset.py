from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT_FILE = DATA_DIR / "combined_dataset.csv"


factions = pd.read_csv(DATA_DIR / "Wahapedia Data Export - Factions.csv")
datasheets = pd.read_csv(DATA_DIR / "Wahapedia Data Export - Datasheets.csv")
abilities = pd.read_csv(DATA_DIR / "Wahapedia Data Export - Abilities.csv")
ds_abilities = pd.read_csv(DATA_DIR / "Wahapedia Data Export - DS_Abilities.csv")

# 1) Renombrar columnas para unificar IDs
factions_clean = factions[["id", "name"]].rename(columns={"id": "faction_id", "name": "faction_name"})
datasheets_clean = datasheets[["id", "name", "faction_id", "source_id", "role", "link"]].rename(
    columns={"id": "datasheet_id", "name": "unit_name"}
)

# 2) Unir Facciones + Datasheets
base = datasheets_clean.merge(factions_clean, on="faction_id", how="left")

# 3) Preparar la tabla de habilidades del datasheet
# Se conserva el nombre de la habilidad si existe en la tabla general, o el nombre del propio DS_Abilities
abilities_clean = abilities[["id", "name", "faction_id", "description"]].rename(
    columns={"id": "ability_id", "name": "ability_name", "description": "ability_description"}
)

ability_rows = ds_abilities[["datasheet_id", "ability_id", "name", "description", "type", "parameter"]].copy()
ability_rows["ability_name_raw"] = ability_rows["name"].fillna("")
ability_rows = ability_rows.merge(
    abilities_clean[["ability_id", "ability_name", "ability_description"]],
    on="ability_id",
    how="left",
)
ability_rows["ability_name_final"] = ability_rows["ability_name"].fillna(ability_rows["ability_name_raw"]).fillna("")
ability_rows["ability_description_final"] = ability_rows["ability_description"].fillna(ability_rows["description"]).fillna("")

# 4) Agregar habilidades por datasheet, como texto concatenado
ability_summary = (
    ability_rows.groupby("datasheet_id")
    .agg(
        ability_names=("ability_name_final", lambda s: "; ".join(sorted({str(x).strip() for x in s if str(x).strip()}))),
        ability_descriptions=("ability_description_final", lambda s: " | ".join(sorted({str(x).strip() for x in s if str(x).strip()}))),
        ability_count=("ability_id", "count"),
    )
    .reset_index()
)

# 5) Dataset final
final_df = base.merge(ability_summary, on="datasheet_id", how="left")

# 6) Orden de columnas útil para clasificación de facciones
final_df = final_df[
    [
        "datasheet_id",
        "faction_id",
        "faction_name",
        "unit_name",
        "source_id",
        "role",
        "ability_count",
        "ability_names",
        "ability_descriptions",
        "link",
    ]
]

final_df.to_csv(OUTPUT_FILE, index=False)
print(f"Dataset combinado guardado en: {OUTPUT_FILE}")
print(final_df.head().to_string(index=False))
