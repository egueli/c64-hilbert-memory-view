#!/usr/bin/env python

import flask
import sqlite3
from flask import Flask
from flask import request

app = Flask(__name__)

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
    return flask.jsonify(**out)

@app.route("/trace")
def getTraceData():
    fromTime = int(request.args.get('from'))
    toTime = int(request.args.get('to')) + 1
    accCursor = conn.execute('SELECT type, address FROM accesses WHERE timestamp >= ? AND timestamp < ? ORDER BY timestamp ASC', (fromTime, toTime))
    accessesRaw = [{}, {}, {}]
    for row in accCursor.fetchall():
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

    out = { 'accesses': accesses }
    return flask.jsonify(**out)

if __name__ == "__main__":
    app.run()

