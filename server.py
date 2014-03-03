#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle, Jordan Ching
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# You can start this by executing it in python:
# python server.py
#
# remember to:
#     pip install flask


import flask
from flask import Flask, request
import json
import random
app = Flask(__name__)
app.debug = True

# An example world
# {
#    'a':{'x':1, 'y':2},
#    'b':{'x':2, 'y':3}
# }

class World:
    def __init__(self):
        self.clear()
        
    def update(self, entity, key, value):
        entry = self.space.get(entity,dict())
        entry[key] = value
        self.space[entity] = entry

    def set(self, entity, data):
        self.space[entity] = data

    def clear(self):
        self.space = dict()

    def get(self, entity):
        return self.space.get(entity,dict())
    
    def world(self):
        return self.space

# you can test your webservice from the commandline
# curl -v   -H "Content-Type: appication/json" -X PUT http://127.0.0.1:5000/entity/X -d '{"x":1,"y":1}' 

myWorld = World()
myCounter = 1;

# I give this to you, this is how you get the raw body/data portion of a post in flask
# this should come with flask but whatever, it's not my project.
def flask_post_json():
    '''Ah the joys of frameworks! They do so much work for you
       that they get in the way of sane operation!'''
    if (request.json != None):
        return request.json
    elif (request.data != None and request.data != ''):
        return json.loads(request.data)
    else:
        return json.loads(request.form.keys()[0])

@app.route("/")
def hello():
    return flask.redirect('/static/index.html')

@app.route("/entity/<entity>", methods=['POST','PUT'])
def update(entity):
    updateEntity = flask_post_json()
    for key in updateEntity:
        myWorld.update(entity, key, updateEntity[key])
    
    return flask.jsonify(myWorld.get(entity))

@app.route("/world", methods=['POST','GET'])
def world():
    if(request.method == 'POST'):
        entities = flask_post_json()
        print(entities)
        for i in entities:
            myWorld.set(str(random.randint(1,1000000)), entities[i])
    
    return flask.jsonify(myWorld.world())

@app.route("/seeTheWorld", methods=['GET'])
def seeTheWorld():
    html = "<!DOCTYPE html><head><title>World Representation</title></head><body>"
    html += "<h1>World Representation</h1>"
    html += "<table><thead><th>Name</th><th>X</th><th>Y</th><th>Colour</th></thead>"
    html += "<tbody>"
    entities = myWorld.world()
    for entity in entities:
        myEntity = entities[entity]
        html += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (entity, myEntity["x"], myEntity["y"], myEntity["colour"])
    
    html += "</tbody></table></body></html>"
    
    return html

@app.route("/entity/<entity>")    
def get_entity(entity):
    return flask.jsonify(myWorld.get(entity))

@app.route("/clear", methods=['POST','GET'])
def clear():
    myWorld.clear()
    return "World cleared."

if __name__ == "__main__":
    app.run()
