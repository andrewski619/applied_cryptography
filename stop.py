#!/usr/bin/env python
import os
import sys


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


def main():
    if os.path.exists(Globals.PROCESSES_FILE):
        f = open(Globals.PROCESSES_FILE, "r")
        contents = f.read()
        processes = contents.strip('][').split(',')
        for process in processes:
            print(Globals.GREEN + 'Terminating ' + Globals.NOCOLOR + Globals.YELLOW + str(process) + Globals.NOCOLOR)
            sys.stdout.flush()
            os.system('taskkill /PID ' + str(process) + ' /T /F')
        f.close()

        os.remove(Globals.PROCESSES_FILE)

    print(Globals.GREEN + 'All processes terminated' + Globals.NOCOLOR)
    sys.stdout.flush()
    return 0


if __name__ == '__main__':
    exit_code = main()
    exit(exit_code)
