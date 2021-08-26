// initializing home location
var mymap = L.map('mapid').setView([38.00089003740244, -121.287269144516], 4);

// rendering map
L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'TOKEN'
}).addTo(mymap);

// adding marker for home location
var marker = L.marker([38.00089003740244, -121.287269144516]).addTo(mymap)
    .bindPopup('Home Location')
    .openPopup();
marker._icon.classList.add("huechange");

// initializing dictionary for caching
var dict = {}

// processing the csv file every 10 seconds
setInterval(function() {
    $.ajax({
        type: "GET",
        url: "static/data.json",
        dataType: "json",
        success: function(data) {
            processData(data);
        }
    });
}, 10000);

// method to process json data saved in csv file
function processData(fleetData) {
    for (i = 1; i < fleetData.length; i++) {
        vehicle_location = fleetData[i];

        id = vehicle_location["id"];
        name = vehicle_location["name"];
        latitude = vehicle_location["latitude"];
        longitude = vehicle_location["longitude"];

        // saving markers in a dictionary
        if (!(id in dict)) {
            marker = L.marker([latitude, longitude]);
            marker.addTo(mymap).bindPopup(name);
            dict[id] = marker;
        } else {
            marker = dict[id];
            current_location = marker._latlng;

            // removing previous marker and adding new marker if the location changes
            if (current_location.lat != latitude || current_location.lng != longitude) {
                mymap.removeLayer(marker);
                newMarker = L.marker([latitude, longitude]);
                newMarker.addTo(mymap).bindPopup(name);
                dict[id] = newMarker;
            }
        }
    }
}