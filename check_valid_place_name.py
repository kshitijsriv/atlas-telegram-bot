import pycountry
import requests
import json


# Function to load valid places from the JSON file
def load_valid_places(file_path='valid_places.json'):
    with open(file_path, 'r') as file:
        places = json.load(file)
    return places


# Function to save a new place to the JSON file
def save_valid_place(place_name, file_path='valid_places.json'):
    places = load_valid_places(file_path)
    places.append(place_name)
    with open(file_path, 'w') as file:
        json.dump(places, file)


def is_valid_country(input_name):
    try:
        country = pycountry.countries.get(name=input_name)
        if country:
            return True
    except KeyError:
        return False
    return False


def is_valid_state(input_name):
    for subdivision in pycountry.subdivisions:
        if subdivision.name == input_name:
            return True
    return False


def is_valid_city(city_name):
    url = f"http://geodb-free-service.wirefreethought.com/v1/geo/cities?namePrefix={city_name}"
    response = requests.get(url)
    data = response.json()

    # If the city exists, the API will return results
    return len(data['data']) > 0


def is_valid_custom_place(input_name, valid_places_names):
    if valid_places_names:
        return input_name.strip().lower() in valid_places_names
    return False


def is_valid_location(input_name, valid_places_names=None):
    if is_valid_country(input_name):
        return True
    elif is_valid_state(input_name):
        return True
    elif is_valid_city(input_name):
        return True
    elif is_valid_custom_place(input_name, valid_places_names):
        return True
    else:
        return False


if __name__ == '__main__':
    valid_places = load_valid_places('data/valid_places.json')
    # Example usage
    print(is_valid_location("Lucknow"))  # Country
    print(is_valid_location("California"))  # State
    print(is_valid_location("dehradun"))  # City
    print(is_valid_location("manipur"))  # Not valid
