import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

df = pd.read_csv("mainDataset.csv", low_memory=False)

PRIMARY = "#2C5F8A"
BG      = "#FFFFFF"
CARD    = "#F7F7F7"
TEXT    = "#1A1A2E"
MUTED   = "#555555"

wins_df    = df[df["finish_position"] == 1]
top_constr = wins_df["constructor_name"].value_counts().head(10)
top_drivers = wins_df["driver_surname"].value_counts().head(10)
races_per_year = df.drop_duplicates(["year", "raceId"]).groupby("year").size()

kpis = [
    ("75 YEARS",              "of F1 History"),
    ("802\nDrivers",          "competed"),
    ("211\nConstructors",     "entered"),
    (f"{int(races_per_year.sum())}\nRaces", "total entries: 26 759"),
    (f"{top_drivers.iloc[0]}\nWins",        f"Record holder: {list(top_drivers.index)[0]}"),
    (f"{int(top_constr.iloc[0])}\nWins",    f"Most wins team: {top_constr.index[0]}"),
]

fig = plt.figure(figsize=(18, 4), facecolor=BG)
gs  = gridspec.GridSpec(1, 6, figure=fig, wspace=0.25,
                        left=0.03, right=0.97, top=0.82, bottom=0.18)

for i, (val, lbl) in enumerate(kpis):
    ax = fig.add_subplot(gs[i])
    ax.set_facecolor(CARD)
    for sp in ax.spines.values():
        sp.set_color(PRIMARY)
        sp.set_linewidth(1.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.text(0.5, 0.60, val, ha="center", va="center",
            fontsize=14, fontweight="bold", color=PRIMARY,
            transform=ax.transAxes, linespacing=1.3)
    ax.text(0.5, 0.22, lbl, ha="center", va="center",
            fontsize=9, color=MUTED,
            transform=ax.transAxes)

