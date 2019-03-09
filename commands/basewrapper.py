from datetime import datetime
import pyodbc
import json
import configparser
import os

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

    def get_config_vars(self, var):
        token = os.environ.get(var)
        return token

class Database(object):
    def __init__(self):
        serverip = Base().get_config_vars("D_IP")
        databasename = Base().get_config_vars("D_DATABASE")
        password = Base().get_config_vars("D_PASSWORD")
        uid = Base().get_config_vars("D_USERNAME")
        self.cnxn = pyodbc.connect('Driver={SQL Server};'
                                f'Server={serverip};'
                                f'Database={databasename};'
                                f'PWD={password};'
                                f'UID={uid};')

    def write_suggestion(self, text):
        sql_code = f'INSERT INTO `suggestion` (`suggestions`) VALUES ({Base.info_logger(text)});'
        self.cursor = self.cnxn.cursor()
        self.cursor.execute(sql_code)
        self.cursor.commit()
        self.cursor.close()
        self.cnxn.close()


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
