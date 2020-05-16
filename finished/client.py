from pathlib import Path

import cherrypy
import codecs
import json
import urllib.request
import urllib.parse
import requests
import re
import base64

import db
import scheduler
import visualizer

cherrypy.config.update({'server.socket_port': 8069})
cherrypy.engine.restart()

class Root(object):
    @cherrypy.expose
    def index(self):
        key_path = str(Path(__file__).resolve().parents[2]) + "\\key.txt" # up(up(up(__file__))) + "\\key.txt"
        API_key = (open(key_path, "r").read())
        #scheduler.plan_schedule(work_start_time=, work_end_time=, lunch_time=, lunch_duration=, load_time=, unload_time=, break_time=)
        db.init()
        contents_to_save = scheduler.plan_schedule(API_key, "08:00", "17:00", "12:00", 60, 15, 10, 10)
        visualizer.save_HTML(contents_to_save)
        header_file = codecs.open("./display.html","r")
        return header_file.read()

if __name__ == '__main__':
    #cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.quickstart(Root())
