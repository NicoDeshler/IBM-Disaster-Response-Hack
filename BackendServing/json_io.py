#!flask/bin/python

import sys

from flask import Flask, render_template, request, redirect, Response
from flask_cors import CORS
import random, json

app = Flask(__name__)
cors = CORS(app)
received = " "
ty = " "
jsoniee = " "
boo = " "
stringedCoordinates = " "
daaattypee = " "
res = " "

@app.route('/main')
def output():
	# serve index template
	return render_template('./index.html',map="Get Directions!",
						                  authors="Justin Wong, Sam Wu, Billy Chau, Nico Deshler")

@app.route('/receiver', methods = ['GET','POST'])
def worker():
	##print("I received the following:", request.get_json())
	# read json + reply
	received = request
	ty = type(request)
	jsoniee = request.get_json()
	stringedCoordinates = request.get_data()
	parsed = str(stringedCoordinates)[2:len(str(stringedCoordinates))-1]
	print("parsed: ",parsed)
	loaded_json = json.loads(parsed)
	print("loaded:", loaded_json)
	for x in loaded_json:
		print("new coordinate found:", x)
	print()
	print()

	if (request.method=='GET'):
		print("get called")
		print(received)
		print(ty)
		print(jsoniee)
		print(boo)
		print(stringedCoordinates)
		print(daaattypee)
		return render_template('contained.html', a=jsoniee, b=daaat);
	if (request.method=='POST'):
		print("json parsed:")
		print("cnotent length:", request.content_length)
		print("cnotent type:", request.content_type)
		print("data:",request.get_data)
		print("md5", request.content_md5)
		gottenjson = request.get_json();
		print("gotten json:",gottenjson)
		print(gottenjson())
		print("json:",request.json)
		print()
		print(received)
		print(ty)
		print(jsoniee)
		print(boo)
		print()
		print("\nBefore processing")
		print(stringedCoordinates)
		print(daaattypee)
		result = ''
		for item in stringedCoordinates:
			# loop over every row
			result += str(item['make']) + '\n'
		print("post calleed")
		res = result
		return "returned from json_io post"



if __name__ == '__main__':
	# run!
	app.run()
