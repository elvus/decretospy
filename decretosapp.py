from flask import Flask, Response, render_template
from flask_cors import CORS

from decretos import decretos, write_output

app = Flask(__name__, static_url_path='')
cors = CORS(app, resources={r"/api/*": {"origins":"*"}})

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/1.0/")

def api_root():
    response=""
    try:
        with open('decretos.json', 'r') as f:
            response=f.read()
    except IOError:
        response=decretos()
        write_output()
    return Response(response=response, status=200, mimetype='application/json')

    if __name__=="__main__":
        app.run(debug=True)