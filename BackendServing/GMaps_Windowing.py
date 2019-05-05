# Imports
import numpy as np
import requests
import os


# Raster_Search_Area outputs the mapped/satellite images of an area to retrieve the images of a departing location and arriving destination. This is the first stage before even processing any image. This gets the images that will be processed.
## Parameters for Raster_Search_Area:
#origin: the beginning coordinates in a dictionary format
#dest: the  destinatino coordinates in a dictionary format
#location_name: determines a folder location name to output the mapped files to
#view: two different views for image output, 'map' and 'satellite'
def Raster_Search_Area(origin, dest, location_name, view, pair):
	# Current active API key  (change in urls if API subscription is different)
	API_KEY = "AIzaSyBFc4JbwRiSga0ELL0mI3k9yNVIlYpACQc"
		
	# URLs for the Google Static Maps API.
	# map_url = "https://maps.googleapis.com/maps/api/staticmap?key=AIzaSyDzhP-wAh1hJpqu2ZSuxuS-MU84SuVAWb4&center=%s,%s&zoom=16&scale=2&format=png&maptype=roadmap&style=element:geometry%7Ccolor:0x212121&style=element:labels%7Cvisibility:off&style=element:labels.icon%7Cvisibility:off&style=element:labels.text.fill%7Ccolor:0x757575&style=element:labels.text.stroke%7Ccolor:0x212121&style=feature:administrative%7Celement:geometry%7Ccolor:0x757575%7Cvisibility:off&style=feature:administrative.country%7Celement:labels.text.fill%7Ccolor:0x9e9e9e&style=feature:administrative.land_parcel%7Cvisibility:off&style=feature:administrative.locality%7Celement:labels.text.fill%7Ccolor:0xbdbdbd&style=feature:administrative.neighborhood%7Cvisibility:off&style=feature:poi%7Cvisibility:off&style=feature:poi%7Celement:labels.text.fill%7Ccolor:0x757575&style=feature:poi.park%7Celement:geometry%7Ccolor:0x181818&style=feature:poi.park%7Celement:labels.text.fill%7Ccolor:0x616161&style=feature:poi.park%7Celement:labels.text.stroke%7Ccolor:0x1b1b1b&style=feature:road%7Celement:geometry.fill%7Ccolor:0x2c2c2c&style=feature:road%7Celement:labels.icon%7Cvisibility:off&style=feature:road%7Celement:labels.text.fill%7Ccolor:0x8a8a8a&style=feature:road.arterial%7Celement:geometry%7Ccolor:0x373737&style=feature:road.highway%7Celement:geometry%7Ccolor:0x3c3c3c&style=feature:road.highway.controlled_access%7Celement:geometry%7Ccolor:0x4e4e4e&style=feature:road.local%7Celement:labels.text.fill%7Ccolor:0x616161&style=feature:transit%7Cvisibility:off&style=feature:transit%7Celement:labels.text.fill%7Ccolor:0x757575&style=feature:water%7Celement:geometry%7Ccolor:0x000000&style=feature:water%7Celement:labels.text.fill%7Ccolor:0x3d3d3d&size=200x200"
	map_url = "https://maps.googleapis.com/maps/api/staticmap?key=AIzaSyBFc4JbwRiSga0ELL0mI3k9yNVIlYpACQc&center=%s,%s"
	satellite_url = "https://maps.googleapis.com/maps/api/staticmap?center=%s,%s&zoom=16&size=200x200&scale=2&maptype=satellite&format=png&key=AIzaSyBFc4JbwRiSga0ELL0mI3k9yNVIlYpACQc"
			
	# Square search window size defines coordinate update step for raster.
	window = 0.0003
	steps = 20
				
	# Define lattitude and longitude positions for rastering.
	#print("Raster called and received:", type(origin), "and", origin)
	LONS = np.linspace(origin['lng'], dest['lng'], steps)
	LATS = np.linspace(origin['lat'], dest['lat'], steps)
	# print("LATS that RasterSearchArea received:", LATS)
	# print("LONG that RasterSearchArea received:", LONS)
	# Define raster-image folder directory path.
	image_folder = location_name + '/' + view + '/' + str(pair)
	# Make raster-image folder.
	if not os.path.exists(image_folder):
		os.makedirs(image_folder)
		print('Directory ', image_folder, ' created.')
	else:
		print('Directory ' , image_folder, ' already exists.')
			
	# Raster the search area by centering appropriate centering lon,lat earth coordinates in the request URLs.
	print('Collecting ', view, ' images from Google Maps.')
	for lon in LONS:
		for lat in LATS:
			# Modify API URLs to adjust window position.
			if view == 'map':
				url = map_url % (str(lon),str(lat)) + "&zoom=16&scale=2&format=png&maptype=roadmap&style=element:geometry%7Ccolor:0x212121&style=element:labels%7Cvisibility:off&style=element:labels.icon%7Cvisibility:off&style=element:labels.text.fill%7Ccolor:0x757575&style=element:labels.text.stroke%7Ccolor:0x212121&style=feature:administrative%7Celement:geometry%7Ccolor:0x757575%7Cvisibility:off&style=feature:administrative.country%7Celement:labels.text.fill%7Ccolor:0x9e9e9e&style=feature:administrative.land_parcel%7Cvisibility:off&style=feature:administrative.locality%7Celement:labels.text.fill%7Ccolor:0xbdbdbd&style=feature:administrative.neighborhood%7Cvisibility:off&style=feature:poi%7Cvisibility:off&style=feature:poi%7Celement:labels.text.fill%7Ccolor:0x757575&style=feature:poi.park%7Celement:geometry%7Ccolor:0x181818&style=feature:poi.park%7Celement:labels.text.fill%7Ccolor:0x616161&style=feature:poi.park%7Celement:labels.text.stroke%7Ccolor:0x1b1b1b&style=feature:road%7Celement:geometry.fill%7Ccolor:0x2c2c2c&style=feature:road%7Celement:labels.icon%7Cvisibility:off&style=feature:road%7Celement:labels.text.fill%7Ccolor:0x8a8a8a&style=feature:road.arterial%7Celement:geometry%7Ccolor:0x373737&style=feature:road.highway%7Celement:geometry%7Ccolor:0x3c3c3c&style=feature:road.highway.controlled_access%7Celement:geometry%7Ccolor:0x4e4e4e&style=feature:road.local%7Celement:labels.text.fill%7Ccolor:0x616161&style=feature:transit%7Cvisibility:off&style=feature:transit%7Celement:labels.text.fill%7Ccolor:0x757575&style=feature:water%7Celement:geometry%7Ccolor:0x000000&style=feature:water%7Celement:labels.text.fill%7Ccolor:0x3d3d3d&size=200x200"
			elif view == 'satellite':
				url = satellite_url % (str(lon), str(lat))
					
			else:
				print("Something went wrong")
				raise Exception('map_view is invalid: ', view)
					
			# Filename for image
			filename = image_folder + view + '_%s_%s.png' % (str(lon), str(lat))

			# Request and save Google Maps image.
			response = requests.get(url)
			open(filename, 'wb').write(response.content)