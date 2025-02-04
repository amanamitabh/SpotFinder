document.addEventListener("DOMContentLoaded", () => {
    // Each parking zone has 5 spots
    let totalSpotsPerZone = 5;  
    let parkingZones = [
        { id: 1, name: "Parking Zone 1", available: 5, lat: 37.7749, lng: -122.4194 },
        { id: 2, name: "Parking Zone 2", available: 5, lat: 40.7128, lng: -74.0060 }
    ];

    let parkingList = document.getElementById("parking-list");
    let availableSpotsElement = document.getElementById("available-spots");

    // Function to update UI without changing zone names
    function updateParkingDisplay() {
        parkingList.innerHTML = ""; // Clear previous UI
        let totalAvailableSpots = parkingZones.reduce((sum, zone) => sum + zone.available, 0);
        availableSpotsElement.textContent = totalAvailableSpots; // Update total available spots count

        parkingZones.forEach((zone) => {
            let spot = document.createElement("div");
            spot.className = `parking-spot ${zone.available > 0 ? "available" : "full"}`;
            spot.innerHTML = `
                <span>${zone.name}</span>
                <p>${zone.available} Open Spots</p>
                <a href="https://www.google.com/maps?q=${zone.lat},${zone.lng}" target="_blank">📍 Navigate</a>
            `;
            parkingList.appendChild(spot);
        });
    }

    // Simulate parking changes while keeping zones fixed
    function simulateParkingChanges() {
        parkingZones.forEach((zone) => {
            let randomChange = Math.random() > 0.5 ? 1 : -1;
            zone.available = Math.max(0, Math.min(totalSpotsPerZone, zone.available + randomChange));
        });

        updateParkingDisplay();
    }

    // Update every 5 seconds
    setInterval(simulateParkingChanges, 5000);
    updateParkingDisplay();
});
