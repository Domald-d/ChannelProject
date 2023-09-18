from mysql.connector import connect
from mysql.connector import Error
import config
import json

class DataManager:
    def __init__(self):
        self.status = None
        try:
            self.conn = connect(user=config.USER,
                                password=config.PASSWORD,
                                host=config.HOST,
                                database=config.DB,
                                auth_plugin=config.AUTH)
            if self.conn.is_connected():
                self.status = "Connected"
                print(self.status)
            else:
                self.status = "connection failed"
                print(self.status)
        except Error as error:
            self.status = str(error)

    def __str__(self):
        return f"DataManager Status: {self.status}"
    
    def execute_sql_function(self,function_name,parameters=None):
        returns =  []
        try:
            cursor = self.conn.cursor(prepared=True)
            if parameters:
                cursor.execute(function_name,parameters)
            else:
                cursor.execute(function_name)
            returns = cursor.fetchone()
            cursor.close()

        except Error as error:
            self.status = error
            returns.append(None)
        finally:
            return returns[0]
        
    def execute_sql_procedure(self,the_query,parameters=None):
        results = []
        try:
            cursor = self.conn.cursor(dictionary=True)
            if parameters:
                cursor.callproc(the_query,parameters)
            else:
                cursor.callproc(the_query)
            self.conn.commit()

        except Error as error:
            self.status = error
        finally:
            return results
        
    def BuaTilNotanda(self,Nafn,Nick,Title,lvl,runs,runsToday,timer):
        params = [Nafn,Nick,Title,lvl,runs,runsToday,timer]
        data = self.execute_sql_procedure('BuaTilNotanda',params)
        return json.dumps(data,indent=3,ensure_ascii=False)
    
    def uppfaeraNotanda(self,Nafn,Nick,Title,lvl,runs,runsToday,timer):
        params = [Nafn,Nick,Title,lvl,runs,runsToday,timer]
        data = self.execute_sql_procedure('uppfaeraNotanda',params)
        return json.dumps(data,indent=3,ensure_ascii=False)
    
    def UserExists(self,Nafn):
        params = [Nafn]
        data = self.execute_sql_procedure('UserExists',params)
        return json.dumps(data,indent=3,ensure_ascii=False)
    
    def GetUserByUsername(self,Nafn):
        params = [Nafn]
        data = self.execute_sql_procedure('GetUserByUsername',params)
        return json.dumps(data,indent=3,ensure_ascii=False)
    