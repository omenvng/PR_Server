import threading
import requests
from random import randrange
import time
from flask import Flask, request
import logging


data_resource = [2, 1, 6, 9, 4, 2, 4, 8, 4, 1, 5, 7, 9, 5, 2, 3, 4, 6, 4, 7, 9, 5, 3, 2, 1, 6, 7, 5, 2, 54, 7, 8, 5, 3,
                 3, 65, 7, 6, 3, 4, 65, 34, 6, 6, 4576, 5, 325, 46, 2, 5, 765, 7, 52, 55, 54, 2, 5474, 65342, 654, 52,
                 35]


num_threads = 5

# Flask app for hosting the HTTP server
app = Flask(__name__)



@app.route('/reconsume', methods=['POST'])
def consume_data():

    data = request.get_json()["value"]

    print("Producer received {} from consumer".format(data))


    data_resource.append(data)

    return 'Data consumed successfully', 200


# Function that produces data on a separate thread
def produce_data():
    while True:
        if data_resource:

            data = data_resource.pop(randrange(len(data_resource)))

            print("Producer sent {} to consumer".format(data))

            package = {"value": data}

            requests.post('http://127.0.0.1:5000/consume', json=package)

            time.sleep(1)



for _ in range(num_threads):
    thread = threading.Thread(target=produce_data)
    thread.start()

print("Starting producer")


log = logging.getLogger('werkzeug')
log.disabled = True
app.run(port=5001)