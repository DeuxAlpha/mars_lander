import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/v1/hello-world', methods=['GET'])
def api__hello_world():
    return flask.jsonify({'greeting': 'Hello World'})


app.run()
