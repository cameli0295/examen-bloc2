from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean, median

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


leads = read_csv(DATA_DIR / "leads_novaretail.csv")
crm = read_csv(DATA_DIR / "crm_novaretail.csv")
campaigns = json.loads((DATA_DIR / "campaign_novaretail.json").read_text(encoding="utf-8"))

# Filtrer octobre 2025
start = datetime(2025, 10, 1)
end = datetime(2025, 10, 31)
leads_scope = []
for row in leads:
    d = datetime.strptime(row["date"], "%Y-%m-%d")
    if start <= d <= end:
        leads_scope.append(row)

crm_by_lead = {row["lead_id"]: row for row in crm}
merged = []
for lead in leads_scope:
    crm_row = crm_by_lead.get(lead["lead_id"])
    if crm_row:
        merged.append({**lead, **crm_row})

# KPI campagnes
kpi_rows = []
for camp in campaigns:
    row = dict(camp)
    row["ctr"] = row["clicks"] / row["impressions"]
    row["conversion_rate"] = row["conversions"] / row["clicks"]
    row["cpl"] = row["cost"] / row["conversions"]

    leads_count = sum(1 for x in merged if x["channel"] == row["channel"])
    clients_count = sum(1 for x in merged if x["channel"] == row["channel"] and x["status"] == "Client")
    row["leads"] = leads_count
    row["clients"] = clients_count
    row["cost_per_lead"] = row["cost"] / leads_count if leads_count else None
    row["cost_per_client"] = row["cost"] / clients_count if clients_count else None
    kpi_rows.append(row)

write_csv(
    OUTPUT_DIR / "kpi_par_canal.csv",
    kpi_rows,
    [
        "campaign_id",
        "channel",
        "cost",
        "impressions",
        "clicks",
        "conversions",
        "ctr",
        "conversion_rate",
        "cpl",
        "leads",
        "clients",
        "cost_per_lead",
        "cost_per_client",
    ],
)

# Univarié quantitatif
quant_vars = ["cost", "impressions", "clicks", "conversions", "ctr", "conversion_rate", "cpl"]
quant_summary = []
for var in quant_vars:
    values = [float(r[var]) for r in kpi_rows]
    quant_summary.append(
        {
            "variable": var,
            "mean": mean(values),
            "median": median(values),
            "min": min(values),
            "max": max(values),
            "range": max(values) - min(values),
        }
    )
write_csv(OUTPUT_DIR / "analyse_univariee_quant.csv", quant_summary, list(quant_summary[0].keys()))

# Univarié qualitatif
channel_counts = Counter(row["channel"] for row in merged)
status_counts = Counter(row["status"] for row in merged)

write_csv(
    OUTPUT_DIR / "frequences_channel.csv",
    [{"channel": k, "count": v, "proportion": v / len(merged)} for k, v in channel_counts.items()],
    ["channel", "count", "proportion"],
)
write_csv(
    OUTPUT_DIR / "frequences_status.csv",
    [{"status": k, "count": v, "proportion": v / len(merged)} for k, v in status_counts.items()],
    ["status", "count", "proportion"],
)

# Bivarié
status_by_channel: dict[tuple[str, str], int] = defaultdict(int)
status_by_size: dict[tuple[str, str], int] = defaultdict(int)
status_by_sector: dict[tuple[str, str], int] = defaultdict(int)

for row in merged:
    status_by_channel[(row["channel"], row["status"])] += 1
    status_by_size[(row["company_size"], row["status"])] += 1
    status_by_sector[(row["sector"], row["status"])] += 1

channels = sorted({r["channel"] for r in merged})
statuses = sorted({r["status"] for r in merged})
sizes = sorted({r["company_size"] for r in merged})
sectors = sorted({r["sector"] for r in merged})

rows_channel = []
for c in channels:
    row = {"channel": c}
    for s in statuses:
        row[s] = status_by_channel[(c, s)]
    rows_channel.append(row)

rows_size = []
for c in sizes:
    row = {"company_size": c}
    for s in statuses:
        row[s] = status_by_size[(c, s)]
    rows_size.append(row)

rows_sector = []
for c in sectors:
    row = {"sector": c}
    for s in statuses:
        row[s] = status_by_sector[(c, s)]
    rows_sector.append(row)

write_csv(OUTPUT_DIR / "croisement_status_channel.csv", rows_channel, ["channel", *statuses])
write_csv(OUTPUT_DIR / "croisement_status_taille.csv", rows_size, ["company_size", *statuses])
write_csv(OUTPUT_DIR / "croisement_status_secteur.csv", rows_sector, ["sector", *statuses])

# Taux client par région
region_totals = Counter(r["region"] for r in merged)
region_clients = Counter(r["region"] for r in merged if r["status"] == "Client")
region_rows = []
for region, total in sorted(region_totals.items(), key=lambda x: x[0]):
    region_rows.append(
        {
            "region": region,
            "leads": total,
            "clients": region_clients[region],
            "client_rate": region_clients[region] / total,
        }
    )
write_csv(OUTPUT_DIR / "taux_client_region.csv", region_rows, ["region", "leads", "clients", "client_rate"])

print("Analyse terminée (sans dépendances externes).")
