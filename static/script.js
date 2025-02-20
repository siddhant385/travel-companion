function sendLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;

                // document.getElementById("status").innerText = `Location: ${latitude}, ${longitude}`;

                // Send location data to Flask
                fetch('/location', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ latitude, longitude })
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Location sent successfully:', data);

                    if (data.city) {
                        document.getElementById("status").innerText += ` (City: ${data.city})`;
                    }

                    // Fetch relevant information from Flask
                    return fetch('/get-info');
                })
                .then(response => response.json())
                .then(infoData => {
                    console.log("Received Info:", infoData);

                    // Display information
                    document.getElementById("source").innerHTML = `source: weatherapi`;
                    document.getElementById("temperature").innerHTML = `temperature: ${infoData.weather.temperature} C`;
                    document.getElementById("description").innerHTML = `description: ${infoData.weather.description}`;
                    document.getElementById("humidity").innerHTML = `Humidity: ${infoData.weather.humidity}% moisture`;
                    document.getElementById("wind-speed").innerHTML = `wind-speed: ${infoData.weather.wind_speed} km/h`;
                    for (let i=0;i<3;i++){
                        console.log("news-article"+i)
                        document.getElementById("news-article"+i).innerHTML = `<h3>${infoData.traffic[i].title}</h3>
                    <p>${infoData.traffic[i].description}</p>
                    <a href="${infoData.traffic[i].url}" target="_blank">Click to read full article</a>`
                    console.log("news-article"+i)
                    }
                    document.getElementById('police').innerHTML = `
                    <h2>Police Station</h2>
                    <a href="${infoData.police_station}" target="_blank">Click here for police Station</a>`
                    document.getElementById('hospital').innerHTML = `
                    <h2>Hospital</h2>
                    <a href="${infoData.hospital}" target="_blank">Click here for Hospital</a>`         
                })
                .catch(error => console.error('Error fetching info:', error));
            },
            (error) => {
                console.error("Error getting location:", error);
            }
        );
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function findPoliceStation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;
            
            const googleMapsLink = `https://www.google.com/maps/search/police+station/@${lat},${lng},15z`;
            document.getElementById("police-link").innerHTML = `<a href="${googleMapsLink}" target="_blank">Nearest Police Station</a>`;
        }, () => {
            alert("Location access denied. Unable to find nearby police stations.");
        });
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}