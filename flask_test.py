from flask import Flask, request, jsonify
from flask_cors import CORS
from cal import *

app = Flask(__name__)
CORS(app)

cal = Calendar('user') 


@app.route('/sync_db', methods=['POST'])
def sync_db():
    # Receive the JSON data sent from JavaScript
    data = request.get_json()
    num_events = data['head']['num_events']
    # print('number of events - ', num_events)

    list_events = list(data['events'])
    for read_event in list_events:
        id = read_event['id']
        # first, make sure the id exists, add if not...
        if (cal.event_from_id(id) == None):
            print('not found, adding new event...')
            cal.add_event(Event(id))
        # sync important data:
        cal.set_name(id, read_event['name']) 
        cal.set_time(id, read_event['start_time'], read_event['end_time']) 
        cal.set_repeat(id, read_event['repeat'])
    
    cal.print_list_names()
    # Send back a JSON response
    return jsonify({
        'reversedMessage': "synced data!" 
    })
  
@app.route('/push_forward', methods=['POST'])
def push_forward():
    # Receive the JSON data sent from JavaScript
    data = request.get_json()
    event = data['head']
    cal.push_event(event['id'], event['start_time'])

    cal.print_list_names()

    # Send back a JSON response
    message = []
    for ev in cal.event_list:
        temp = {'id': ev.id, 'start_time': ev.tar_time_start}
        message.append(temp)

    return jsonify({
        'reversedMessage': message
    })

@app.route('/grab_analytics', methods=['POST'])
def grab_analytics():
    # Receive the JSON data sent from JavaScript
    data = request.get_json()
    print(data)

    test = [2,4,5,6,7,7]
    # Send back a JSON response
    return jsonify({
        'reversedMessage': "data analytics", 'pack': test
    })


@app.route('/report_low_perf', methods=['POST'])
def report_low_perf():
    # Receive the JSON data sent from JavaScript
    data = request.get_json()
    print(data)

    # Send back a JSON response
    return jsonify({
        'reversedMessage': "hi"
    })

@app.route('/set_priority', methods=['POST'])
def set_priority():
    # Receive the JSON data sent from JavaScript
    data = request.get_json()
    print(data)

    # Send back a JSON response
    return jsonify({
        'reversedMessage': "hi"
    })
 
@app.route('/set_transparancy', methods=['POST'])
def set_transparancy():
    # Receive the JSON data sent from JavaScript
    data = request.get_json()
    print(data)

    # Send back a JSON response
    return jsonify({
        'reversedMessage': "hi"
    })
   
@app.route('/set_mutability', methods=['POST'])
def set_mutability():
    # Receive the JSON data sent from JavaScript
    data = request.get_json()
    print(data)

    # Send back a JSON response
    return jsonify({
        'reversedMessage': "hi"
    })
 
if __name__ == '__main__':
    app.run(debug=True)