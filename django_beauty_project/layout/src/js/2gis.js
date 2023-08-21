// 2Gis API Homepage
var DG = require('2gis-maps');


DG.then(function() {
    const api_salons_url = '/api/salons/';

    var map,
        markers = DG.featureGroup(),
        markers_actions = DG.featureGroup(),
        markers_open_now = DG.featureGroup(),
        coordinates = [];

    map = DG.map('section-map__map', {
        'center': [55.754, 37.619],
        'zoom': 10,

        'dragging': true,
        'touchZoom': true,
        'scrollWheelZoom': true,
        'doubleClickZoom': true,
        'boxZoom': true,
        'geoclicker': true,
        'zoomControl': true,
        'fullscreenControl': false
    });

    // Add markers to map on page load
    fetch(api_salons_url)
        .then(response => response.json())
        .then(data => {
            for (let i = 0; i < data.length; i++) {
                /*
                coordinates[0] = data[i].latitude;
                coordinates[1] = data[i].longitude;

                // Add each Salon to markers
                DG.marker(coordinates).addTo(markers).bindPopup(data[i].name);

                // Add markers with actions
                if (data[i].has_actions === true) {
                    DG.marker(coordinates).addTo(markers_actions).bindPopup(data[i].name);
                }

                // Add markers for open now Salons
                if (data[i].working_schedule.open_now === true) {
                    DG.marker(coordinates).addTo(markers_open_now).bindPopup(data[i].name);
                }
                */

                data[i].addresses.forEach(el => {
                    // console.log(el);
                    coordinates[0] = el.latitude;
                    coordinates[1] = el.longitude;

                    // Add each Salon to markers
                    DG.marker(coordinates).addTo(markers).bindPopup(data[i].name);

                    // Add markers with actions
                    if (data[i].has_actions === true) {
                        DG.marker(coordinates).addTo(markers_actions).bindPopup(data[i].name);
                    }

                    // Add markers for open now Salons
                    if (el.working_schedule.open_now === true) {
                        DG.marker(coordinates).addTo(markers_open_now).bindPopup(data[i].name);
                    }
                });
            }
        })
        .catch(err => console.error(err))

    // Show all markers
    showMarkers();


    document.getElementById('hide').onclick = hideMarkers;

    document.getElementById('section-map__legend--show-all').onclick = showMarkers;
    document.getElementById('section-map__legend--show-actions').onclick = showActionsMarkers;
    document.getElementById('section-map__legend--show-opened').onclick = showOpenNowMarkers;

    function showMarkers() {
        hideMarkers();

        markers.addTo(map);
        // map.fitBounds(markers.getBounds());
    };

    function showActionsMarkers() {
        hideMarkers();

        markers_actions.addTo(map);
        map.fitBounds(markers_actions.getBounds());
    };

    function showOpenNowMarkers() {
        hideMarkers();

        console.log(markers_open_now);

        markers_open_now.addTo(map);
        map.fitBounds(markers_open_now.getBounds());
    }

    function hideMarkers() {
        markers.removeFrom(map);
        markers_actions.removeFrom(map);
        markers_open_now.removeFrom(map);
    };
});

/*
DG.then(function() {
    var map,
        markers = DG.featureGroup(),
        coordinates = [];

    map = DG.map('map', {
        center: [54.98, 82.89],
        zoom: 13
    });

    for (var i = 0; i < 100; i++) {
        coordinates[0] = 54.98 + Math.random();
        coordinates[1] = 82.89 + Math.random();
        DG.marker(coordinates).addTo(markers);
    }

    document.getElementById('hide').onclick = hideMarkers;
    document.getElementById('show').onclick = showMarkers;

    function showMarkers() {
        markers.addTo(map);
        map.fitBounds(markers.getBounds());
    };

    function hideMarkers() {
        markers.removeFrom(map);
    };
});
*/