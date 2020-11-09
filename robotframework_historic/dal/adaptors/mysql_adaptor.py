import mysql.connector


class MySqlDb:
    def __init__(self, **conn_params):
        # connection arguments: https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
        self.conn_config = conn_params
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.conn_config)
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(e)

    def use_db(self, db_name):
        self.cursor.execute("USE %s;" % db_name)

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

    def commit_close(self):
        self.connection.commit()
        self.connection.close()
