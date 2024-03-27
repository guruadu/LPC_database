from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import googlemaps
from database import *

load_dotenv()
API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")

app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    starting_location = request.form['startingLocation']
    state = request.form['state'].lower()
    addresses = get_all_addresses('data.db', state)
    if not addresses:
        return render_template('index.html', error="No addresses in the table for this state")
    
    addresses_with_distance = get_closest_destination(starting_location, addresses, API_KEY)
    
    results = []
    for address, distance in addresses_with_distance[:5]:
        ngo_details = get_ngo_name('data.db', address, state)
        results.append({
            'ngo_details': ngo_details[0],
            'distance': distance
        })
    
    return render_template('index.html', results=results)

if __name__ == "__main__":
    app.run(debug=True)
