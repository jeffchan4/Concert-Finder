import React, { useState, useEffect, useCallback } from 'react';

function App() {
    
  const [topArtists, setTopArtists] = useState([]);
  const [upcomingConcerts, setUpcomingConcerts] = useState([]);
  const [timeRange, setTimeRange] = useState('short_term');
  const [accessToken, setAccessToken] = useState(null);
  const [activeButton, setActiveButton] = useState('short_term'); // Initialize with the default button

  const  [findbuttonVisibility, setfindButtonVisibility] = useState({});
  
  const fetchTopArtists = useCallback(() => {
    // Fetch data from Flask endpoint for top artists
    fetch(`/get_top_artists?time=${timeRange}`)
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
  
          // Call concertFetch for each top artist
          data.items.forEach((artist) => {
            concertFetch(artist.name);
          });
        } else {
          console.error('Data.items is not an array:', data);
        }
      })
      .catch((error) => {
        console.error('Error fetching top artists:', error);
      });
  }, [timeRange]);
  
   
  // Fetch data from Flask endpoint for upcoming concerts
  const concertFetch = (artist) => {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
  
        // Send latitude and longitude to the Flask backend and fetch concerts
        fetch(`/get_concerts?time=${timeRange}&latitude=${latitude}&longitude=${longitude}&artist=${artist}`)
          .then((response) => {
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
            return response.json();
          })
          .then((data) => {
            // Update the state with the fetched concert data
            setUpcomingConcerts((prevData) => ({
              ...prevData,
              [artist]: data, // Store concert data for the artist using their name as the key
            }));
            console.log(upcomingConcerts);
          })
          .catch((error) => {
            console.error('Error fetching concerts:', error);
          });
      },
      (error) => {
        console.error('Error getting geolocation:', error);
      }
    );
  };
  

    
  
  useEffect(() => { //Fetch new access token
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
  const concertfinderButtonClick = (artistName) => {
    setfindButtonVisibility((prevVisibility) => ({
      ...prevVisibility,
      [artistName]: false, // Set the visibility to false when the button is clicked
    }));
  };
  


  return (
    <div className="App">
      <header>
      <h1>Spotify's Wrapped</h1>
      </header>
      <img className='spotifylogo' src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTyzMf_KIKpV3q-YB93kf-JMcgbqF5TIGhuow&usqp=CAU" alt="Spotify Logo"></img>
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
      
      {topArtists.length > 0  ? (
        <ol>
          {topArtists.map((artist, index) => {
            
            
            const renderEventUrl = (text) => {
              if (!text.includes(':')) {
                return text;
              }
              const [eventUrlText, eventUrlLink] = text.split(": ");
              
              
              return (
                <>
                  
                  <a href={eventUrlLink} target="_blank" rel="noopener noreferrer">
                    Find Tickets
                  </a>
                </>
              );
            };
            const split = (text) => {
              if (text) {
                const [first, second] = text.split(":");
                return second;
              }
              return null; // Or a default value, depending on your needs
            };
            return (
              <div>
                <li value={index+1} key={artist.id}>
                  <img
                    src={artist.images[0]['url']}
                    alt={artist.name}
                    style={{ width: '80px', height: '80px' }}
                  />
                  <br />
                  
                  <a className='artisturl' href={artist.external_urls.spotify} target="_blank" rel="noopener noreferrer" >
                    {artist.name}
                    
                  </a>
                  

                  {findbuttonVisibility[artist.name] !== false &&(
                  <div key={artist}>
                  {/* <button
                    className='find_concert'
                    onClick={() => {
                      concertFetch(artist.name);
                      concertfinderButtonClick(artist.name);
                    }}
                  >
                    Find Concerts
                  </button> */}
                  </div>
                  )}
                  <br/>
                  <br/>
                  
                  {upcomingConcerts[artist.name] && (
                  <div className='concert_details_container'>
                    <div className='concert_box'>
                    <p className='find_tickets'> {renderEventUrl(upcomingConcerts[artist.name][0])}</p>
                    <p className='tour_name'> {split(upcomingConcerts[artist.name][1])}</p>
                    <p className='tour_date'>{split(upcomingConcerts[artist.name][2])}</p>
                    <p className='tour_location' >{split(upcomingConcerts[artist.name][3])}{split(upcomingConcerts[artist.name][4])}</p>
                    </div>
                  </div>
                )}


        
                </li>
                <br/>
                <br/>
            
                
              </div>
            );
          })}
        </ol>
      ):(
        <p>Loading top artists...</p>
      )
      }
      


      
      <h2>Find Friends</h2>
      <button onClick={fetchSimilarUsers} disabled={isLoading}>
        {isLoading ? 'Finding..' : 'Start Searching'}
      </button>
      <ul>
        {Object.entries(data).map(([userString, artistList]) => {
          const [id, user_name] = userString.split(',');

          return (
            <li key={id}>
              <a
                href={`http://localhost:5000/reroute_user/${id}/${user_name}`}
                target="_blank"
              >
                <strong>{user_name}</strong>
              </a>{" "}
              also listens to {artistList.join(', ')}
            </li>
          );
        })}
      </ul>


    </div>
    
  );
      }
  export default App;
