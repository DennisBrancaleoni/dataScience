import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- Caricamento dati ---
df = pd.read_csv("mainDataset.csv", low_memory=False)

# Teniamo solo il giro veloce ufficiale di ogni gara (rank 1)
df = df[df["fastest_lap_rank"] == 1].dropna(subset=["fastest_lap_speed_kmh", "year"])
df["year"] = df["year"].astype(int)

# Media della velocità del giro veloce per anno
yearly_mean = df.groupby("year")["fastest_lap_speed_kmh"].mean()

# --- Linea di tendenza lineare (regressione di primo grado) ---
x = yearly_mean.index.values
y = yearly_mean.values
coeffs = np.polyfit(x, y, 1)        # coeffs[0] = pendenza, coeffs[1] = intercetta
trend = np.poly1d(coeffs)

# --- Ere regolamentari (sfondo del grafico) ---
eras = [
    (2004, 2005, "V10"),
    (2006, 2013, "V8"),
    (2014, 2021, "V6 Turbo Ibrido"),
    (2022, 2024, "Effetto suolo"),
]

# --- Grafico ---
fig, ax = plt.subplots(figsize=(14, 6))

# Sfondo per ogni era (colori alternati grigi chiari)
era_colors = ["#f0f0f0", "#e0e0e0", "#f0f0f0", "#e0e0e0"]
for (start, end, label), color in zip(eras, era_colors):
    ax.axvspan(start - 0.5, end + 0.5, color=color, alpha=0.6)
    ax.text((start + end) / 2, 223, label,
            ha="center", va="bottom", fontsize=9, color="gray", style="italic")

# Scatter: velocità di ogni singola gara
ax.scatter(df["year"], df["fastest_lap_speed_kmh"],
           color="steelblue", alpha=0.3, s=20, label="Singola gara")

# Linea della media annuale
ax.plot(yearly_mean.index, yearly_mean.values,
        color="steelblue", linewidth=2.5, marker="o", markersize=6,
        label="Media annuale")

# Linea di tendenza
ax.plot(x, trend(x),
        color="red", linewidth=1.5, linestyle="--",
        label=f"Tendenza ({coeffs[0]:+.2f} km/h/anno)")

# --- Etichette e titolo ---
ax.set_xlabel("Anno", fontsize=12)
ax.set_ylabel("Velocità media del giro veloce (km/h)", fontsize=12)
ax.set_title("Evoluzione dei giri veloci in F1 (2004–2024)", fontsize=14, fontweight="bold")

ax.set_xlim(2003.5, 2024.5)
ax.set_xticks(range(2004, 2025))
ax.set_xticklabels(range(2004, 2025), rotation=45, ha="right")
ax.set_ylim(150, 265)

ax.grid(axis="y", linestyle="--", alpha=0.4)
ax.legend(fontsize=10)

plt.tight_layout()
plt.savefig("FastlapEvolution.png", dpi=150, bbox_inches="tight")
plt.show()
