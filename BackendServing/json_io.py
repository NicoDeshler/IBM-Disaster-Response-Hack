#!flask/bin/python

import sys

from flask import Flask, render_template, request, redirect, Response
from flask_cors import CORS
import random, json

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


	if (request.method=='GET'):
		print("get called. Fetching data to serve to contained.html")
	
		return render_template('contained.html', requestCalled=previousReq, numOfPairs=glob.get("pairsFound"), coordinates=glob.get("stringedCoordinates"));
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
			for x in loaded:
				print("   New user-destination coordinates found:", x)
	## Can be put into a singular string or into an array, depending on whatever is easier to format to pass into first stage of pipeline---- finding realtime-satellite images of coordiantes before sending to IBM Visual Recognition classification of "extent of traffic"
		except ValueError as err:
			print("Something went terribly wrong. Likely no points were received.")
			print(err)

		## loaded_json will contain the user input that will be passed into first stage of pipeline after this point
		print("\nBefore processing")
#		print(parsed)
#		result = ''
#		for item in stringedCoordinates:
#			# loop over every row
#			result += str(item['make']) + '\n'
		print("POST call completed")
		res = glob.get("loaded_json")

# returne results after processing thorugh data points.
# Put through pipeline
		return "returned from json_io post"



if __name__ == '__main__':
	# run!
	app.run()
