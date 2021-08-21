import mysql.connector
class log_Structure:

    def __init__(self,_id,pwd,db=None,data=None):
        self.const = {"host":"localhost" , "user":_id ,"passwd":pwd, "database":db}
        self.data = data

        self.conn = mysql.connector.connect(host="localhost",user=_id,passwd=pwd)
        self.cursor = self.conn.cursor()
        if db == None:
            self.cursor.execute("create database if not exists testdb")
            self.conn.commit()
            self.cursor.execute("Use testdb")
        else:
            self.cursor.execute(f"create database if not exists {db}")
            self.conn.commit()
        self.close()

    def connect(self):
        self.conn = mysql.connector.connect( **self.const )
        self.cursor = self.conn.cursor()
    def close(self):
        self.cursor.close()
        self.conn.close()

    def Str_create(self,table,fields):
        stat = "CREATE TABLE if not exists "+table+" ("
        for i in fields:
            if i == fields[-1]:stat+= i+")"
            else:stat += i +","
        self.cursor.execute(stat)
        self.conn.commit()

    def Sql_saver(self,table,values):
        self.connect()
        stat = f"INSERT INTO {table} values("+ "%s,"*(len(values[0])-1) +"%s)"
        self.cursor.executemany(stat,values)
        self.conn.commit()
        self.close()


    def CREATE(self):
        gross = ["P_ID INTEGER(10) Primary Key","Item_Name varchar(255) UNIQUE",
        "Quantity INTEGER(6)","Price INTEGER(6)","Batch_No INTEGER(15)"]

        emp = ["user VARCHAR(255) PRIMARY KEY","pwd VARCHAR(255)","type VARCHAR(10)",
            "Name VARCHAR(255)","Address VARCHAR(255),"'City VARCHAR(55)',
            'State VARCHAR(55)','PIN VARCHAR(55)','Phone VARCHAR(15)',
            'Email VARCHAR(255)','DOB VARCHAR(255)',

            'authorized Integer(1)','felony Integer(1)','past Integer(1)',

            'Position VARCHAR(25)','Start VARCHAR(50)',
            'Pay VARCHAR(10)','shift CHAR(1)',
            'education TEXT','image MEDIUMBLOB','image_type varchar(5)']

        cust = ('ID VARCHAR(255) PRIMARY KEY','NAME VARCHAR(255)','passwd varchar(255)',
            'phone INTEGER(15)','email VARCHAR(255)','address VARCHAR(255)',
            'score INTEGER(15) DEFAULT "0"')

        self.connect()
        self.Str_create('Groceries',gross)
        self.Str_create('Utilities',gross)
        self.Str_create('Electronic',gross)

        self.Str_create('employee',emp)
        self.Str_create('customer',cust)
        self.close()

        if self.data:self.test_data()

    def test_data(self):
        try:
            import db_creater_testdata as df
        except ImportError:
            import source.db_creater_testdata as df

        try:
            self.Sql_saver("Groceries",df.gross)
        except Exception as e:
            print("From Groceries test data:   "+str(e))
        try:
            self.Sql_saver("Utilities",df.utl)
        except Exception as e:
            print("From Utilities test data:   "+str(e))
        try:
            self.Sql_saver("Electronic",df.elec)
        except Exception as e:
            print("From Electronic test data:  "+str(e))

