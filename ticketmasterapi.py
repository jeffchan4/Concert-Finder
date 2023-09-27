import requests
def get_near_events(artist_name, location):
    # Replace 'YOUR_API_KEY' with your actual Ticketmaster API key
    api_key = '	sA1PvXgvPPZAlLvyKo9wA1A2GHV3RqDB'



    # Ticketmaster API endpoint for searching events
    base_url = 'https://app.ticketmaster.com/discovery/v2/events.json'

    # Parameters for artist, event, and location search
    params = {
        'apikey': api_key,
        'keyword': artist_name,
        'classificationName': 'music',  # You can specify the type of event (e.g., music)
        'city': location  # Specify the city for location-based search
    }

    # Make the request to search for artist events near the specified location
    response = requests.get(base_url, params=params)

    # Parse the JSON response
    data = response.json()
    events_list=[]
    # Check if any events were found
    if 'page' in data and 'totalElements' in data['page'] and data['page']['totalElements'] > 0:
        events = data['_embedded']['events']
        
        if events:
            # Process and display the upcoming events
            for event in events:
                events_list.append(f"Event Name: {event['name']}")
                events_list.append(f"Date: {event['dates']['start']['localDate']}")
                events_list.append(f"Venue: {event['_embedded']['venues'][0]['name']}")
                events_list.append(f"Location: {event['_embedded']['venues'][0]['city']['name']}, {event['_embedded']['venues'][0]['state']['name']}, {event['_embedded']['venues'][0]['country']['name']}")
                
        else:
            events_list.append(f"No upcoming events found for {artist_name} near {location}")
    else:
        events_list.append(f"No upcoming events found for {artist_name} near {location}")
    return events_list
