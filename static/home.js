function fetchLocation() {
    navigator.geolocation.getCurrentPosition(position => {
        let latitude = position.coords.latitude;
        let longitude = position.coords.longitude;

        fetch('/location', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ latitude, longitude })
        })
        .then(response => response.json())

        // Redirect to Flask route with query parameters
        window.location.href = `/get_info`;
    });
}