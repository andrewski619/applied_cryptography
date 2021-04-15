# applied_cryptography

Utilizes Kansal blockchain example to spin up an application for Stimulus transfer.

## What is blockchain? How it is implemented? And how it works?

Please read the [step-by-step implementation tutorial](https://www.ibm.com/developerworks/cloud/library/cl-develop-blockchain-app-in-python/index.html) to get your answers :)

## Instructions to run

Clone the project (If using Windows, ensure you have GIT BASH installed),

```sh
$ git clone https://github.com/andrewski619/applied_cryptography.git
OR
$ git clone git@github.com:andrewski619/applied_cryptography.git
```

Install the dependencies,

```sh
# Open environment variables, and add python to environment variables
$ cd applied_cryptography
$ pip install -r requirements.txt
```

Start a blockchain node server,

```sh
# If running manually
$ export FLASK_APP=node_server.py
$ flask run --port 8000

# If starting application automatically 
$ python start.py

# Stop application and all opened python processes
$ python stop.py
```

One instance of our blockchain node is now up and running at port 8000
Port 8001 registered to 
	User: Bob
	Password: password1
Port 8002 registered to
	User: Smith
	Password: password2

Run the application on a different terminal session,

```sh
# If running manually, execute below
$ python run_app.py

# If starting application automatically, the start.py above will start web application
```

The application should be up and running at [http://localhost:5000](http://localhost:5000).
