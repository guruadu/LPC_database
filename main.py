import os
from dotenv import load_dotenv

import googlemaps
from database import *

load_dotenv()
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def get_closest_destination(starting_location, possible_destinations, api_key):
    gmaps = googlemaps.Client(key=api_key)
    
    response = gmaps.distance_matrix(starting_location, possible_destinations)
    distance_matrix = response['rows'][0]['elements']
    
    min_distance_index = min(range(len(distance_matrix)), key=lambda i: distance_matrix[i].get('distance', {}).get('value', float('inf')))
    closest_destination = possible_destinations[min_distance_index]
    distance_to_closest = distance_matrix[min_distance_index].get('distance', {}).get('text', 'Unknown')
    
    return closest_destination, distance_to_closest

def main():
    #uncomment below line when you want to update db
    #excel_sheets_to_sqlite('maindb.xlsx', 'data.db')
    state = input("Enter state: ").lower()
    addresses = get_all_addresses('data.db', state)
    if not addresses:
        print("no addresses in table for this state")
        exit()
    starting_location = input("enter starting location: ")
    closest_dest_address, distance_to_closest = get_closest_destination(starting_location, addresses, API_KEY)
    ngo_details = get_ngo_name('data.db', closest_dest_address, state)
    for details in ngo_details[0]:
        print(details)
    print("Distance to the ngo:", distance_to_closest)  


if(__name__ == "__main__"):
    main()