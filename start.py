#!/usr/bin/env python
import json
import os
import subprocess
import sys
import time


class Globals:
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[0;33m"
    BLUE = "\033[0;36m"
    NOCOLOR = "\033[0m"

    NETWORK_ADDRESS = '127.0.0.1'
                  #webapp,  Bob,   Smith
    FLASK_PORTS = ['8000', '8001', '8002']

    PROCESSES_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), '.running_processes')
    OPENED_PROCESSES = []


class Start:
    def __init__(self):
        print(Globals.YELLOW + 'Starting required python flask ports and webapp' + Globals.NOCOLOR)
        sys.stdout.flush()

    def setup_flask_environment(self):
        """
        Sets the flask environment variable
        """
        dir_path = os.path.dirname(os.path.realpath(__file__))
        os.environ["FLASK_APP"] = os.path.join(str(dir_path), 'node_server.py')
        current_env = os.environ.copy()
        return current_env

    def start_flask(self):
        """
        Starts the required ports using python flask
        """
        for counter, port in enumerate(Globals.FLASK_PORTS):
            flask_command = ['python', '-m', 'flask', 'run', '--port', str(port), '&']
            print('Executing flask port # ' + Globals.YELLOW + str(port) + Globals.NOCOLOR + ' with command: ' + Globals.YELLOW + ' '.join(flask_command) + Globals.NOCOLOR)
            sys.stdout.flush()
            self.execute_process(command=flask_command)
            print('Command ' + Globals.GREEN + 'complete' + Globals.NOCOLOR)
            if counter != 0:
                d_option = {
                    "node_address": "http://" + Globals.NETWORK_ADDRESS + ":" + port
                }
                curl_command = ["curl -X POST http://" + Globals.NETWORK_ADDRESS + ":" + Globals.FLASK_PORTS[0] + "/register_with -H 'Content-Type: application/json' -d '" + str(json.dumps(d_option)) + "'"]
                print('Executing curl command to register users ' + Globals.YELLOW + str(port) + Globals.NOCOLOR + ' with command: ' + Globals.YELLOW + ' '.join(curl_command) + Globals.NOCOLOR)
                sys.stdout.flush()
                self.execute_process(command=curl_command)
                print('Command ' + Globals.GREEN + 'complete' + Globals.NOCOLOR)

    def start_web_app(self):
        """
        Starts the web app by executing the python process
        """
        dir_path = os.path.dirname(os.path.realpath(__file__))
        run_app = os.path.join(dir_path, 'run_app.py')
        print('Starting webapp by executing ' + Globals.YELLOW + str(run_app) + Globals.NOCOLOR)
        sys.stdout.flush()
        self.execute_process(['python', str(run_app)])
        print('Command ' + Globals.GREEN + 'complete' + Globals.NOCOLOR)

    def execute_process(self, command):
        """
        Opens a subprocess to execute the command with updated env
        """
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        Globals.OPENED_PROCESSES.append(proc.pid)
        time.sleep(2)


def main():
    if os.path.exists(Globals.PROCESSES_FILE):
        print(Globals.RED + 'Unable to start application since it is already running. Execute ' + Globals.NOCOLOR +
              Globals.YELLOW + './stop.py' + Globals.NOCOLOR +
              Globals.RED + ' to stop all processes' + Globals.NOCOLOR)
        sys.stdout.flush()
        return 1

    start = Start()
    #updated_env = start.setup_flask_environment()
    start.start_flask()
    start.start_web_app()

    f = open(Globals.PROCESSES_FILE, "a")
    f.write(str(Globals.OPENED_PROCESSES))
    f.close()

    return 0


if __name__ == '__main__':
    exit_code = main()
    exit(exit_code)
