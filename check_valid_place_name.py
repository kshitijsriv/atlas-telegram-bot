import pycountry
import requests


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


def is_valid_location(input_name):
    if is_valid_country(input_name):
        return True
    elif is_valid_state(input_name):
        return True
    elif is_valid_city(input_name):
        return True
    else:
        return False


if __name__ == '__main__':
    # Example usage
    print(is_valid_location("Lucknow"))      # Country
    print(is_valid_location("California")) # State
    print(is_valid_location("dehradun"))   # City
    print(is_valid_location("inida"))   # Not valid
