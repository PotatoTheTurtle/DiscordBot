from datetime import datetime
import mysql.connector
import mysql.connector.errorcode
import json
import os

class Base(object):
    def info_logger(self, message):
        print(f'[{datetime.today()} - INFO] {message}')

    def error_logger(self, message):
        raise Exception(f'[{datetime.today()} - **ERROR**] {message}')

    def warning_logger(self, message):
        print(f'[{datetime.today()} - *WARNING*] {message}')

    def jsondata(self, author, playlistlink):
        data = {f"{author}": {"name": f"{author}", "playlist_link": f"{playlistlink}"}}
        return data

    def get_config_vars(self, var):
        token = os.environ.get(var)
        return token

class Database(object):
    def write_suggestion(self, text: str):
        Base().info_logger("PREPARING SQL CONNECTION")
        serverip = Base().get_config_vars("D_IP")
        databasename = Base().get_config_vars("D_DATABASE")
        password = Base().get_config_vars("D_PASSWORD")
        uid = Base().get_config_vars("D_USERNAME")
        sql = mysql.connector.connect(host=serverip, database=databasename, user=uid, password=password)
        cursor = sql.cursor()

        #I really really really dont like mysql afther this.
        Base().info_logger("SQL - Write suggestion")
        sql_code = "INSERT INTO suggestion VALUES ('%s')" % text
        print(sql_code)
        try:
            cursor.execute(sql_code)
            sql.commit()
            Base().info_logger("SQL CONNECTION COMPLETE")

        except mysql.connector.Error as error:
            sql.rollback()  # rollback if any exception occured
            Base().info_logger("Failed inserting record into python_users table {}".format(error))

        finally:
            if sql.is_connected():
                cursor.close()
                sql.close()

    def get_player_data(self, player=None):
        Base().info_logger("PREPARING SQL CONNECTION")
        serverip = Base().get_config_vars("D_IP")
        databasename = Base().get_config_vars("D_DATABASE1")
        password = Base().get_config_vars("D_PASSWORD1")
        uid = Base().get_config_vars("D_USERNAME1")
        sql = mysql.connector.connect(host=serverip, database=databasename, user=uid, password=password)

        #I really really really dont like mysql afther this.
        Base().info_logger("SQL - Get playerdata")
        sql_code = "SELECT * FROM darkrp_player"
        cursor = sql.cursor()
        array = []
        print(sql_code)
        try:
            cursor.execute(sql_code)
            records = cursor.fetchall()

            array.append([records[0][0],records[0][1],records[0][2],records[0][3]])
            print(array)

            Base().info_logger("SQL CONNECTION COMPLETE")

        except mysql.connector.Error as error:
            sql.rollback()  # rollback if any exception occured
            Base().info_logger("Failed inserting record into python_users table {}".format(error))

        finally:
            if sql.is_connected():
                cursor.close()
                sql.close()
                return array


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
