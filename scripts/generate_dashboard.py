import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

df = pd.read_csv("mainDataset.csv", low_memory=False)

# ── Palette ──────────────────────────────────────────────────────────────────
F1_RED   = "#E10600"
F1_BLACK = "#15151E"
F1_SILVER = "#B0B7C3"
F1_GOLD  = "#FFD700"
BG       = "#0F0F14"
CARD     = "#1A1A24"
TEXT     = "#FFFFFF"
MUTED    = "#8A8A9A"

CONSTRUCTOR_COLORS = {
    "Ferrari":   "#DC0000",
    "McLaren":   "#FF8000",
    "Mercedes":  "#00D2BE",
    "Red Bull":  "#3671C6",
    "Williams":  "#005AFF",
    "Team Lotus":"#FFE400",
    "Renault":   "#FFF500",
    "Benetton":  "#00A550",
    "Brabham":   "#006EFF",
    "Tyrrell":   "#FAFAFA",
}

# ── Data prep ────────────────────────────────────────────────────────────────
wins_df = df[df["finish_position"] == 1]

# 1. Top-10 constructors by wins
top_constr = wins_df["constructor_name"].value_counts().head(10)

# 2. Top-10 drivers by wins
top_drivers = wins_df["driver_surname"].value_counts().head(10)
top_drivers_fn = {
    row["driver_surname"]: row["driver_forename"]
    for _, row in df[df["driver_surname"].isin(top_drivers.index)].drop_duplicates("driver_surname").iterrows()
}


# 4. Race finish status
fin_map = {
    "Finished":          "Finished",
    "+1 Lap":            "Lapped",
    "+2 Laps":           "Lapped",
    "+3 Laps":           "Lapped",
    "+4 Laps":           "Lapped",
    "+5 Laps":           "Lapped",
    "Engine":            "Mechanical",
    "Gearbox":           "Mechanical",
    "Hydraulics":        "Mechanical",
    "Electrical":        "Mechanical",
    "Suspension":        "Mechanical",
    "Brakes":            "Mechanical",
    "Transmission":      "Mechanical",
    "Accident":          "Accident / Collision",
    "Collision":         "Accident / Collision",
    "Spun off":          "Accident / Collision",
    "Did not qualify":   "Did Not Qualify / Start",
    "Did not prequalify":"Did Not Qualify / Start",
}
df["status_group"] = df["status"].map(fin_map).fillna("Other")
status_counts = df["status_group"].value_counts()
STATUS_COLORS = {
    "Finished":                "#2ecc71",
    "Lapped":                  "#3498db",
    "Mechanical":              "#e67e22",
    "Accident / Collision":    "#e74c3c",
    "Did Not Qualify / Start": "#9b59b6",
    "Other":                   "#7f8c8d",
}

# 5. Races per year trend
races_per_year = df.drop_duplicates(["year", "raceId"]).groupby("year").size()

# ── Figure ───────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(22, 26), facecolor=BG)
fig.patch.set_facecolor(BG)

gs = gridspec.GridSpec(
    4, 2,
    figure=fig,
    hspace=0.55, wspace=0.35,
    left=0.07, right=0.96,
    top=0.93, bottom=0.05,
)

def card_ax(gs_cell):
    ax = fig.add_subplot(gs_cell)
    ax.set_facecolor(CARD)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.tick_params(colors=MUTED, labelsize=10)
    return ax

# ── Header ───────────────────────────────────────────────────────────────────
fig.text(0.5, 0.965, "FORMULA 1 WORLD CHAMPIONSHIP", ha="center",
         fontsize=34, fontweight="bold", color=TEXT, fontfamily="DejaVu Sans")
fig.text(0.5, 0.950, "1950 – 2024  |  26 759 race entries  •  802 drivers  •  211 constructors",
         ha="center", fontsize=13, color=MUTED)
# Red accent line
fig.add_artist(plt.Line2D([0.07, 0.96], [0.945, 0.945],
               transform=fig.transFigure, color=F1_RED, linewidth=3))


# ── 4. Race Result Distribution (donut) ──────────────────────────────────────
ax4 = card_ax(gs[2, 0])
ax4.set_aspect("equal")
order = ["Finished", "Lapped", "Mechanical", "Accident / Collision",
         "Did Not Qualify / Start", "Other"]
