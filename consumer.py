import threading
from flask import Flask, request
import requests
import time
import logging


data_resource = []

num_threads = 5
app = Flask(__name__)


# HTTP endpoint for consuming data
@app.route('/consume', methods=['POST'])
def consume_data():

    data = request.get_json()["value"]
    print("Consumer received {} from producer".format(data))

    data_resource.append(data)
    return 'Data consumed successfully', 200


# Function that consumes data on a separate thread
def consume_data_from_resource():
    while True:

        if data_resource:

            data = data_resource.pop()
            print("Consumer sending {} back to producer".format(data))
            package = {"value": data}
            requests.post('http://127.0.0.1:5001/reconsume', json=package)
            time.sleep(1)



for _ in range(num_threads):
    thread = threading.Thread(target=consume_data_from_resource)
    thread.start()

print("Starting consumer")


log = logging.getLogger('werkzeug')
log.disabled = True
app.run(port=5000)