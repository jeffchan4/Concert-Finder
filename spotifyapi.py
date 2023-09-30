import time
import requests
import base64
from flask import Flask, request, redirect, session, jsonify, render_template
from flask_cors import CORS
from urllib.parse import urlencode
import ticketmasterapi

# Define your Spotify app credentials
client_id = "db10f7b93fda4eb9995c51fa223addeb"
client_secret = "cd019f241f19431da6bc569127e6c79b"
redirect_uri = "http://localhost:5000/callback"
scope = "user-top-read"

# Create a Flask app
app = Flask(__name__)
CORS(app)
app.secret_key = 'your_secret_key'

# Spotify API endpoints
authorize_url = "https://accounts.spotify.com/authorize"
token_url = "https://accounts.spotify.com/api/token"
top_artists_url = "https://api.spotify.com/v1/me/top/artists"

# Function to generate the authorization URL
def generate_authorization_url():
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": scope,
    }
    query_params = urlencode(params)
    return f"{authorize_url}?{query_params}"

# Function to exchange the authorization code for an access token
def exchange_code_for_access_token(code):
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()}"
    }
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri
    }
    response = requests.post(token_url, data=data, headers=headers)
    return response.json().get("access_token")

# Function to get the user's top artists
def get_top_artists(access_token, time_range):
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"time_range": time_range, "limit":1}
    response = requests.get(top_artists_url, params=params, headers=headers)
    return response.json()

@app.route('/get_top_artists')
def getartists():

    time=request.args.get('time')
    
    top_artists = get_top_artists(session['access_token'], time)
    
    return top_artists

@app.route('/')
def index():
    return render_template('index.html')
# Route to initiate the Spotify authorization process
@app.route('/login')
def login():
    authorization_url = generate_authorization_url()
    return redirect(authorization_url)

# Route to handle the Spotify callback and fetch top artists
@app.route('/callback')
def callback():
    
    code = request.args.get('code')
    access_token = exchange_code_for_access_token(code)
    session['access_token'] = access_token
    print(session['access_token'])
    return redirect('http://localhost:3000/')




    
@app.route('/get_concerts')
def concerts():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    print(latitude)
    print(longitude)
    print('testing')

    time=request.args.get('time')
    
    # Fetch the user's top artists for the last month (you can change the time range)
    top_artists = get_top_artists(session['access_token'], time)
    
    artist_items = top_artists.get('items', [])

    artist_names = []
    artist_images = []
    event_details=[]
    for artist in artist_items:
        
        name = artist['name']
        
        images = artist['images'][2]["url"]
        artist_names.append(name)
        artist_images.append(images)
    
    for artist in artist_names:
        
        event_details.append(ticketmasterapi.get_near_events(artist,latitude,longitude))
    
    return(event_details)
    

if __name__ == '__main__':
    app.run(debug=True)

