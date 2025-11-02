document.addEventListener("DOMContentLoaded", () => {
    const parkingList = document.getElementById("parking-list");
    const availableSpotsElement = document.getElementById("available-spots");
    const totalSpotsElement = document.getElementById("total-spots");

    async function fetchTelemetry() {
        try {
            const response = await fetch("/api/telemetry");
            const data = await response.json();

            updateParkingDisplay(data);
        } catch (error) {
            console.error("Error fetching telemetry:", error);
        }
    }

    function updateParkingDisplay(data) {
        parkingList.innerHTML = ""; // Clear previous UI

        let totalSpots = 0;
        let totalAvailable = 0; 

        data.forEach(zone => {
            const vacant = parseInt(zone.vacant);
            const occupied = parseInt(zone.occupied);
            const total = vacant + occupied;

            totalSpots += total;
            totalAvailable += vacant;

            const spot = document.createElement("div");
            spot.className = `parking-spot ${vacant > 0 ? "available" : "full"}`;
            spot.innerHTML = `
                <span>${zone.client_name}</span>
                <p>${vacant} Open Spots</p>
                <a href="https://www.google.com/maps?q=${zone.latitude},${zone.longitude}" target="_blank">📍 Navigate</a>
            `;
            parkingList.appendChild(spot);
        });

        totalSpotsElement.textContent = totalSpots;
        availableSpotsElement.textContent = totalAvailable;
    }

    // Fetch telemetry initially and then every 5 seconds
    fetchTelemetry();
    setInterval(fetchTelemetry, 5000);
});
