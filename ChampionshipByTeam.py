import pandas as pd
import matplotlib.pyplot as plt

# Carica il dataset
df = pd.read_csv("mainDataset.csv")

# Filtra solo le vittorie (posizione finale = 1)
wins = df[df["finish_position"] == 1]

# Conta le vittorie per scuderia
top_teams = (
    wins.groupby("constructor_name")["finish_position"]
    .count()
    .sort_values(ascending=False)
    .head(10)
)

# Grafico
plt.figure()
top_teams.sort_values().plot(kind="barh")

plt.title("Top 10 scuderie più vincenti")
plt.xlabel("Numero di vittorie")
plt.ylabel("Scuderia")

plt.tight_layout()
plt.show()