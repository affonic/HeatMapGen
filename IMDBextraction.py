import requests
import matplotlib

def fetch_imdb_data(show_id):
    url = f"https://api.imdbapi.dev/titles/{show_id}/episodes?pageSize=50"
    response = requests.get(url)
    data = response.json()
    print(data)

fetch_imdb_data("tt2861424")