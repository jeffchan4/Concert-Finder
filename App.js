import React, { useState, useEffect, useCallback } from 'react';

function App() {
    
  const [topArtists, setTopArtists] = useState([]);
  const [upcomingConcerts, setUpcomingConcerts] = useState([]);
  const [timeRange, setTimeRange] = useState('short_term');
  const [accessToken, setAccessToken] = useState(null);
  const [activeButton, setActiveButton] = useState('short_term'); // Initialize with the default button

  const fetchTopArtists = useCallback(() => {
    // Fetch data from Flask endpoint for top artists
    const artistFetch = fetch(`/get_top_artists?time=${timeRange}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data) => {
        // Ensure that data.items is an array
        if (Array.isArray(data.items)) {
          // Update the state with the fetched data
          setTopArtists(data.items);
        } else {
          console.error('Data.items is not an array:', data);
        }
      })
      .catch((error) => {
        console.error('Error fetching top artists:', error);
      });

    // Fetch data from Flask endpoint for upcoming concerts
    const concertFetch = new Promise((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          console.log('Latitude:', position.coords.latitude);
          console.log('Longitude:', position.coords.longitude);
          const { latitude, longitude } = position.coords;

          // Send latitude and longitude to the Flask backend and fetch concerts
          fetch(`/get_concerts?time=${timeRange}&latitude=${latitude}&longitude=${longitude}`)
            .then((response) => {
              if (!response.ok) {
                throw new Error('Network response was not ok');
              }
              return response.json();
            })
            .then((data) => {
             
              // Update the state with the fetched concert data
              setUpcomingConcerts(data);
              
              resolve(); // Resolve the promise when concert data is fetched
            })
            .catch((error) => {
              console.error('Error fetching concerts:', error);
              reject(error); // Reject the promise if there's an error
            });
        },
        (error) => {
          console.error('Error getting geolocation:', error);
          reject(error); // Reject the promise if there's an error
        }
      );
    });

    // Wait for both artistFetch and concertFetch to complete
    Promise.all([artistFetch, concertFetch])
      .catch((error) => {
        // Handle any errors that occurred during the fetch
        console.error('Error in fetchTopArtists:', error);
      });
  }, [timeRange]);
  
  useEffect(() => {
    // Fetch the new access token from your Flask backend
    const fetchNewAccessToken = async () => {
      try {
        const response = await fetch('/refresh_token', {
          method: 'POST',
          // You may need to include headers or credentials depending on your server setup
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();

        // Assuming your server responds with the new access token
        const newAccessToken = data.access_token;
        console.log('successful fetch of access token')
        // Update the state with the new access token
        setAccessToken(newAccessToken);
      } catch (error) {
        console.error('Error refreshing access token:', error);
      }
    };

    // Call the function to refresh the token when the component mounts
    fetchNewAccessToken();
    const intervalId = setInterval(fetchNewAccessToken, 900000);

    // Clean up the interval when the component unmounts
    return () => clearInterval(intervalId);
  }, []);

  

  useEffect(() => {
    // Call fetchTopArtists when the component mounts
    fetchTopArtists();
    
  }, [fetchTopArtists]);
  
  useEffect(() => {
    // This effect runs whenever upcomingConcerts changes
    // You can put your logic here that depends on the updated upcomingConcerts state
    // For example, you can call a function or perform other actions.
    // Make sure to check for the conditions you need before proceeding.

    if (upcomingConcerts.length > 0) {
      
      // You can proceed with other functions here
      // This block will execute when upcomingConcerts has data
    }
  }, [upcomingConcerts]);

  const [data, setData] = useState({});
  const [isLoading, setIsLoading] = useState(false);

  const fetchSimilarUsers = () => {
    setIsLoading(true);

    // Make a fetch request to your Flask route to get the data
    fetch('/get_users_w_same_artists')
      .then((response) => response.json())
      .then((responseData) => {
        setData(responseData);
        setIsLoading(false);
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
        setIsLoading(false);
      });
  };
  const handleButtonClick = (button) => {
    setActiveButton(button);
    setTimeRange(button); // Set the time range when a button is clicked
  };

  


  return (
    <div className="App">
      <header>
      <h1>Spotify's Wrapped</h1>
      </header>
      <div className="buttonwrapper">
      <button
            className={activeButton === 'short_term' ? 'active' : ''}
            onClick={() => handleButtonClick('short_term')}
          >
            Short Term
          </button>
          <button
            className={activeButton === 'medium_term' ? 'active' : ''}
            onClick={() => handleButtonClick('medium_term')}
          >
            Medium Term
          </button>
          <button
            className={activeButton === 'long_term' ? 'active' : ''}
            onClick={() => handleButtonClick('long_term')}
          >
            Long Term
          </button>
        
      </div>
      <h2>Top Artists</h2>
      
      {topArtists.length > 0 && upcomingConcerts !== null && upcomingConcerts.length > 0 ?  (
        <ol>
          {topArtists.map((artist, index) => {
            const correspondingConcerts = upcomingConcerts[index];
            console.log(correspondingConcerts);
            const renderEventUrl = (text) => {
              const [eventUrlText, eventUrlLink] = text.split(": ");
              return (
                <>
                  {eventUrlText}:{' '}
                  <a href={eventUrlLink} target="_blank" rel="noopener noreferrer">
                    {eventUrlLink}
                  </a>
                </>
              );
            };
  
            const formattedConcerts = correspondingConcerts.map((item, index) => (
              <li  className='nostyleli' key={index}>
                {index === 0 ? renderEventUrl(item) : item}
                {index < correspondingConcerts.length - 1 && <br />}
              </li>
            ));
  
            return (
              <div>
                <li value={index+1} key={artist.id}>
                  <img
                    src={artist.images[0]['url']}
                    alt={artist.name}
                    style={{ width: '60px', height: '60px' }}
                  />
                  <a href={artist.external_urls.spotify} target="_blank" rel="noopener noreferrer">
                    {artist.name}
                  </a>
                  <div>
                    {formattedConcerts}
                  </div>
                </li>
            
                
              </div>
            );
          })}
        </ol>
      ) : (
        <p>Loading top artists...</p>
      )}
      {/* Data from Flask */}
      <h2>Find Friends</h2>
                <button onClick={fetchSimilarUsers } disabled={isLoading}>
                  {isLoading ? 'Fetching Data...' : 'Fetch Data'}
                </button>
                <ul>
                  {Object.keys(data).map((key) => (
                    <li key={key}>
                      <strong>{key}</strong> also listens to {data[key]}
                    </li>
                  ))}
                </ul>
    </div>
    
  );
      }
  export default App;
