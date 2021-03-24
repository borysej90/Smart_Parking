import signal
import time
import zmq

signal.signal(signal.SIGINT, signal.SIG_DFL)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind('tcp://*:5555')
"""
    USAGE!!!
    RUN main.py first (city_api has to be launched ofc)
    RUN testPUB.py
    CHANGE 'is_occupied' on lot with id 3 to True 
    RUN testPUB.py
    CHANGE 'is_occupied' on lot with id 2 to True as fast as you can
    RUN testPUB.py
"""
data = [
        {'id':1,'is_occupied':True},
        {'id':2,'is_occupied':True},
        {'id':3,'is_occupied':True},
        {'id':4,'is_occupied':True},
        {'id':5,'is_occupied':True},
]
for i in range(2):
    socket.send(b'parking-Yeet_Prospect',flags = zmq.SNDMORE)
    socket.send_pyobj(data)
    time.sleep(1)

