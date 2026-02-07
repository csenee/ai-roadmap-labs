# How to connect to an API using python
import requests
import json
from pathlib import Path
import os

base_url = "https://pokeapi.co/api/v2/"
#DATA_DIR = Path("data")
#DATA_DIR.mkdir(exist_ok=True)

def get_pokemon_info(name):
    url = f"{base_url}/pokemon/{name}"
    response = requests.get(url)
    
    if response.status_code == 200:
        pokemon_data = response.json()
        return pokemon_data
    else:
        print(f"Failed to retrieve data {response.status_code}")
    
def save_json(data):
    #path = DATA_DIR / f"{data["name"]}.json"
    path = os.path.expanduser("~") + f"\\Documents\\Business\\Programming\\ai-roadmap-labs\\data\\{data["name"]}.json"
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


pokemon_name = "charizard"
pokemon_info = get_pokemon_info(pokemon_name)


if pokemon_info:
    print(f"Name: {pokemon_info["name"].capitalize()}")
    print(f"Height: {pokemon_info["height"]}")
    print(f"Weight: {pokemon_info["weight"]}")
    save_json(pokemon_info)