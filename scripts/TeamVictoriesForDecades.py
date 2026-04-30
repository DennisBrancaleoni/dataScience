import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("mainDataset.csv")

winners = df[df["finish_position"] == 1].copy()

winners["decade"] = (winners["year"] // 10) * 10

wins_by_decade = winners.groupby(["decade", "constructor_name"]).size().unstack(fill_value=0)

top_teams = wins_by_decade.sum().sort_values(ascending=False).head(10).index
wins_by_decade = wins_by_decade[top_teams]

wins_by_decade.index = [f"{d}s" for d in wins_by_decade.index]

colors = {
    "Ferrari": "#DC0000",      # rosso Ferrari
    "Red Bull": "#000E5F",     # blu Red Bull
    "Mercedes": "#00D2BE",     # azzurro Mercedes
    "Renault": "#FFF500",      # giallo Renault
    "Williams": "#2370FF",     # blu Williams (diverso!)
    "McLaren": "#FF8700",
    "Team Lotus": "#1E551F",
    "Benetton": "#33B536",
    "Brabham": "gray",
    "Tyrrell": "#6696BB"
}

default_colors = plt.cm.tab20.colors
color_list = []

for i, team in enumerate(wins_by_decade.columns):
    if team in colors:
        color_list.append(colors[team])
    else:
        color_list.append(default_colors[i % len(default_colors)])

wins_by_decade.plot(kind="bar", stacked=True, figsize=(12,7), color=color_list)

plt.xlabel("Decades")
plt.ylabel("Number of victory")
plt.title("Team victories for decades")

plt.legend(title="Scuderia", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()

plt.show()