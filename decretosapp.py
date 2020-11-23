from flask import Flask, Response, render_template
from flask_cors import CORS
from bson.json_util import dumps
from requests.api import request

from decretos import connection, write_output
import urllib3

app = Flask(__name__, static_url_path='')
cors = CORS(app, resources={r"/api/*": {"origins":"*"}})

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/all")
def api_root():
    db=connection()
    response=dumps(db.decretos.find())
    return Response(response=response, status=200, mimetype='application/json')

@app.route("/api/<path:q>",methods=['GET', 'POST'])
def query(q):
    db=connection()
    print(q)
    response=dumps(db.decretos.find({
        "$or":[
                {'fecha': {'$regex': q}},
                {'descripcion': {'$regex': str(urllib3.util.parse_url(q)), "$options" :'i'}}
            ]
        })
    )
    return Response(response=response, status=200, mimetype='application/json')


if __name__=="__main__":
        app.run(debug=True)