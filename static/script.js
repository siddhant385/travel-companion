function sendLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;

                document.getElementById("status").innerText = `Location: ${latitude}, ${longitude}`;

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
                    document.getElementById("info").innerHTML = `
                        <strong>City:</strong> ${infoData.city} <br>
                        <strong>Traffic:</strong> ${infoData.traffic_news} <br>
                        <strong>Weather:</strong> ${infoData.weather}
                        <strong>AI Description:</strong> ${infoData.rate}
                    `;
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
