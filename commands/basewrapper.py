from datetime import datetime
import random
import json
import configparser

#CFG_PATH = r"C:\Users\turbiv\PycharmProjects\DiscordBot\cfg\config.ini"
#CFG_PATH = r"D:\__GIT\DiscordBot\cfg\config.ini"
CFG_PATH = r"app/cfg/config.ini"

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

    def get_token(self, title, token):
        config = configparser.ConfigParser()
        config.read(CFG_PATH)
        return config[title][token]

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
