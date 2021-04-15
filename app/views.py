import datetime
import json
import random
import requests
from flask import render_template, flash, redirect, request, session

from app import app

# The node with which our application interacts, there can be multiple
# such nodes as well.
CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8000"
LOGGED_IN = False
UPDATE_IRS = None

posts = []


def fetch_posts():
    """
    Function to fetch the chain from a blockchain node, parse the
    data and store it locally.
    """
    get_chain_address = "{}/chain".format(CONNECTED_NODE_ADDRESS)
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        chain = json.loads(response.content)
        for block in chain["chain"]:
            for tx in block["transactions"]:
                tx["index"] = block["index"]
                tx["hash"] = block["previous_hash"]
                content.append(tx)

        global posts
        posts = sorted(content, key=lambda k: k['timestamp'],
                       reverse=True)


@app.route('/')
def index():
    fetch_posts()
    url = 'login.html'
    account_number = ''
    if LOGGED_IN is True:
        url = 'index.html'
        if CONNECTED_NODE_ADDRESS == 'http://127.0.0.1:8001':
            account_number = '1234'
        elif CONNECTED_NODE_ADDRESS == 'http://127.0.0.1:8002':
            account_number = '9876'

    remaining_amount = 0
    for post in posts:
        if 'remainingAmount' in post and post['remainingAmount'] is not None:
            remaining_amount = int(post['remainingAmount'])
            break

    return render_template(url,
                           title='IRS Stimulus Check',
                           posts=posts,
                           accountNumber=account_number,
                           node_address=CONNECTED_NODE_ADDRESS,
                           remainingAmount=remaining_amount,
                           readable_time=timestamp_to_string)


@app.route('/submit', methods=['POST'])
def submit_textarea():
    """
    Endpoint to create a new transaction via our application.
    """
    last_remaining_amount = 0
    for post in posts:
        if 'remainingAmount' in post and post['remainingAmount'] is not None:
            last_remaining_amount = post['remainingAmount']
            break

    transaction_message = request.form["transactionMessage"]
    transaction_amount = request.form["transactionAmount"]

    if transaction_amount == "" or last_remaining_amount == 0 or int(transaction_amount) > int(last_remaining_amount):
        flash("Unable to transfer that quantity. Enter valid input and retry")
        return redirect('/')

    new_remaining_amount = last_remaining_amount - int(transaction_amount)

    # Submit a transaction
    post_object = {
        'transactionAmount': transaction_amount,
        'transactionMessage': transaction_message,
    }
    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)
    requests.post(new_tx_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})

    # Submit a transaction for remaining amount
    remaining_post_object = {
        'remainingAmount': new_remaining_amount
    }
    new_tx_address = "{}/new_remaining_amount".format(CONNECTED_NODE_ADDRESS)
    requests.post(new_tx_address,
                  json=remaining_post_object,
                  headers={'Content-type': 'application/json'})

    return redirect('/')


@app.route('/refresh_remaining_amount', methods=['POST'])
def refresh_remaining_amount():
    """
    Endpoint to update remaining amount via our application.
    """
    global UPDATE_IRS
    x = datetime.datetime.today()
    if UPDATE_IRS is None:
        UPDATE_IRS = x.minute
    y = x.replace(day=x.day, hour=x.hour, minute=UPDATE_IRS, second=0, microsecond=0) + datetime.timedelta(minutes=2)
    delta_t = y - x
    secs = delta_t.total_seconds()

    if secs < 0 and UPDATE_IRS is not None:
        UPDATE_IRS = None
        last_remaining_amount = 0
        for post in posts:
            if 'remainingAmount' in post and post['remainingAmount'] is not None:
                last_remaining_amount = post['remainingAmount']
                break

        next_remaining_amount = random.randint(0, 1600)
        new_remaining_amount = last_remaining_amount + next_remaining_amount
        post_object = {
            'remainingAmount': new_remaining_amount
        }

        # Submit a transaction
        new_tx_address = "{}/new_remaining_amount".format(CONNECTED_NODE_ADDRESS)

        requests.post(new_tx_address,
                      json=post_object,
                      headers={'Content-type': 'application/json'})

    return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    """
    Endpoint to login to the blockchain application.
    """
    global CONNECTED_NODE_ADDRESS
    global LOGGED_IN
    username = request.form["username"]
    password = request.form["password"]

    if str(username).lower() == 'bob':
        CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8001"
        LOGGED_IN = True
    elif str(username).lower() == 'smith':
        CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8002"
        LOGGED_IN = True

    if CONNECTED_NODE_ADDRESS == "http://127.0.0.1:8000":
        LOGGED_IN = False
        flash("Incorrect username and password combination")
    return redirect('/')


@app.route('/logout', methods=['POST'])
def logout():
    """
    Endpoint to login to the blockchain application.
    """
    global CONNECTED_NODE_ADDRESS
    global LOGGED_IN

    LOGGED_IN = False
    CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8000"
    session.pop('_flashes', None)
    return redirect('/')


def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')
