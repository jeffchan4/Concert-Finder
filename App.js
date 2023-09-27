import React, { useState, useEffect } from 'react';

function App() {
  const loginToSpotify = () => {
    // Redirect to your Flask /login route
    window.location.href = 'http://localhost:5000/login';
  };

  const [topArtists, setTopArtists] = useState([]);

  useEffect((time) => {
    // Fetch data from Flask endpoint
    fetch(`/get_top_artists?time=${'long_term'}`)
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
  }, []);

  return (
    <div className="App">
      <button onClick={loginToSpotify}>refresh access token</button>
      <button>short-term</button>
      <button>medium-term</button>
      <button>long-term</button>


      <h2>Top Artists</h2>
      {topArtists.length > 0 ? (
        <ul>
          {topArtists.map((artist) => (
            <li key={artist.id}>
                <img src={artist.images[0]['url']} alt={artist.name} style={{ width: '60px', height: '60px' }} />
                <a href={artist.external_urls.spotify} target="_blank" rel="noopener noreferrer">
                {artist.name}
                </a>
              
            </li>
          ))}
        </ul>
      ) : (
        <p>Loading top artists...</p>
      )}
    </div>
  );
}

export default App;
