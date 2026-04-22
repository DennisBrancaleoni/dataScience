import pandas as pd
import matplotlib.pyplot as plt

# Carica il dataset
df = pd.read_csv("mainDataset.csv")

# Pulizia: rimuove valori mancanti
df = df.dropna(subset=["year", "pit_stop_count"])

# Calcola media pit stop per anno
pitstop_trend = (
    df.groupby("year")["pit_stop_count"]
    .mean()
    .sort_index()
)

# Grafico
plt.figure()
pitstop_trend.plot(marker='o')

plt.title("Numero medio di pit stop nel tempo")
plt.xlabel("Anno")
plt.ylabel("Pit stop medi")

plt.grid(True)
plt.tight_layout()
plt.show()