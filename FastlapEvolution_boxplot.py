import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- Caricamento dati ---
df = pd.read_csv("mainDataset.csv", low_memory=False)

df = df[df["fastest_lap_rank"] == 1].dropna(subset=["fastest_lap_speed_kmh", "year"])
df["year"] = df["year"].astype(int)

years = sorted(df["year"].unique())
data_by_year = [df[df["year"] == y]["fastest_lap_speed_kmh"].values for y in years]

# --- Ere regolamentari ---
eras = [
    (2004, 2005, "V10"),
    (2006, 2013, "V8"),
    (2014, 2021, "V6"),
    (2022, 2024, "V6 Turbo Ibrido"),
]
era_colors = ["#f0f0f0", "#e0e0e0", "#f0f0f0", "#e0e0e0"]

# --- Grafico ---
fig, ax = plt.subplots(figsize=(16, 7))

# Sfondo per ogni era
for (start, end, label), color in zip(eras, era_colors):
    ax.axvspan(years.index(start) + 0.5, years.index(end) + 1.5,
               color=color, alpha=0.6, zorder=0)
    mid_idx = (years.index(start) + years.index(end)) / 2 + 1
    ax.text(mid_idx, 0.97, label,
            ha="center", va="top", fontsize=9, color="gray", style="italic",
            transform=ax.get_xaxis_transform())

# Boxplot
bp = ax.boxplot(data_by_year,
                positions=range(1, len(years) + 1),
                widths=0.6,
                patch_artist=True,
                medianprops=dict(color="red", linewidth=2),
                boxprops=dict(facecolor="steelblue", alpha=0.6),
                whiskerprops=dict(color="steelblue"),
                capprops=dict(color="steelblue"),
                flierprops=dict(marker="o", color="steelblue", alpha=0.4,
                                markersize=4, linestyle="none"))

# Linea della mediana annuale
medians = [np.median(d) for d in data_by_year]
ax.plot(range(1, len(years) + 1), medians,
        color="red", linewidth=1.5, linestyle="--",
        marker="", alpha=0.7, label="Mediana annuale")

# --- Etichette e titolo ---
ax.set_xlabel("Anno", fontsize=12)
ax.set_ylabel("Velocità del giro veloce (km/h)", fontsize=12)
ax.set_title("Evoluzione dei giri veloci in F1 (2004–2024)", fontsize=14, fontweight="bold")

ax.set_xticks(range(1, len(years) + 1))
ax.set_xticklabels(years, rotation=45, ha="right")
ax.set_ylim(150, 265)

ax.grid(axis="y", linestyle="--", alpha=0.4)

from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor="steelblue", alpha=0.6, label="Distribuzione gare"),
    plt.Line2D([0], [0], color="red", linewidth=2, label="Mediana"),
    plt.Line2D([0], [0], color="red", linewidth=1.5, linestyle="--", alpha=0.7, label="Trend mediana"),
]
ax.legend(handles=legend_elements, fontsize=10)

plt.tight_layout()
plt.savefig("FastlapEvolution_boxplot.png", dpi=150, bbox_inches="tight")
plt.show()
