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

conn = sqlite3.connect('test.sqlite')

@app.route('/')
def home():
    print "root!"
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
  # send_static_file will guess the correct MIME type
  return app.send_static_file(path)


@app.route("/info")
def getTraceInfo():
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
def getTraceData():
    fromTime = int(request.args.get('from'))
    toTime = int(request.args.get('to')) + 1
    accesses = get_accesses(fromTime, toTime)

    out = {
        'accesses': accesses
    }
    if profiler:
        return "<html><body>" + json.dumps(out) + "</body></html>"
    else:
        return flask.jsonify(**out)


def get_accesses(fromTime, toTime):
    accCursor = conn.execute('SELECT type, address FROM accesses WHERE timestamp >= ? AND timestamp < ?',
                             (fromTime, toTime))
    accessesRaw = [{}, {}, {}]
    while True:
        fetched = accCursor.fetchmany(toTime - fromTime)
        if not fetched:
            break
        for row in fetched:
            typeNum, address = row
            accessesRaw[typeNum][address] = True
    accesses = {
        'read': [],
        'write': [],
        'execute': []
    }
    for i in range(0, 3):
        accessType = ['read', 'write', 'execute'][i]
        accesses[accessType] = list(accessesRaw[i])
    return accesses


if __name__ == "__main__":
    app.run()

