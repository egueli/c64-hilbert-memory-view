#!/usr/bin/env python

import flask
import sqlite3
import json
from flask import Flask
from flask import request
from flask_profile import Profiler

profiler = False

app = Flask(__name__)
app.debug = profiler
Profiler(app)

conn = sqlite3.connect('donkey_kong.sqlite')


@app.route('/')
def home():
    print "root!"
    return app.send_static_file('index.html')


@app.route('/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(path)


@app.route("/info")
def get_trace_info():
    first = conn.execute('SELECT timestamp FROM accesses ORDER BY timestamp ASC LIMIT 1').fetchone()[0]
    last = conn.execute('SELECT timestamp FROM accesses ORDER BY timestamp DESC LIMIT 1').fetchone()[0]
    out = {
        'firstTimestamp': first,
        'lastTimestamp': last
    }
    if profiler:
        return "<html><body>" + json.dumps(out) + "</body></html>"
    else:
        return flask.jsonify(**out)


@app.route("/trace")
def get_trace_data():
    from_time = int(request.args.get('from'))
    to_time = int(request.args.get('to')) + 1
    accesses = get_accesses(from_time, to_time)
    memory_values = get_memory_values(from_time, to_time)

    out = {
        'accesses': accesses,
        'memoryValues': memory_values
    }
    if profiler:
        return "<html><body>" + json.dumps(out) + "</body></html>"
    else:
        return flask.jsonify(**out)


def get_accesses(from_time, to_time):
    acc_cursor = conn.execute('SELECT type, address FROM accesses WHERE timestamp >= ? AND timestamp < ?',
                              (from_time, to_time))
    accesses_raw = [{}, {}, {}]
    while True:
        fetched = acc_cursor.fetchmany(to_time - from_time)
        if not fetched:
            break
        for row in fetched:
            type_num, address = row
            accesses_raw[type_num][address] = True
    accesses = {
        'read': [],
        'write': [],
        'execute': []
    }
    for i in range(0, 3):
        access_type = ['read', 'write', 'execute'][i]
        accesses[access_type] = list(accesses_raw[i])
    return accesses


def get_memory_values(from_time, to_time):
    val_cursor = conn.execute(
        'SELECT timestamp, address, value FROM memory_values WHERE timestamp >= ? AND timestamp < ?',
        (from_time, to_time))
    memory_values_raw = {}
    for row in val_cursor.fetchall():
        timestamp, address, value = row
        if (address not in memory_values_raw) or (memory_values_raw[address]['timestamp'] < timestamp):
            memory_values_raw[address] = {
                'timestamp': timestamp,
                'value': value
            }

    memory_values = []
    for address, data in memory_values_raw.iteritems():

        memory_values.append({address: data['value']})
    return memory_values

if __name__ == "__main__":
    app.run()
