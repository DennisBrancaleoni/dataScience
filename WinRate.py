import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("mainDataset.csv", low_memory=False)

win_rate = (
    df.groupby(["driver_forename", "driver_surname"])
    .agg(
        gare_disputate=("finish_position", "count"),
        vittorie=("finish_position", lambda x: (x == 1.0).sum()),
    )
    .reset_index()
)

win_rate["win_rate_%"] = (win_rate["vittorie"] / win_rate["gare_disputate"] * 100).round(2)
win_rate["pilota"] = win_rate["driver_forename"] + " " + win_rate["driver_surname"]
win_rate = win_rate[win_rate["gare_disputate"] >= 50].sort_values("win_rate_%", ascending=False).head(20)

fig, ax = plt.subplots(figsize=(10, 8))
colors = ["gold" if i == 0 else "steelblue" for i in range(len(win_rate))]
ax.barh(win_rate["pilota"][::-1], win_rate["win_rate_%"][::-1], color=colors[::-1], edgecolor="white")
ax.set_title("Top 20 Piloti F1 per Win Rate (min. 50 gare)", fontsize=13, fontweight="bold")
ax.set_xlabel("Win Rate (%)")
for i, val in enumerate(win_rate["win_rate_%"][::-1]):
    ax.text(val + 0.3, i, f"{val}%", va="center", fontsize=9)

plt.tight_layout()
plt.savefig("win_rate_piloti.png", dpi=150)
plt.show()