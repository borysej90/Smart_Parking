import signal
import zmq
import requests
import asyncio


signal.signal(signal.SIGINT, signal.SIG_DFL)
context = zmq.Context()
# Create SUB socket and connect it
socket = context.socket(zmq.SUB)
socket.connect('tcp://localhost:5555')
# Filter data
socket.setsockopt(zmq.SUBSCRIBE, b'parking-')

# Function that has to wait 15 min and then check if parking lot was paid for.
# BUT IT DOES NOT WORK. WHY? I DON'T KNOW, MB I AM AN IDIOT, MB NOT
async def find_paid(lot, street):

    await asyncio.sleep(10)
    # Advaned debugging technique
    print("Female dog")
    # Get info about parking lot
    response = requests.get("http://127.0.0.1:5000" + f"/parking/{street}/lot_number/{lot}").json()
    # Check if it was paid for
    if response['is_paid'] == False:
        print(f"Pidoras detected on site - {street}, lot - {lot}")
    else:
        print(f"All good at site - {street}, lot - {lot}")


async def main():

    cache = {}
    tasks = []
    while True:
        # Receive title from PUB
        topic = socket.recv()
        # Receive data from PUB
        data = socket.recv_pyobj()
        # Extract street name for further usage
        street = topic.decode("utf-8").split("parking-")[1]

        lot = 0
        # Check if we already have data about specified street
        if street in cache:
            #Check if new data has changes
            if cache[street] != data:
                #Find parking lot where changes are
                for i in range(len(data)):
                    if data[i] != cache[street][i]:
                        # Store lot id for further usage
                        lot = data[i]['id']

                        #If "is_occupied" changes to True set timer to check if it will be paid in 15 min
                        if (cache[street][i]['is_occupied'] == False) and (data[i]['is_occupied'] == True):
                            print("Checking")
                            # Call for async function THAT DOES NOT WORK
                            tasks.append(asyncio.create_task(find_paid(lot, street)))
                            await asyncio.gather(*tasks)

            cache[street] = data
        else:
            cache[street] = data
            print(cache)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()




