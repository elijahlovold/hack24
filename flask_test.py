from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_cors import cross_origin
from cal import *

app = Flask(__name__)
CORS(app, origins="localhost")

cal = Calendar('user') 
cal.load_calendar()
# print(cal.event_from_id('id213').past_sessions[0])

@app.route('/sync_db', methods=['POST'])
@cross_origin()
def sync_db():
    # Receive the JSON data sent from JavaScript
    data = request.get_json()

    list_events = list(data['events'])
    for read_event in list_events:
        id = read_event['id']
        # first, make sure the id exists, add if not...
        if (cal.event_from_id(id) == None):
            print('not found, adding new event...')
            cal.add_event(Event(id))
        # sync important data:
        cal.set_name(id, read_event['name']) 
        cal.set_date(id, read_event['start_time'])
        cal.set_time(id, read_event['start_time'], read_event['end_time']) 
    #     cal.set_repeat(id, read_event['repeat'])
    
    cal.print_list_names()
    cal.save_calendar()
    # Send back a JSON response
    return jsonify({
        'reversedMessage': "synced data!" 
    })
  
@app.route('/push_forward', methods=['POST'])
@cross_origin()
def push_forward():
    # Receive the JSON data sent from JavaScript
    data = request.get_json()
    event = data['head']
    time = event['start_time'] + cal.event_from_id(event["id"]).tar_time_start
    cal.push_event(event['id'], time)

    cal.print_list_names()

    # Send back a JSON response
    message = []
    for ev in cal.event_list:
        hours = int(ev.tar_time_start)
        minutes = int((ev.tar_time_start - int(ev.tar_time_start))*60)
        time = date_time_to_iso(ev.date, hours, minutes)

        hours = int(ev.tar_time_end)
        minutes = int((ev.tar_time_end - int(ev.tar_time_end))*60)
        endtime = date_time_to_iso(ev.date, hours, minutes)
        temp = {'id': ev.id, 'start_time': time, 'end_time': endtime}
        message.append(temp)

    return jsonify({
        'reversedMessage': message
    })

@app.route('/get_analytics', methods=['POST'])
def get_analytics():
    # Receive the JSON data sent from JavaScript
    data = request.get_json()
    event = data['head']
    analytics = cal.get_analytics(event['id'])

    message = {'overall_performance': cal.get_overall_performance(event['id']), 'session_data': analytics}
    # Send back a JSON response
    return jsonify({
        'reversedMessage': message
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
    event = data['head']
    cal.set_priority(event['id'], event['priority'])

    # Send back a JSON response
    return jsonify({
        'reversedMessage': True
    })
 
@app.route('/set_transparancy', methods=['POST'])
def set_transparancy():
    # Receive the JSON data sent from JavaScript
    data = request.get_json()
    event = data['head']
    cal.set_priority(event['id'], event['transparancy'])


    # Send back a JSON response
    return jsonify({
        'reversedMessage': True
    })
   
@app.route('/set_mutability', methods=['POST'])
def set_mutability():
    # Receive the JSON data sent from JavaScript
    data = request.get_json()
    event = data['head']
    cal.set_priority(event['id'], event['mutability'])

    # Send back a JSON response
    return jsonify({
        'reversedMessage': True
    })
    
@app.route('/start_event', methods=['POST'])
def start_event():
    # Receive the JSON data sent from JavaScript
    data = request.get_json()
    event = data['head']
    cal.end_task(event['id'])

    # Send back a JSON response
    return jsonify({
        'reversedMessage': True
    })

@app.route('/stop_event', methods=['post'])
def stop_event():
    # receive the json data sent from javascript
    data = request.get_json()
    event = data['head']
    cal.end_task(event['id'])

    # send back a json response
    return jsonify({
        'reversedmessage': True
    })

@app.route('/plot_prod', methods=['post'])
def plot_prod():
    # receive the json data sent from javascript
    data = request.get_json()
    event = data['head']
    cal.plot_productivity_dist()

    # send back a json response
    return jsonify({
        'reversedmessage': True
    })

@app.route('/plot_event_stats', methods=['post'])
def plot_event_stats():
    # receive the json data sent from javascript
    data = request.get_json()
    event = data['head']
    cal.plot_event_data(event['id'])

    # send back a json response
    return jsonify({
        'reversedmessage': True
    })



if __name__ == '__main__':
    app.run(debug=True)