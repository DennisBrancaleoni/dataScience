import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("mainDataset.csv", low_memory=False)
df_pit = df[["pit_stop_count", "finish_position"]].dropna()

avg_pos = (
    df_pit.groupby("pit_stop_count")["finish_position"]
    .agg(["mean", "count"])
    .reset_index()
    .rename(columns={"mean": "pos_media", "count": "n_gare"})
)
avg_pos = avg_pos[avg_pos["n_gare"] >= 30]

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("Correlazione Pit Stop ↔ Posizione Finale", fontsize=14, fontweight="bold")

# Scatter
axes[0].scatter(df_pit["pit_stop_count"], df_pit["finish_position"], alpha=0.1, s=8, color="steelblue")
m, b = pd.Series(df_pit["pit_stop_count"]).corr(df_pit["finish_position"]), None
import numpy as np
coef = np.polyfit(df_pit["pit_stop_count"], df_pit["finish_position"], 1)
x_line = range(int(df_pit["pit_stop_count"].min()), int(df_pit["pit_stop_count"].max()) + 1)
axes[0].plot(x_line, [coef[0]*x + coef[1] for x in x_line], color="red", linewidth=2)
axes[0].set_title("Scatter + Linea di Tendenza")
axes[0].set_xlabel("Numero Pit Stop")
axes[0].set_ylabel("Posizione Finale")
r = df_pit["pit_stop_count"].corr(df_pit["finish_position"])
axes[0].text(0.05, 0.92, f"r = {r:.2f}", transform=axes[0].transAxes, color="red", fontsize=10)

# Posizione media per n° pit stop
axes[1].bar(avg_pos["pit_stop_count"], avg_pos["pos_media"], color="steelblue", edgecolor="white")
axes[1].set_title("Posizione Media per N° Pit Stop")
axes[1].set_xlabel("Numero Pit Stop")
axes[1].set_ylabel("Posizione Media")
axes[1].invert_yaxis()
for i, row in avg_pos.iterrows():
    axes[1].text(row["pit_stop_count"], row["pos_media"] + 0.3, f"{row['pos_media']:.1f}", ha="center", fontsize=8)

plt.tight_layout()
plt.savefig("pit_stop_correlation.png", dpi=150)
plt.show()