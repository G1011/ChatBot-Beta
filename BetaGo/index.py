from flask import json
from flask import request
from flask import Flask


app = Flask(__name__)
@app.route('/index')
def chatbot():
	return "Welcome to Chatbot"
	


if __name__ == '__main__':
	app.run(debug = True)