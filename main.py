import datetime
from flask import render_template, Flask, request, redirect, url_for, Blueprint
from google.cloud import datastore
datastore_client = datastore.Client()
message_kind = 'bajs'

is_running_in_cloud = True

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
        cloud_url = 'https://europe-west1-python-example-app.cloudfunctions.net/trainify'
        redirect_url = cloud_url if is_running_in_cloud else url_for('.index')
        return redirect(redirect_url)

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
        training_sessions = fetch_workouts(10)

        return render_template("index.html", training_sessions=training_sessions)

def store_message(message):
    print(f'storing message: {message} to datastore with kind {message_kind}')
    entity = datastore.Entity(key=datastore_client.key(message_kind))
    entity.update({
        'timestamp': datetime.datetime.utcnow(),
        'message': message
    })

    datastore_client.put(entity)

def fetch_workouts(limit):
    query = datastore_client.query(kind=message_kind)
    query.order = ['-timestamp']

    workouts = query.fetch(limit=limit)

    return workouts

if __name__ == "__main__":
    is_running_in_cloud = False

    app = Flask(__name__)

    @app.route('/')
    def index():
        return root(request)

    @app.route('/', methods=['POST'])
    def index_post():
        return root(request)

    app.run('127.0.0.1', 8080, debug=True)