function showLoader() {
    document.getElementById("loading-spinner").classList.remove("hidden"); 
    document.getElementById("main-content").classList.add("blur"); // Blur background only
}

// Remove blur when page reloads
window.addEventListener("load", function() {
    document.getElementById("main-content").classList.remove("blur");
});

document.getElementById("get-location-btn").addEventListener("click", function() {
    showLoader();
    fetchLocation();
});
document.querySelector("form").addEventListener("submit", function() {
    showLoader();
});



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

// Show loader when search form is submitted
// Show loader when search form is submitted
document.addEventListener("DOMContentLoaded", function() {
    document.querySelector("form").addEventListener("submit", function() {
        showLoader();
    });
});


