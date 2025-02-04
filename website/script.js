document.addEventListener("DOMContentLoaded", () => {
    let totalSpots = 10;
    let availableSpots = 10;
    let parkingList = document.getElementById("parking-list");
    let availableSpotsElement = document.getElementById("available-spots");

   
    const parkingLocations = [
        { id: 1, lat: 37.7749, lng: -122.4194 }, 
        { id: 2, lat: 40.7128, lng: -74.0060 }, 
        { id: 3, lat: 34.0522, lng: -118.2437 }, 
        { id: 4, lat: 51.5074, lng: -0.1278 },   
        { id: 5, lat: 48.8566, lng: 2.3522 },  
    ]  

    function updateParkingDisplay() {
        parkingList.innerHTML = "";
        availableSpotsElement.textContent = availableSpots;

        for (let i = 0; i < availableSpots; i++) {
            let spot = document.createElement("div");
            spot.className = "parking-spot";
            spot.innerHTML = `
                <span>Parking Spot ${i + 1}</span>
                <a href="https://www.google.com/maps?q=${parkingLocations[i % parkingLocations.length].lat},${parkingLocations[i % parkingLocations.length].lng}" 
                   target="_blank">📍 View on Map</a>
            `;
            parkingList.appendChild(spot);
        }
    }

    setInterval(() => {
        let randomChange = Math.random() > 0.5 ? 1 : -1;
        availableSpots = Math.max(0, Math.min(totalSpots, availableSpots + randomChange));
        updateParkingDisplay();
    }, 5000);

    updateParkingDisplay();
});
document.addEventListener("DOMContentLoaded", () => {
    let parkingList = document.getElementById("parking-list");
    let availableSpotsElement = document.getElementById("available-spots");

    function updateParkingDisplay(availableSpots, totalSpots) {
        parkingList.innerHTML = "";
        availableSpotsElement.textContent = availableSpots;

        for (let i = 0; i < availableSpots; i++) {
            let spot = document.createElement("div");
            spot.className = "parking-spot";
            spot.innerHTML = `
                <span>🅿️ Spot ${i + 1}</span>
                <a href="https://www.google.com/maps?q=37.7749,-122.4194" target="_blank">📍 Navigate</a>
            `;
            parkingList.appendChild(spot);
        }
    }

    function fetchParkingData() {
        fetch("http://127.0.0.1:5000/get_parking_data")
            .then(response => response.json())
            .then(data => updateParkingDisplay(data.available_spots, data.total_spots))
            .catch(error => console.error("Error fetching data:", error));
    }

    setInterval(fetchParkingData, 5000);
    fetchParkingData();
});
