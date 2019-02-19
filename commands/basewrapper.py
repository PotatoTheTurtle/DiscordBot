from datetime import datetime
import random
import json

class Base(object):
    def info_logger(self, message):
        print(f"[{datetime.today()} - INFO] {message}")

    def error_logger(self, message):
        raise Exception(f"[{datetime.today()} - **ERROR**] {message}")

    def warning_logger(self, message):
        print(f"[{datetime.today()} - *WARNING*] {message}")

    def jsondata(self, author, playlistlink):
        data = {f"{author}": {"name": f"{author}", "playlist_link": f"{playlistlink}"}}
        return data

class Json(object):
    def json_load(self, json_file, char):
        jsonfile = open(json_file, char)
        jl = json.load(jsonfile)
        jsonfile.close()
        return jl

    def json_write(self, json_file, char, data_list):
        jsonfile = open(json_file, char)
        jsonfile.write(json.dumps(data_list, indent=4, sort_keys=True))
        jsonfile.close()
