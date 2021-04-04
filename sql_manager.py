import sqlite3
import time
import pandas as pd

class SqlManager:
    def __init__(self , file):
        self.conn = sqlite3.connect(file)
        self.crs = self.conn.cursor()

    def create_database(self):
        self.crs.execute("""CREATE TABLE IF NOT EXISTS transactions (
                                    tr_id VARCHAR(100) NOT NULL,
                                    description VARCHAR(200) NOT NULL);""")

        self.conn.commit()

    def excel_to_sql(self, fille_address):
        data = pd.read_csv(fille_address, header=None,sep=',')
        df = pd.DataFrame(data=data)
        sql_data = []
        for index, row in df.iterrows():
            row = row.dropna()
            for item in row:
                sql_data.append((index, item))
        query = "insert into transactions values (?,?)"
        try:
            self.crs.executemany(query, sql_data)
        except Exception as e:
            raise e
        self.conn.commit()
         
if __name__ == '__main__':
    start_time=time.time()
    sql_manager = SqlManager("information.sqlit3")
    sql_manager.create_database()
    sql_manager.excel_to_sql(fille_address=".\\Project1-groceries.csv")
    print("TIME=",time.time()-start_time)
