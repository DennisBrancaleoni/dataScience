import pandas as pd
import matplotlib.pyplot as plt

# Caricamento dataset
df = pd.read_csv("mainDataset.csv")

# Tieni solo colonne utili
df = df[['year', 'fastest_lap_time']].dropna()

# --- Conversione tempo giro veloce in secondi ---
def lap_to_seconds(lap_time):
    try:
        if isinstance(lap_time, str) and ':' in lap_time:
            minutes, seconds = lap_time.split(':')
            return int(minutes) * 60 + float(seconds)
        return float(lap_time)
    except:
        return None

df['fastest_lap_seconds'] = df['fastest_lap_time'].apply(lap_to_seconds)

# Rimuovi valori non validi
df = df.dropna(subset=['fastest_lap_seconds'])

# --- Media giro veloce per anno ---
yearly = df.groupby('year')['fastest_lap_seconds'].mean().reset_index()

# Ordina per anno
yearly = yearly.sort_values('year')

# --- Plot ---
plt.figure(figsize=(10,6))

plt.plot(yearly['year'], yearly['fastest_lap_seconds'], marker='o')

plt.xlabel("Anno")
plt.ylabel("Tempo giro veloce (secondi)")
plt.title("Evoluzione dei giri veloci negli anni")

plt.grid(True)

plt.show()