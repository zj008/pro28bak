import pymysql
import logging
from configparser import ConfigParser

cf = ConfigParser()
cf.read("conf/base_conf")

class Sql():
    def __init__(self):
        self.db = pymysql.Connect(
            host=cf.get("mysql", "host"),
            port=int(cf.get("mysql", "port")),
            user=cf.get("mysql", "user"),
            password=cf.get("mysql", "pass"),
            database=cf.get("mysql", "db")
        )
        self.cursor = self.db.cursor()

    def close(self):
        self.cursor.close()
        self.db.close()

    def select(self, no, num):
        self.cursor.execute(f"select id, pub_time, result, alg{no}big, res{no} from lottery  order by id desc limit {num}")
        ret = self.cursor.fetchall()
        return ret

    def execute(self, sql):
        try:
            self.cursor.execute(sql)
            ret = self.cursor.fetchall()
            return ret, 0
        except Exception as e:
            logging.error(f"error when execute sql: {sql}, error is {e.__str__()}")
            return None, e