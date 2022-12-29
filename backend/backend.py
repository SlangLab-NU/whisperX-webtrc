from flask import Flask, request
from flask_cors import CORS
import aiortc
from typing import TypedDict
from pprint import pprint

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return "Hello"


class InitRequest(TypedDict):
    model: str
    temperature: float
    top_p: float
    chunk_size: int

#get param from the url
@app.route("/initmodel", methods=['POST'])
def hello_name():
    req_data: InitRequest = request.get_json(force=True)
    pprint(req_data)
    return req_data['model']


app.run()