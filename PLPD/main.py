import time
import requests
import zmq
import signal
import threading
from datetime import datetime, timedelta


class PaymentDetector():
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
    def sleeper(self):
        # If it's not the time - sleep
        if (self.check_time - datetime.now()) > timedelta(seconds=0):
            time.sleep((self.check_time - datetime.now()).total_seconds())



    def check(self):
        # Get info about lot
        response = requests.get("http://127.0.0.1:5000" + f"/parking/{self.street}/lot_number/{self.lot}").json()
        # Check if it was paid for
        # Note: If 'lot_number' was not found you will get error
        if not response['is_paid']:
            # Do smth
            print(f"Site - {self.street}, lot - {self.lot} was not paid for")
        else:
            # Do smth
            print(f"All good at site - {self.street}, lot - {self.lot}")

# List of Checker objects
processes = []

# If we have any lots in 'processes' this function will
def observer():
        while True:
            # Check if processes has any objects
            if len(processes) > 0:
                processes[0].sleeper()
                # Check if lot was paid for
                processes[0].check()
                processes.pop(0)





def main():

        context = zmq.Context()
        # Set socket
        socket = context.socket(zmq.SUB)
        socket.connect('tcp://localhost:5556')
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
                                                        checker = PaymentDetector(street,lot,datetime.now() + timedelta(minutes=15))
                                                        processes.append(checker)


                        cache[street] = data
                else:
                        # Create new key-value pair and print
                        cache[street] = data

if __name__ == '__main__':

        signal.signal(signal.SIGINT, signal.SIG_DFL)
        main_thread = threading.Thread(target=main)
        observer_thread = threading.Thread(target=observer)

        main_thread.start()
        observer_thread.start()

