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
    
   distances_with_addresses = []
   for i, destination in enumerate(possible_destinations):
        distance = distance_matrix[i].get('distance', {}).get('text', 'Unknown')
        address = destination
        distances_with_addresses.append((address,distance))
    
   sorted_addresses_with_distance = sorted(distances_with_addresses, key=lambda x: x[1])
    
   return sorted_addresses_with_distance

def main():
    #uncomment below line when you want to update db
    #excel_sheets_to_sqlite('maindb.xlsx', 'data.db')
    
   state = input("Enter state: ").lower()
   addresses = get_all_addresses('data.db', state)
   if not addresses:
      print("no addresses in table for this state")
      exit()
   starting_location = input("enter starting location: ")
   
   addresses_with_distance = get_closest_destination(starting_location, addresses, API_KEY)
   
   for i, (address, distance) in enumerate(addresses_with_distance[:5]):
      if i < len(addresses_with_distance):
         ngo_details = get_ngo_name('data.db', address, state)
         for details in ngo_details[0]:
            print(details)
         print("Distance to the ngo:", distance)
         print("\n")


if(__name__ == "__main__"):
    main()