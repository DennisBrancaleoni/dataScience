import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("mainDataset.csv", low_memory=False)
df_pit = df[["start_position", "finish_position", "pit_stop_count"]].dropna()

# Limita a valori sensati
df_pit = df_pit[
    (df_pit["start_position"].between(1, 20)) &
    (df_pit["finish_position"].between(1, 20)) &
    (df_pit["pit_stop_count"].between(1, 6))
]
df_pit["start_position"] = df_pit["start_position"].astype(int)
df_pit["finish_position"] = df_pit["finish_position"].astype(int)

# Matrice: media pit stop per ogni combinazione start/finish
heatmap_data = (
    df_pit.groupby(["finish_position", "start_position"])["pit_stop_count"]
    .mean()
    .unstack(fill_value=np.nan)
)

fig, ax = plt.subplots(figsize=(12, 10))

im = ax.imshow(heatmap_data.values, cmap="coolwarm", aspect="auto",
               vmin=1, vmax=3)

ax.set_xticks(range(len(heatmap_data.columns)))
ax.set_xticklabels([f"P{int(c)}" for c in heatmap_data.columns], fontsize=9)
ax.set_yticks(range(len(heatmap_data.index)))
ax.set_yticklabels([f"P{int(i)}" for i in heatmap_data.index], fontsize=9)

ax.set_xlabel("Start Position", fontsize=13)
ax.set_ylabel("Finish Position", fontsize=13)
ax.set_title("Average Pit Stops: Start Position vs Finish Position\n(color = avg pit stops)", fontsize=14, fontweight="bold")

ax.invert_yaxis()


# Valori nelle celle
for i in range(len(heatmap_data.index)):
    for j in range(len(heatmap_data.columns)):
        val = heatmap_data.values[i, j]
        if not np.isnan(val):
            color = "white" if (val > 2.5 or val < 1.5) else "black"
            ax.text(j, i, f"{val:.1f}", ha="center", va="center", fontsize=7, color=color)

cbar = plt.colorbar(im, ax=ax, label="Average Pit Stops")
cbar.set_ticks([1, 1.5, 2, 2.5, 3])

plt.tight_layout()
plt.savefig("pit_stop_heatmap.png", dpi=150)
plt.show()