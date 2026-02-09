# How to connect to an API using python
import requests
import json
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_DIR = os.path.join(ROOT_DIR, "data")

base_url = "https://pokeapi.co/api/v2/"

def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def get_pokemon_info(name):
    url = f"{base_url}/pokemon/{name}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
    
def save_json(data):
    ensure_data_dir()
    filename = f"{data["name"]}.json" 
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def main():
    pokemon_name = sys.argv[1] if len(sys.argv) > 1 else "charizard"
    pokemon_info = get_pokemon_info(pokemon_name)

    if pokemon_info:
        print(f"Name: {pokemon_info["name"].capitalize()}")
        print(f"Height: {pokemon_info["height"]}")
        print(f"Weight: {pokemon_info["weight"]}")
        save_json(pokemon_info)

if __name__ == "__main__":
    main()