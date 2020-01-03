import datetime
from flask import render_template, Flask, request, redirect, url_for
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
    print("start root function")
    request_json = request.get_json()

    if request.form and 'workout_description' in request.form:
        form_input = request.form['workout_description']
        print(f"Form input: {form_input}")
        store_message(form_input)
        return redirect(url_for('index'))

    if request.args and 'message' in request.args:
        message = request.args.get('message')
        store_message(message)
        return message
    elif request_json and 'message' in request_json:
        message = request_json['message']
        store_message(message)
        return message
    else:
        print("Displaying start page")
        training_sessions = [
            datetime.datetime(2020, 1, 1, 15, 00),
            datetime.datetime(2019, 1, 2, 15, 30),
            datetime.datetime(2019, 1, 5, 15, 30),
            datetime.datetime(2019, 1, 6, 15, 30),
            datetime.datetime(2020, 1, 1, 14, 30)]
        return render_template("index.html", training_sessions=training_sessions)

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

    @app.route('/', methods=['POST'])
    def index_post():
        return root(request)

    app.run('127.0.0.1', 8080, debug=True)