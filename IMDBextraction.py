import requests
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.colors import LinearSegmentedColormap as lsc
import json
import numpy as np

Shows = {
    "RickAndMorty" : "tt2861424",
    "Archer" : "tt1486217",
    "BreakingBad" : "tt0903747",
    "ParksAndRecreation" : "tt1266020",
    "AOT" : "tt2560140",
    "RvB" : "tt0401747",
    "TeenWolf" : "tt1567432",
    "Simpsons" : "tt0096697",
    "ModernFamily" : "tt1442437",
    "SouthPark" : "tt0121955",
    "GameOfThrones" : "tt0944947",
    "House" : "tt0412142"
}

def fetch_imdb_data(show_name):
    url = f"https://api.imdbapi.dev/titles/{Shows.get(show_name)}/episodes"

    params = {"pageSize": 50}
    
    all_episodes = []

    while True:
        response = requests.get(url, params)
        response.raise_for_status()
        data = response.json()

        all_episodes.extend(data.get("episodes", []))

        next_page = data.get("nextPageToken")
        if not next_page:
            break
        params["pageToken"] = next_page

    with open(f"{show_name}.json", "w", encoding="utf-8") as f:
        json.dump(all_episodes, f, indent=2, ensure_ascii=False)

    print(all_episodes)

def generate_heatmap(show_name):
    with open(f"{show_name}.json", "r") as file:
        data = json.load(file)


    all_episodes = []

    for episode in data:
        if "rating" not in episode or "unknown" in episode.get("season") or not episode.get("episodeNumber"):
            continue
        rating = episode.get("rating").get("aggregateRating")
        epNum = episode.get("episodeNumber")
        season = episode.get("season")
        all_episodes.append([int(season), int(epNum), rating])
    
    sorted_episodes = sorted(all_episodes, key=lambda ep: (ep[0], ep[1]))
    print(sorted_episodes)
    
    Ratings2D = []
    currSeasonNum = "1"
    currSeason = []
    for episode in sorted_episodes:
        if episode[0] is not currSeasonNum:
            currSeasonNum = episode[0]
            Ratings2D.append(currSeason)
            currSeason = []
        currSeason.append(float(episode[2])/10)
    Ratings2D.append(currSeason)

    maxEps = max(len(season) for season in Ratings2D)
    padded = [season + [np.nan]*(maxEps - len(season)) for season in Ratings2D]
    Ratings2D = np.array(padded)

    norm = colors.Normalize(vmin=0.4, vmax=1)
    traffic_lights = lsc.from_list("traffic_lights", ["#2b0000", "red", "#FFD300", "green"])

    plt.imshow(Ratings2D, cmap=traffic_lights, norm=norm, interpolation="nearest")
    plt.title(f"{show_name}")
    plt.show()
    
def new_heat_map(show_name):
    fetch_imdb_data(show_name)
    generate_heatmap(show_name)

generate_heatmap("AOT")
generate_heatmap("BreakingBad")
generate_heatmap("Archer")
generate_heatmap("RickAndMorty")
generate_heatmap("ParksAndRecreation")
new_heat_map("House")