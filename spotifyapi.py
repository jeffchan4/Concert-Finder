
import requests
import base64
from flask import Flask, request, redirect, session, jsonify, render_template,send_file

from urllib.parse import urlencode
import ticketmasterapi

from googlecloudsql import *





# Define your Spotify app credentials
client_id = "db10f7b93fda4eb9995c51fa223addeb"
client_secret = "cd019f241f19431da6bc569127e6c79b"
redirect_uri = "http://localhost:5000/callback"
scope = "user-top-read, user-read-private, user-read-email"

# Create a Flask app
app = Flask(__name__)

app.secret_key = 'your_secret_key'

# Spotify API endpoints
authorize_url = "https://accounts.spotify.com/authorize"
token_url = "https://accounts.spotify.com/api/token"
top_artists_url = "https://api.spotify.com/v1/me/top/artists"
user_url="https://api.spotify.com/v1/me/"



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
    session['refresh_token'] = response.json().get("refresh_token")
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
    
    top_items= top_artists['items']
    top_artist_names = [item['name'] for item in top_items]
    
    
    # insert_your_artists(session['user_email'],top_artist_names)
    return top_artists

@app.route('/')
def index():
   return send_file(f'../src/login.js', mimetype='application/javascript')
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
    headers = {"Authorization": f"Bearer {access_token}"}
    response= requests.get(user_url, headers=headers)
    user_name=response.json()['display_name']
    user_email= response.json()['email']
    session['user_name']=user_name
    session['user_email']=user_email
    if not query_user(user_email):
        insert_users(user_name,user_email)

   
    return redirect('http://localhost:3000/')

@app.route('/refresh_token', methods=['POST'])
def refresh_token():
    # Extract the user's refresh token from the request
    refresh_token = session['refresh_token']
    
    # Make a POST request to Spotify's token endpoint to refresh the access token
    # Use the refresh token as a parameter to obtain a new access token
    # You may need to use a library like requests or an OAuth2 library for this step

    # Example using the requests library:
   

    CLIENT_ID = client_id
    CLIENT_SECRET = client_secret
    SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'

    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
    }

    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode('utf-8')).decode('utf-8'),
    }

    response = requests.post(SPOTIFY_TOKEN_URL, data=data, headers=headers)
    
    if response.status_code == 200:
        # Parse the response to extract the new access token
        new_access_token = response.json()['access_token']
        
        session['access_token']=new_access_token
        # Return the new access token to the client
        return jsonify({'access_token': new_access_token})
    else:
        # Handle token refresh error (e.g., invalid refresh token)
        return jsonify({'error': 'Token refresh failed'}), 400


    
@app.route('/get_concerts')
def concerts():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
   
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

