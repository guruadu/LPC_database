from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import googlemaps
from database import *
import math

load_dotenv()
API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")

app = Flask(__name__)

def get_closest_destination(starting_location, possible_destinations, api_key):
    gmaps = googlemaps.Client(key=api_key)
    num_destinations = len(possible_destinations)
    batch_size = 25 
    num_batches = math.ceil(num_destinations / batch_size)
    
    sorted_addresses_with_distance = []
    for i in range(num_batches):
        start_idx = i * batch_size
        end_idx = min((i + 1) * batch_size, num_destinations)
        batch_destinations = possible_destinations[start_idx:end_idx]
        
        response = gmaps.distance_matrix(starting_location, batch_destinations)
        distance_matrix = response['rows'][0]['elements']
        
        distances_with_addresses = []
        for j, destination in enumerate(batch_destinations):
            distance_text = distance_matrix[j].get('distance', {}).get('text', 'Unknown')
            address = destination
            distance = float(distance_text.split()[0]) if distance_text != 'Unknown' else float('inf')
            distances_with_addresses.append((address, distance))
        
        sorted_addresses_with_distance.extend(distances_with_addresses)
    
    sorted_addresses_with_distance.sort(key=lambda x: x[1])  # Sort the combined results
    
    return sorted_addresses_with_distance

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    starting_location = request.form['startingLocation']
    state = request.form['state'].lower()
    db_type = request.form['ngoType']
    addresses = get_all_addresses(db_type, state)
    if not addresses:
        return render_template('index.html', error="No addresses in the table for this state")
    
    addresses_with_distance = get_closest_destination(starting_location, addresses, API_KEY)
    
    results = []
    for address, distance in addresses_with_distance[:10]:
        ngo_details = get_ngo_name(db_type, address, state)
        results.append({
            'ngo_details': ngo_details[0],
            'distance': distance
        })
    
    return render_template('index.html', results=results)

if __name__ == "__main__":
    #excel_sheets_to_sqlite('testdb.xlsx','test.db')
    app.run(debug=True)
