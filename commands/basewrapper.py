from datetime import datetime
import mysql.connector
import json
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

    def get_config_vars(self, var):
        token = os.environ.get(var)
        return token

class Database(object):
    def __init__(self):
        Base().info_logger("PREPARING SQL CONNECTION")
        serverip = Base().get_config_vars("D_IP")
        databasename = Base().get_config_vars("D_DATABASE")
        password = Base().get_config_vars("D_PASSWORD")
        uid = Base().get_config_vars("D_USERNAME")
        self.sql = mysql.connector.connect(host=serverip, database=databasename, user=uid, password=password)

    def write_suggestion(self, text):
        Base().info_logger("SQL - Write suggestion")
        sql_code = f'INSERT INTO `suggestion` (`suggestions`) VALUES ({Base.info_logger(text)});'
        try:
            self.cursor = self.sql.cursor()
            self.cursor.execute(sql_code)
            self.cursor.commit()

        except mysql.connector.Error as error:
            self.sql.rollback()  # rollback if any exception occured
            Base().info_logger("Failed inserting record into python_users table {}".format(error))

        finally:
            if self.sql.is_connected():
                self.cursor.close()
                self.sql.close()
                Base().info_logger("SQL CONNECTION COMPLETE")


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
