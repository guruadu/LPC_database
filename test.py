import os
from dotenv import load_dotenv

import googlemaps
from main import *
from database import *

def main():
   state = "delhi"
   addresses = get_all_addresses('data.db', state)
   if not addresses:
      print("no addresses in table for this state")
      exit()
   starting_location = "Salaria officers enclave, dwarka"
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