
var apiKey = "AIzaSyBFc4JbwRiSga0ELL0mI3k9yNVIlYpACQc";

var map;
var drawingManager;
var placeIdArray = [];
var polylines = [];
var snappedCoordinates = [];

function initialize() {
    var mapOptions = {
        zoom: 17,
        center: {lat: 37.8716, lng: -122.2727}
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
        var path = poly.getPath();
        polylines.push(poly);
        placeIdArray = [];
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