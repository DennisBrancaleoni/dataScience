import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Caricamento dati
df = pd.read_csv("mainDataset.csv")

# Selezione colonne e pulizia
df = df[['quali_position', 'finish_position']].dropna()

df['quali_position'] = pd.to_numeric(df['quali_position'], errors='coerce')
df['finish_position'] = pd.to_numeric(df['finish_position'], errors='coerce')

df = df.dropna()

# Filtro valori validi
df = df[(df['quali_position'] >= 1) & (df['quali_position'] <= 30)]
df = df[(df['finish_position'] >= 1) & (df['finish_position'] <= 30)]

# Creazione matrice heatmap
heatmap = pd.crosstab(df['quali_position'], df['finish_position'])

# Assicura dimensione 30x30
heatmap = heatmap.reindex(index=range(1,31), columns=range(1,31), fill_value=0)

# Trasformazione logaritmica
data = np.log1p(heatmap)

# Plot
plt.figure(figsize=(10,8))
plt.imshow(data, cmap='turbo', origin='lower')  # <-- asse y parte dal basso

# Assi
plt.xticks(range(30), range(1,31))
plt.yticks(range(30), range(1,31))

plt.xlabel("Race Position")
plt.ylabel("Qualifying Position")
plt.title("Correlation between qualifying result and race result")

# (Opzionale ma consigliato) barra colori
plt.colorbar(label='Log(Frequency + 1)')

plt.show()