from flask import Flask, Response, render_template
from flask_cors import CORS
from decretos import write_output, connection
from bson.json_util import dumps

app = Flask(__name__, static_url_path='')
cors = CORS(app, resources={r"/api/*": {"origins":"*"}})

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/v1/")

def api_root():
    write_output()
    db=connection()
    response=dumps(db.decretos.find())
    return Response(response=response, status=200, mimetype='application/json')
    if __name__=="__main__":
        app.run(debug=True)