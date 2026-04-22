import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Caricamento e filtraggio ──────────────────────────────────────────────
df = pd.read_csv("mainDataset.csv", low_memory=False)

# Solo il giro veloce ufficiale di gara (rank 1 = pilota più veloce della gara)
fl = df[df["fastest_lap_rank"] == 1].dropna(subset=["fastest_lap_speed_kmh", "year"]).copy()
fl["year"] = fl["year"].astype(int)

# ── Aggregati annuali ─────────────────────────────────────────────────────
yearly = (
    fl.groupby("year")["fastest_lap_speed_kmh"]
    .agg(mean="mean", std="std", count="count")
    .reset_index()
    .sort_values("year")
)

# ── Configurazione ere regolamentari ──────────────────────────────────────
ERAS = [
    {"start": 2004, "end": 2005, "label": "V10 —\nultimi anni",    "color": "#E8F4FD"},
    {"start": 2006, "end": 2008, "label": "V8\nintroduzione",      "color": "#FEF9E7"},
    {"start": 2009, "end": 2013, "label": "KERS / DRS",            "color": "#EAFAF1"},
    {"start": 2014, "end": 2021, "label": "Ibrido V6 Turbo",       "color": "#FDECEA"},
    {"start": 2022, "end": 2024, "label": "Effetto suolo",         "color": "#F3E8FD"},
]

# Cambi regolamentari chiave con anno e testo
RULE_CHANGES = [
    (2006,  "2006 → V8\n(2.4 L)"),
    (2009,  "2009 → KERS\n+ aero overhaul"),
    (2014,  "2014 → Ibrido\nV6 Turbo (1.6 L)"),
    (2017,  "2017 → Monoposto\npiù larghe"),
    (2022,  "2022 → Effetto\nsuolo"),
]

# ── Figura ────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(15, 8))
fig.patch.set_facecolor("#FAFAFA")
ax.set_facecolor("#FAFAFA")

# Bande era
y_min, y_max = 150, 265
for era in ERAS:
    ax.axvspan(era["start"] - 0.5, era["end"] + 0.5,
               color=era["color"], alpha=0.9, zorder=0)
    ax.text(
        (era["start"] + era["end"]) / 2, y_max - 2,
        era["label"],
        ha="center", va="top", fontsize=8.5, color="#555555",
        fontstyle="italic", fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.6),
    )

# Scatter: tutti i giri veloci di ogni gara (punti piccoli, semi-trasparenti)
ax.scatter(
    fl["year"] + np.random.uniform(-0.25, 0.25, len(fl)),
    fl["fastest_lap_speed_kmh"],
    color="#607D8B", alpha=0.35, s=18, zorder=2, label="Singola gara"
)

# Banda ±1 deviazione standard
ax.fill_between(
    yearly["year"],
    yearly["mean"] - yearly["std"],
    yearly["mean"] + yearly["std"],
    color="#90CAF9", alpha=0.30, zorder=3, label="±1 dev. std."
)

# Linea media annuale
ax.plot(
    yearly["year"], yearly["mean"],
    color="#1565C0", linewidth=2.8, marker="o", markersize=7,
    markerfacecolor="white", markeredgewidth=2,
    zorder=4, label="Media annuale"
)

# Linea di tendenza lineare globale
z = np.polyfit(yearly["year"], yearly["mean"], 1)
p = np.poly1d(z)
x_line = np.array([yearly["year"].min(), yearly["year"].max()])
slope_sign = "+" if z[0] >= 0 else ""
ax.plot(
    x_line, p(x_line),
    color="#E53935", linewidth=1.6, linestyle="--", alpha=0.75, zorder=3,
    label=f"Tendenza ({slope_sign}{z[0]:.2f} km/h/anno)"
)

# Linee verticali ai cambi regolamentari
for year, label in RULE_CHANGES:
    ax.axvline(year - 0.5, color="#B71C1C", linewidth=1.1,
               linestyle=":", alpha=0.65, zorder=5)
    ax.text(
        year - 0.5, y_min + 4, label,
        ha="center", va="bottom", fontsize=7.5, color="#B71C1C",
        rotation=0,
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#B71C1C",
                  alpha=0.85, linewidth=0.8),
    )

# Annotazione anomalia 2020 (no Monaco causa COVID)
ax.annotate(
    "2020: no Monaco\n(COVID-19)",
    xy=(2020, yearly.loc[yearly["year"] == 2020, "mean"].values[0]),
    xytext=(2018.8, 228),
    fontsize=7.5, color="#37474F",
    arrowprops=dict(arrowstyle="->", color="#37474F", lw=1.1),
    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#90A4AE", alpha=0.9),
)

# Annotazione picco velocità (Monza 2020)
fastest_row = fl.loc[fl["fastest_lap_speed_kmh"].idxmax()]
ax.annotate(
    f"Record: {fastest_row['fastest_lap_speed_kmh']:.1f} km/h\n"
    f"({fastest_row['race_name'].split(' Grand')[0]}, {fastest_row['year']})",
    xy=(fastest_row["year"], fastest_row["fastest_lap_speed_kmh"]),
    xytext=(fastest_row["year"] - 2.5, fastest_row["fastest_lap_speed_kmh"] - 4),
    fontsize=7.5, color="#1B5E20",
    arrowprops=dict(arrowstyle="->", color="#1B5E20", lw=1.1),
    bbox=dict(boxstyle="round,pad=0.3", fc="#F1F8E9", ec="#81C784", alpha=0.9),
)

# ── Assi e formattazione ──────────────────────────────────────────────────
ax.set_xlim(2003.2, 2024.8)
ax.set_ylim(y_min, y_max)
ax.set_xticks(range(2004, 2025))
ax.set_xticklabels(range(2004, 2025), rotation=45, ha="right", fontsize=9)
ax.set_yticks(range(160, 266, 10))
ax.yaxis.set_tick_params(labelsize=9)

ax.set_xlabel("Anno", fontsize=12, labelpad=8)
ax.set_ylabel("Velocità del giro veloce (km/h)", fontsize=12, labelpad=8)

ax.set_title(
    "Evoluzione dei Giri Veloci in Formula 1  ·  2004 – 2024\n"
    "Velocità media annuale dei giri veloci di gara per circuito",
    fontsize=14, fontweight="bold", pad=14, color="#212121"
)

ax.grid(axis="y", linestyle="--", linewidth=0.6, alpha=0.45, color="#90A4AE")
ax.grid(axis="x", linestyle=":", linewidth=0.4, alpha=0.25, color="#90A4AE")
for spine in ax.spines.values():
    spine.set_edgecolor("#B0BEC5")

ax.legend(
    loc="lower left", fontsize=9, framealpha=0.9,
    edgecolor="#B0BEC5", fancybox=True
)

plt.tight_layout()
plt.savefig("FastlapEvolution.png", dpi=150, bbox_inches="tight")
plt.show()
