from flask import Flask
app = Flask(__name__)

@app.route("/")
def out1():
	return render_template("index.html", authors="All Our Names")

@app.route("/output")
def output():
	return render_template("index.html", name="All Our Names")

if __name__ == '__main__':
	# run!
	app.run()


