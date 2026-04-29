import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("mainDataset.csv", low_memory=False)

PRIMARY   = "#2C5F8A"
SECONDARY = "#7A9BB5"
BG        = "#FFFFFF"
CARD      = "#F7F7F7"
TEXT      = "#1A1A2E"
MUTED     = "#555555"

races_per_year = df.drop_duplicates(["year", "raceId"]).groupby("year").size()
years = races_per_year.index.values
vals  = races_per_year.values

fig, ax = plt.subplots(figsize=(12, 6), facecolor=BG)
ax.set_facecolor(CARD)
for sp in ax.spines.values():
    sp.set_visible(False)
ax.tick_params(colors=MUTED, labelsize=9)

ax.fill_between(years, vals, alpha=0.25, color=PRIMARY)
ax.plot(years, vals, color=PRIMARY, linewidth=2.2)
ax.set_xlabel("Year", color=MUTED, fontsize=11)
ax.set_ylabel("Races", color=MUTED, fontsize=11)
ax.set_xlim(years.min(), years.max())
ax.set_ylim(0, vals.max() + 3)
ax.axhline(vals.max(), color=SECONDARY, linewidth=0.8, linestyle="--", alpha=0.5)
ax.text(years[-1] + 0.5, vals[-1],
        f"{vals[-1]} races\n({years[-1]})", color=TEXT, fontsize=9, va="center")

era_shades = [
    (1950, 1966, "Pre-Aerodynamic Era"),
    (1966, 1983, "Ground Effect Era"),
    (1983, 2009, "Turbo & V10/V8 Era"),
    (2009, 2024, "Hybrid Era"),
]
era_colors = ["#ffffff08", "#ffffff05", "#ffffff08", "#ffffff05"]
for (y0, y1, lbl), ec in zip(era_shades, era_colors):
    ax.axvspan(y0, y1, color=ec)
    ax.text((y0 + y1) / 2, vals.max() + 1.5, lbl,
            ha="center", va="bottom", fontsize=7, color=MUTED, style="italic")

ax.set_title("Number of Races per Season (1950–2024)",
             color=TEXT, fontsize=15, fontweight="bold", pad=12)



