import pandas as pd
import matplotlib.pyplot as plt

# Carica il dataset (modifica il percorso se serve)
df = pd.read_csv("mainDataset.csv")

# Pulizia base: rimuove valori mancanti
df = df.dropna(subset=["circuit_name", "fastest_lap_speed_kmh"])

# Calcola la velocità media per circuito
fastest_circuits = (
    df.groupby("circuit_name")["fastest_lap_speed_kmh"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

# Plot
plt.figure()
fastest_circuits.sort_values().plot(kind="barh")

plt.title("Top 10 circuiti più veloci (velocità media giro più veloce)")
plt.xlabel("Velocità media (km/h)")
plt.ylabel("Circuito")

plt.tight_layout()
plt.show()