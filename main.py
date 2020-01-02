import datetime
from flask import render_template, Flask, request
from google.cloud import datastore

datastore_client = datastore.Client()
message_kind = 'bajs'

def root(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()

    if request.args and 'message' in request.args:
        message = request.args.get('message')
        store_message(message)
        return message
    elif request_json and 'message' in request_json:
        message = request_json['message']
        store_message(message)
        return message
    else:
        message = 'Pappa bajsar en zippad bajs!'
        store_message(message)
        return render_template("index.html")

def store_message(message):
    print(f'storing message: {message} to datastore with kind {message_kind}')
    entity = datastore.Entity(key=datastore_client.key(message_kind))
    entity.update({
        'timestamp': datetime.datetime.utcnow(),
        'message': message
    })

    datastore_client.put(entity)

if __name__ == "__main__":
    app = Flask(__name__)

    @app.route('/')
    def index():
        return root(request)

    app.run('127.0.0.1', 8080, debug=True)