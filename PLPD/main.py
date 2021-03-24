import time
import requests
import zmq
import signal
import threading
from datetime import datetime, timedelta


class Checker():
    """
            street - string
            lot - int
            check_time - datetime

            THIS CLASS IS USED TO CHECK IF LOT WAS PAID FOR AFTER 15 min
    """
    def __init__(self, street, lot, check_time):
        self.street = street
        self.lot = lot
        self.check_time = check_time

    # Checks if it is time to check payment at specific parking lot
    def time_checker(self):
        # If it's not the time - sleep
        if (self.check_time - datetime.now()) > timedelta(seconds=0):
            time.sleep((self.check_time - datetime.now()).total_seconds())
            print("Awakening")
            # If it is time to check return True
            if self.check_time <= datetime.now():
                return True



    def check(self):
        print("Checking")
        # Get info about lot
        response = requests.get("http://127.0.0.1:5000" + f"/parking/{self.street}/lot_number/{self.lot}").json()
        # Check if it was paid for
        if response['is_paid'] == False:
            # Do smth
            print(f"Pidoras detected on site - {self.street}, lot - {self.lot}")
            return True
        else:
            # Do smth
            print(f"All good at site - {self.street}, lot - {self.lot}")
            return False

# List of Checker objects
processes = []

# NOTE!!!
# This function does not work if we update 2 parking lots at the same time
# (Set 2 parking lots 'is_occupied' from False to True and see what happends)
def observer():
        while True:
            # Check if processes has any objects
            if len(processes) > 0:
                if processes[0].time_checker():
                    # Check if lot was paid for
                    processes[0].check()
                    processes.pop(0)
                    print(processes)




def main():

        context = zmq.Context()
        # Set socket
        socket = context.socket(zmq.SUB)
        socket.connect('tcp://localhost:5555')
        # Subsctibe to parking-  title to filter information
        socket.setsockopt(zmq.SUBSCRIBE, b'parking-')
        # Dictionary where all info from PUB goes; Key - street, value - data
        cache = {}

        while True:
                # Receive topic and date
                topic = socket.recv()
                data = socket.recv_pyobj()
                # Get parking site street
                street = topic.decode("utf-8").split("parking-")[1]
                lot = 0
                # Check if we have specified street in cache
                if street in cache:
                        # Check if new data has changes
                        if cache[street] != data:

                                # Find parking lot where changes are
                                for i in range(len(data)):
                                        if data[i] != cache[street][i]:
                                                # Set lot
                                                lot = data[i]['id']

                                                # If "is_occupied" changes to True set timer
                                                # to check if it will be paid in 15 min
                                                if (cache[street][i]['is_occupied'] == False) and (
                                                        data[i]['is_occupied'] == True):
                                                        # Create new instanse of Cheker and append it to list
                                                        checker = Checker(street,lot,datetime.now() + timedelta(seconds=2))
                                                        processes.append(checker)

                                                        print(processes)
                        cache[street] = data
                else:
                        # Create new key-value pair and print
                        cache[street] = data
                        print(cache)

if __name__ == '__main__':

        signal.signal(signal.SIGINT, signal.SIG_DFL)
        main_thread = threading.Thread(target=main)
        observer_thread = threading.Thread(target=observer)

        main_thread.start()
        observer_thread.start()

