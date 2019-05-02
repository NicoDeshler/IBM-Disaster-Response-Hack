/**
    Backend handler to that:
        1. Receives desired locations from user in coordinates
        2. Calls backend to find optimal route by POSTing json-stringified coordinates
        3. Collects quicket route from backend as a list of coordinates
        4. Colors backend-returned list of coordinates to display for user interface
**/
var apiKey = "AIzaSyBFc4JbwRiSga0ELL0mI3k9yNVIlYpACQc";

var map;
var drawingManager;
var placeIdArray = [];
var polylines = [];
var snappedCoordinates = [];
var selected = [];
var coordinatesStringified =''
var user = document.getElementById('userInfo');
var userLoc = '';
var userLocLat ='';
var userLocLong ='';

/*****************************/
// JS for UI

// Front page
var showBtn = document.getElementById("showOptions");
var closeBtn = document.getElementById("closeDialog");

// Inside Dialog
var dialog = document.getElementById("dialog");

/*****************************/

// Wait for mapRoute button on front... Waiting for coordinates from user
window.onload = function() {
	// Setup the button click for additional
	document.getElementById("mapRoute").onclick = function() {
	    // Get User location so they can locate themselves upon screen load
	    user = document.getElementById('userInfo');
            console.log("getting location");
            getLocation();
            console.log("get Location complete");

        // parse JSON data after they click map. Should be done already by polyline being completed
        if (coordinatesStringified=='') {
            alert("No points were chosen. To pick a destination from a starting point: \n     1. Double click to initialize a starting point. \n     2. You can continue to single click to add more destinations. \n     3. To finish your trip, double click again to end blue drawing.")
        }
		passJSON();
	};

    // Buttons to show and hide instructions windows
	document.getElementById("showOptions").onclick = function(ev) {
                    document.getElementById("dialog").showModal();
                  };

    document.getElementById("closeDialog").onclick = function(ev) {
         document.getElementById("dialog").close();
     };

}

// Get location of user using navigator
function getLocation() {
    if (navigator.geolocation) {
        // Attempting to get user's current location
        //console.log("Attempting to get current position");
        var timeoutVal = 10 * 1000 * 1000;

        navigator.geolocation.getCurrentPosition(
                                            showPosition,
                                            showError,
                                            { enableHighAccuracy: true, timeout: timeoutVal, maximumAge: 0 });
        //console.log("Completed getCurrentPosition.");
        } else {
            console.log("Geolocation not supported");
            user.innerHTML = "Geolocation is not supported by this browser.";
        }
}

// Helper function to getLocation() that displays Positions when returned asynchronously
function showPosition(position) {
    console.log("navigator getting current position from showPosition", position);
        user.innerHTML = "Latitude: " + position.coords.latitude +
                    "<br>Longitude: " + position.coords.longitude;
}

// Handle Error if any from getLocation()
function showError(error) {
  switch(error.code) {
    case error.PERMISSION_DENIED:
      user.innerHTML = "User denied the request for Geolocation."
      break;
    case error.POSITION_UNAVAILABLE:
      user.innerHTML = "Location information is unavailable."
      break;
    case error.TIMEOUT:
      user.innerHTML = "The request to get user location timed out."
      break;
    case error.UNKNOWN_ERROR:
      user.innerHTML = "An unknown error occurred."
      break;
  }
}


// Pass JSON coordinates collected from user-input when they selected destinations/locations on map
function passJSON() {
	// ajax the JSON to the server
	try {
        console.log("coordinatesStringified currently loaded", coordinatesStringified);

        // *** First parameter of url can be changed to POST to a different server url that runs python backend
        // POST coordinates to backend @ /receiver to process points
        // If runnning locally, open terminal to IBM-Disaster-Response-Hack folder and run following:
        // "python BackendServing/json_io.py"
        // This runs the json_io.py python file(inside BackendServing folder), which hosts a HTTP server at port http://127.0.0.1:5000/
        // Once running, you can open up http://127.0.0.1:5000/
        // If you look inside json_io, you can route to different pages(the identifier after '/')
        $.post('http://127.0.0.1:5000/receiver', coordinatesStringified, function(data){
            console.log("post called and returned data:", data);
            });

        console.log("completed JSON passing");
        // stop link reloading the page
        event.preventDefault();
    } catch (err) {
        console.log("Error found:", err);
        }
    }


