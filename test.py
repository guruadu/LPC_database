import os
from dotenv import load_dotenv

import googlemaps
from main import *
from database import *

def main():
   state = "delhi"
   addresses = get_all_addresses('data.db', state)
   if addresses[0] is None:
      print("no addresses in table for this state")
      exit()
   starting_location = "salaria officers enclave, dwarka"
   closest_dest_address, distance_to_closest = get_closest_destination(starting_location, addresses, API_KEY)
   ngo_details = get_ngo_name('data.db', closest_dest_address, state)
   for details in ngo_details[0]:
      print(details)
   print("Distance to the ngo:", distance_to_closest) 

if(__name__ == "__main__"):
    main()