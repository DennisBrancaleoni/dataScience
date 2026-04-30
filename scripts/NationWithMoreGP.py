import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("mainDataset.csv", low_memory=False)
gare_uniche = df.drop_duplicates(subset="raceId")[["raceId", "country", "year"]]

gare_per_paese = (
    gare_uniche.groupby("country").size()
    .reset_index(name="n_gare")
    .sort_values("n_gare", ascending=False)
)

gare_uniche["decennio"] = (gare_uniche["year"] // 10 * 10).astype(str) + "s"

gare_decennio = (
    gare_uniche.groupby(["country", "decennio"]).size()
    .reset_index(name="n_gare")
)

# Tieni SOLO i top 5 per ogni decennio, gli altri → 0
top5_mask = (
    gare_decennio.sort_values("n_gare", ascending=False)
    .groupby("decennio")
    .head(5)
)

pivot = (
    top5_mask.pivot(index="decennio", columns="country", values="n_gare")
    .fillna(0)
)

FLAG_COLORS = {
    "Italy":        "#009246",
    "Germany":      "#FFD700",
    "UK":           "#CF111A",
    "USA":          "#3C3B6E",
    "Monaco":       "#00CED1",
    "Belgium":      "#FF8C00",
    "France":       "#4169E1",
    "Spain":        "#F01843",
    "Canada":       "#FF6347",
    "Brazil":       "#228B22",
    "Japan":        "#8B0000",
    "Austria":      "#DB7093",
    "Hungary":      "#74CC9A",
    "Australia":    "#191970",
    "Netherlands":  "#FF4500",
    "Mexico":       "#556B2F",
    "South Africa": "#DAA520",
    "Bahrain":      "#9400D3",
    "Argentina":    "#87CEEB",
    "Malaysia":     "#8B4513",
    "Switzerland":  "#A9A9A9",
    "Sweden":       "#4682B4",
    "Portugal":     "#006400",
    "China":        "#FF1493",
}

fig, axes = plt.subplots(1, 2, figsize=(20, 7))
fig.suptitle("Paesi con più Gare F1 nel Tempo (1950–2024)", fontsize=14, fontweight="bold")

# --- Grafico 1: Top 20 totale, tutto blu ---
top20 = gare_per_paese.head(20)
blues = plt.cm.Blues([0.3 + 0.7 * i / len(top20) for i in range(len(top20))])
bars = axes[0].barh(top20["country"][::-1], top20["n_gare"][::-1], color=blues, edgecolor="white")
axes[0].set_title("Top 20 Paesi — Totale Gare")
axes[0].set_xlabel("Numero di Gare")
for bar, val in zip(bars, top20["n_gare"][::-1]):
    axes[0].text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                 str(val), va="center", fontsize=8)

# --- Grafico 2: Solo top 5 per decennio ---
decenni = sorted(pivot.index.tolist())
bottom = np.zeros(len(decenni))
x = np.arange(len(decenni))

for paese in pivot.columns:
    valori = [pivot.loc[d, paese] if d in pivot.index else 0 for d in decenni]
    if sum(valori) == 0:
        continue
    color = FLAG_COLORS.get(paese, "#AAAAAA")
    axes[1].bar(x, valori, bottom=bottom, label=paese, color=color, edgecolor="white")
    bottom += np.array(valori)

axes[1].set_title("Top 5 Paesi per Gare — per Decennio")
axes[1].set_xlabel("Decennio")
axes[1].set_ylabel("Numero di Gare")
axes[1].set_xticks(x)
axes[1].set_xticklabels(decenni, rotation=45)
axes[1].legend(title="Paese", bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=8)

plt.tight_layout()
plt.savefig("gare_per_paese.png", dpi=150)
plt.show()