function initialize() {
    // Sets center location of map to use user location if possible; otherwise base location @ Berkely, CA
    var cent = {lat: 37.8716, lng: -122.2727};
    if (userLocLat!= '' && userLocLat!='') {
        center = {lat:userLocLat, lng:userLocLat};
    }

    var mapOptions = {
            zoom: 17,
            // base location
            center: cent
        };
    map = new google.maps.Map(document.getElementById('map'), mapOptions);

    // Adds a Places search box. Searching for a place will center the map on that
    // location.
    map.controls[google.maps.ControlPosition.RIGHT_TOP].push(document.getElementById('bar'));
    var autocomplete = new google.maps.places.Autocomplete(document.getElementById('autoc'));

    autocomplete.bindTo('bounds', map);
    autocomplete.addListener('place_changed', function() {
        var place = autocomplete.getPlace();
        if (place.geometry.viewport) {
            map.fitBounds(place.geometry.viewport);
        } else {
            map.setCenter(place.geometry.location);
            map.setZoom(17);
        }
    });



    // Enables the polyline drawing control. Click on the map to start drawing a
    // polyline. Each click will add a new vertice. Double-click to stop drawing.
    drawingManager = new google.maps.drawing.DrawingManager({
    drawingMode: google.maps.drawing.OverlayType.POLYLINE,
    drawingControl: true,
    drawingControlOptions: {
        position: google.maps.ControlPosition.TOP_CENTER,
        drawingModes: [google.maps.drawing.OverlayType.POLYLINE]
        },
    polylineOptions: {
        strokeColor: '#0066ff',
        strokeWeight: 2
        }
    });
    drawingManager.setMap(map);

    // Snap-to-road when the polyline is completed.
    drawingManager.addListener('polylinecomplete', function(poly) {
        // path is an MVCArray that contains information about selected points returned from google maps api call
        // coords contains the important array of coordinates((lat, long) pairs) that the user wants to go to
        // stringedCoords converts the coordinates into a JSON string to pass to python backend
        var path = poly.getPath();
        var coords = path.getArray();
        var stringedCoords = JSON.stringify(coords);
        polylines.push(poly);
        placeIdArray = [];

        // Assigning global variables to maintain state to avoid mayn api calls for easier testing
        // NEED TO PASS PATH TO PYTHON TO PROCESSS!!!!
        // Here, "path" contains the selected points
        selected = poly;
        coordinatesStringified = stringedCoords;


        //console.log("User wants to go to the follow coordiantes:", stringedCoords);
        passJSON();

        console.log("passed post call");
        runSnapToRoad(path);
      });






    // Clear button. Click to remove all polylines.
    var clearBtn = document.getElementById("clear")
    clearBtn.addEventListener("click", function(ev) {
        for (var i = 0; i < polylines.length; ++i) {
            polylines[i].setMap(null);
        }
        polylines = [];
        ev.preventDefault();
        return false;
    });
    //End of Initialize
}

// Snap a user-created polyline to roads and draw the snapped path
function runSnapToRoad(path) {
  var pathValues = [];
  for (var i = 0; i < path.getLength(); i++) {
    pathValues.push(path.getAt(i).toUrlValue());
  }
  console.log("path here: ", path);

    // DATA HERE NEEDS TO SNAP FROM PYTHON BACKEND isntead of google roads api

  $.get('https://roads.googleapis.com/v1/snapToRoads', {
    interpolate: true,
    key: apiKey,
    path: pathValues.join('|')
  }, function(data) {
  // drawSnappedPolyline colors coordinates in "snappedCoordinates" yellow
  // snappedCoordinates are processed in processSnapToRoadResponse
  console.log("inside runSnapToRoad:", data);
    processSnapToRoadResponse(data);
    drawSnappedPolyline();
  });

}

// Store snapped polyline returned by the snap-to-road service.
function processSnapToRoadResponse(data) {
  snappedCoordinates = [];
  placeIdArray = [];
  console.log(data);
  for (var i = 0; i < data.snappedPoints.length; i++) {
    var latlng = new google.maps.LatLng(
        data.snappedPoints[i].location.latitude,
        data.snappedPoints[i].location.longitude);
    snappedCoordinates.push(latlng);
    placeIdArray.push(data.snappedPoints[i].placeId);
  }
}

// Draws the snapped polyline (after processing snap-to-road response).
function drawSnappedPolyline() {
  var snappedPolyline = new google.maps.Polyline({
    path: snappedCoordinates,
    strokeColor: 'white',
    strokeWeight: 3
  });

  snappedPolyline.setMap(map);
  polylines.push(snappedPolyline);
}

document.addEventListener('DOMContentLoaded', initialize, false);
// getting location of user on load breaks security violation. Getting location must be voluntary from user, hence map button.
getLocation();