sizes = [status_counts.get(o, 0) for o in order]
colors4 = [STATUS_COLORS[o] for o in order]
wedges, texts, autotexts = ax4.pie(
    sizes, labels=None, colors=colors4,
    autopct=lambda p: f"{p:.1f}%" if p > 3 else "",
    startangle=90, pctdistance=0.78,
    wedgeprops=dict(width=0.55, edgecolor=CARD, linewidth=2),
)
for at in autotexts:
    at.set_color(TEXT)
    at.set_fontsize(9)
    at.set_fontweight("bold")
patches = [mpatches.Patch(color=STATUS_COLORS[o], label=o) for o in order]
ax4.legend(handles=patches, loc="center", frameon=False,
           fontsize=9, labelcolor=TEXT,
           bbox_to_anchor=(0.5, -0.18), ncol=2)
ax4.set_title("Race Result Distribution\n(All Entries 1950–2024)",
              color=TEXT, fontsize=13, fontweight="bold", pad=12)

# ── 5. Number of Races per Year ───────────────────────────────────────────────
ax5 = card_ax(gs[2, 1])
years = races_per_year.index.values
vals5 = races_per_year.values
ax5.fill_between(years, vals5, alpha=0.25, color=F1_RED)
ax5.plot(years, vals5, color=F1_RED, linewidth=2.2)
ax5.set_xlabel("Year", color=MUTED, fontsize=11)
ax5.set_ylabel("Races", color=MUTED, fontsize=11)
ax5.tick_params(colors=MUTED, labelsize=9)
ax5.set_xlim(years.min(), years.max())
ax5.set_ylim(0, vals5.max() + 3)
ax5.axhline(vals5.max(), color=F1_SILVER, linewidth=0.8, linestyle="--", alpha=0.5)
ax5.text(years[-1] + 0.5, vals5[-1],
         f"{vals5[-1]} races\n({years[-1]})", color=TEXT, fontsize=9, va="center")
# Shade major eras
era_shades = [(1950,1966,"Pre-Aerodynamic Era"),(1966,1983,"Ground Effect Era"),
              (1983,2009,"Turbo & V10/V8 Era"),(2009,2024,"Hybrid Era")]
era_colors = ["#ffffff08","#ffffff05","#ffffff08","#ffffff05"]
for (y0, y1, lbl), ec in zip(era_shades, era_colors):
    ax5.axvspan(y0, y1, color=ec)
    ax5.text((y0+y1)/2, vals5.max()+1.5, lbl,
             ha="center", va="bottom", fontsize=7, color=MUTED, style="italic")
ax5.set_title("Number of Races per Season (1950–2024)",
              color=TEXT, fontsize=13, fontweight="bold", pad=12)

# ── 6. KPI tiles (bottom row) ────────────────────────────────────────────────
kpis = [
    ("75 YEARS", "of F1 History"),
    ("802\nDrivers", "competed"),
    ("211\nConstructors", "entered"),
    (f"{int(races_per_year.sum())}\nRaces", "total entries: 26 759"),
    (f"{top_drivers.iloc[0]}\nWins", f"Record holder: {list(top_drivers.index)[0]}"),
    (f"{int(top_constr.iloc[0])}\nWins", f"Most wins team: {top_constr.index[0]}"),
]
gs_kpi = gridspec.GridSpecFromSubplotSpec(1, 6, subplot_spec=gs[3, :],
                                          wspace=0.25)
for i, (val, lbl) in enumerate(kpis):
    ax_k = fig.add_subplot(gs_kpi[i])
    ax_k.set_facecolor(CARD)
    for sp in ax_k.spines.values():
        sp.set_color(F1_RED)
        sp.set_linewidth(1.5)
    ax_k.set_xticks([])
    ax_k.set_yticks([])
    ax_k.text(0.5, 0.58, val, ha="center", va="center",
              fontsize=13, fontweight="bold", color=F1_RED,
              transform=ax_k.transAxes, linespacing=1.3)
    ax_k.text(0.5, 0.22, lbl, ha="center", va="center",
              fontsize=8.5, color=MUTED,
              transform=ax_k.transAxes)

# ── Footer ────────────────────────────────────────────────────────────────────
fig.text(0.5, 0.022, "Data source: Ergast F1 API  |  Visualization: F1 Project 2025–26",
         ha="center", fontsize=9, color=MUTED)

out = "F1_Dashboard_Overview.png"
plt.savefig(out, dpi=180, bbox_inches="tight", facecolor=BG)
print(f"Saved → {out}")
