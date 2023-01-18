import pyodbc

class SQLQuery:
    def __init__(self):
        # mssql
        self.server = 'BIQHI02VM'
        self.database = 'QC'
        self.username = 'QCTeam'
        self.password = 'Hidev20220801'

    def database_connect(self):
        print("start") 
        # driver = '{ODBC Driver 17 for SQL Server}' # for windows
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self.server+';PORT=1433;DATABASE='+self.database+';UID='+self.username+';PWD='+ self.password, autocommit=True)
        cursor = conn.cursor()
        return cursor

    def get_access_token(self, id):
        cursor = SQLQuery().database_connect()
        cursor.execute("exec sp_qc_QueryToken @MEMIDNO=" + id)
        rows = cursor.fetchone() 
        print("end")
        return rows[1]

    def get_order_number(self, id):
        cursor = SQLQuery().database_connect()
        cursor.execute("exec sp_qc_getOrderNo @MEMID=" + id)
        rows = cursor.fetchone() 
        print("end")
        print(rows)
        # return rows[1]

if __name__ == '__main__':
    test = SQLQuery()
    test.database_connect()
    test.get_order_number("A257635152")


    