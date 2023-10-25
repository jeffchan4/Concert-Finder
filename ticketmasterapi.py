import requests

# def get_artist_ids(artist_name):## get artist ids and then put them in a list
#     api_key = '	sA1PvXgvPPZAlLvyKo9wA1A2GHV3RqDB'
#     base_url='https://app.ticketmaster.com/discovery/v2/attractions.json'
#     params={
#         'keyword':
#     }
#     pass
# def testfunc():
#     # Replace 'YOUR_API_KEY' with your actual Ticketmaster API key
#     api_key = '	sA1PvXgvPPZAlLvyKo9wA1A2GHV3RqDB'



#     # Ticketmaster API endpoint for searching events
#     base_url = f'https://app.ticketmaster.com/discovery/v2/attractions.json?keyword=Joji&countryCode=US&apikey={api_key}'

#     response = requests.get(base_url)
    
#     # Parse the JSON response
#     data = response.json()
    
#     print(data['_embedded']['attractions'][0]['classifications'])

    
# def get_attraction():
#     api_key = '	sA1PvXgvPPZAlLvyKo9wA1A2GHV3RqDB'



#     # Ticketmaster API endpoint for searching events
#     base_url = 'https://app.ticketmaster.com/discovery/v2/events.json'

#     # Parameters for artist, event, and location search
#     params = {
#         'apikey': api_key,

#         'keyword': 'Bad Bunny',
#         'classificationName': 'music',  # You can specify the type of event (e.g., music)
#         # 'latlong': f'{latitude},{longitude}' ,
#         # 'genreId':'KnvZfZ7vAv1',
#         'city': 'Toronto',
#         'size': 1,
        
#     }

#     # Make the request to search for artist events near the specified location
#     response = requests.get(base_url, params=params)
    
#     # Parse the JSON response
#     data = response.json()
#     print(data)
    # Parse the JSON response
    

def get_near_events(artist_name, latitude,longitude):
    # Replace 'YOUR_API_KEY' with your actual Ticketmaster API key
    api_key = '	sA1PvXgvPPZAlLvyKo9wA1A2GHV3RqDB'



    # Ticketmaster API endpoint for searching events
    base_url = 'https://app.ticketmaster.com/discovery/v2/events.json'

    # Parameters for artist, event, and location search
    params = {
        'apikey': api_key,
        'keyword': artist_name,
        'classificationName': 'music',  # You can specify the type of event (e.g., music)
        # 'latlong': f'{latitude},{longitude}' ,
        
        'city':'Toronto',
        'size': 1,
        
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
                event_id=event['id']
                event_url=f"https://app.ticketmaster.com/discovery/v2/events/{event_id}.json?apikey={api_key}"
                response=requests.get(event_url)
                event_data= response.json()
               
                buy_ticket_url = event_data['url']
                

                events_list.append(f"Event url: {buy_ticket_url} " )
                events_list.append(f"Event Name: {event['name']} ")
                events_list.append(f"Date: {event['dates']['start']['localDate']} ")
                events_list.append(f"Venue: {event['_embedded']['venues'][0]['name']} ")
                events_list.append(f"Location: {event['_embedded']['venues'][0]['city']['name']}, {event['_embedded']['venues'][0]['state']['name']}, {event['_embedded']['venues'][0]['country']['name']}")
                
        else:
            events_list.append(f"Error found for {artist_name} near you")
    else:
        events_list.append(f"No upcoming events for {artist_name} near you")
    
    print(events_list)
    return events_list

