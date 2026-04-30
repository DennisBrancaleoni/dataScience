import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

df = pd.read_csv("mainDataset.csv", low_memory=False)

PRIMARY  = "#2C5F8A"
BG       = "#FFFFFF"
CARD     = "#F7F7F7"
TEXT     = "#1A1A2E"
MUTED    = "#555555"

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
    "Finished":                "#3A7D44",
    "Lapped":                  "#2C5F8A",
    "Mechanical":              "#C47A2B",
    "Accident / Collision":    "#A63228",
    "Did Not Qualify / Start": "#6A5A8C",
    "Other":                   "#8A8A8A",
}

fig, ax = plt.subplots(figsize=(8, 8), facecolor=BG)
ax.set_facecolor(CARD)
for sp in ax.spines.values():
    sp.set_visible(False)
ax.set_aspect("equal")
ax.set_facecolor(BG)

order = ["Finished", "Lapped", "Mechanical", "Accident / Collision",
         "Did Not Qualify / Start", "Other"]
sizes = [status_counts.get(o, 0) for o in order]
colors = [STATUS_COLORS[o] for o in order]

wedges, texts, autotexts = ax.pie(
    sizes, labels=None, colors=colors,
    autopct=lambda p: f"{p:.1f}%" if p > 3 else "",
    startangle=90, pctdistance=0.78,
    wedgeprops=dict(width=0.55, edgecolor=CARD, linewidth=2),
)
for at in autotexts:
    at.set_color(TEXT)
    at.set_fontsize(10)
    at.set_fontweight("bold")

patches = [mpatches.Patch(color=STATUS_COLORS[o], label=o) for o in order]
ax.legend(handles=patches, loc="center", frameon=False,
          fontsize=10, labelcolor=TEXT,
          bbox_to_anchor=(0.5, -0.12), ncol=2)

ax.set_title("Race Result Distribution\n(All Entries 1950–2024)",
             color=TEXT, fontsize=15, fontweight="bold", pad=16)
plt.savefig("donut.png", dpi=150, bbox_inches="tight")
plt.show()
