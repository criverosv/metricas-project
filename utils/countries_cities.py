import json


def get_all_countries():
    countries = {}
    with open("utils/countries_states_cities.json") as jsonFile:
        file_content = json.load(jsonFile)
        all_content = file_content["Countries"]
        for element in all_content:
            countries[element["CountryName"]] = element["CountryName"]
    return countries


def get_all_cities_from_country(country):
    cities_by_country = {}
    with open("utils/countries_states_cities.json") as jsonFile:
        file_content = json.load(jsonFile)
        all_content = file_content["Countries"]
        for element in all_content:
            country_name = element["CountryName"]
            states = element["States"]
            cities = []
            for state in states:
                cities += state["Cities"]
            sorted_cities = sorted(cities)
            cities_by_country[country_name] = {city: city for city in sorted_cities}
    return cities_by_country[country]
