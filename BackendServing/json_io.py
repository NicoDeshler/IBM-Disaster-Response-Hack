#!flask/bin/python

import sys

from flask import Flask, render_template, request, redirect, Response
from flask_cors import CORS
import random, json
import GMaps_Windowing as gmap

app = Flask(__name__)
cors = CORS(app)
## Because of the use of global variables to pass data between retrieve and main, this solution is not scaleable. If there were multiple  instances of retriever open, there would potentially be data races which are no good.
latestRequest = " "    	 	## The latest GET/POST request called from any route
ty = " "					## The corresponding type of the latest Request
stringedCoordinates = " "	## User's desired destination(s) put into a string format. This is not json formated, only a string
res = " "					## result to pass around through pipeline
loaded_json = []			## User;s desired destinations put into json array format
pairsFound = 0;				## number of pairs of coordinates, denoting the location(s) the user wants to to. Also the length of the loaded_json array


@app.route('/main')
def output():
	# serve index template
	return render_template('./index.html',map="Get Directions!",
						                  authors="Justin Wong, Sam Wu, Billy Chau, Nico Deshler")


## Creates  a new route that runs worker, which handles GET and POST calls from /receiver
## worker fetches user coordinates which 
## represent all the locations(in coordinate form of (lat,long) that the user wants to go to.
## minimum requirement: 2 coordinates, a starting point and destination. 
## Could have multiple locations before arriving to final destination
@app.route('/receiver', methods = ['GET','POST'])
def worker():
	# read json + reply
	## Gets access to global variables to switch between get and post calls
	glob = globals()
	previousReq = glob.get("latestRequest")
	glob["latestRequest"] = request
	ty = type(request)
	print()
	print()
	print()
	print("NEW RECEIVER CALL HERE")
	print(latestRequest, " of type",  ty)
#	print("\nGLOBAL VARIABLES FOUND", glob)

	## Handle GET calls
	if (request.method=='GET'):
		print("GET called. Fetching data to serve to contained.html")
	
		return render_template('contained.html', requestCalled=previousReq, numOfPairs=glob.get("pairsFound"), coordinates=glob.get("stringedCoordinates"));
	
	## Handle POST calls
	if (request.method=='POST'):
		#	On /retriever POST call(when /retriever is called from browser),
		#	render a new page that spits out the received coordinates from a previous /main load
		## Updates global variables so that any GET request to /receiver will be able to receive the most recent call
		print("POST called. Posting data to for parsing and processing")
		glob["stringedCoordinates"] = request.get_data()
		stringy = glob.get("stringedCoordinates")
		parsed = str(stringy)[2:len(str(stringy))-1]
		print("Parsed through the request and received: \n",parsed)
		try:
			## JSON-Parse through the String parsed to find number of coordinates received from user
			## This corresponds to the different locations the user wants to go to
			## pairsFound denotes the number of  destinations received from user
			glob["loaded_json"] = json.loads(parsed)
			loaded = glob.get("loaded_json")
			glob["pairsFound"] = len(loaded)
			print("After loading json, Found ", glob.get("pairsFound"), " pairs from parsing json:", loaded)

			## loaded_json will contain the user input that will be passed into first stage of pipeline after this point
			## Can be put into a singular string or into an array, depending on whatever is easier to format to pass into first stage of pipeline
			## PIPELINE STAGE 1a: finding realtime-satellite images of coordiantes before sending to IBM Visual Recognition classification of "extent of traffic"
			print("\nBefore processing received coordinates")

			## Store map/satellite images into directory for image-processing retrieval
			## places images received into new directory called "serverWrite".
			##//TODO HERE: needs to be tested to see if len() can be called on loaded
			location_name = 'serverWrite'
			print("hardcoded completed")
			for i in range(0, len(loaded) - 1):
				print("   New user-destination coordinates found:", loaded[i])
				print("             Rastering Search Area and storing to new directory: " + location_name)
				gmap.Raster_Search_Area(loaded[i], loaded[i+1], location_name, 'map', i)
				gmap.Raster_Search_Area(loaded[i], loaded[i+1], location_name, 'satellite', i)
			for x in loaded:
				print("   New user-destination coordinates found:", x)


	
		except ValueError as err:
			print("Something went terribly wrong. Likely no points were received.")
			print(err)

		
		print("POST call completed")
		res = glob.get("loaded_json")

# returne results after processing thorugh data points.
# Put through pipeline
		return "returned from json_io post"



if __name__ == '__main__':
	# run!
	app.run()
