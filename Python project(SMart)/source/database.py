import mysql.connector
class my_db:
    temp_file = None
    def __init__(self,_id,pwd,db=None):
        self.const = {"host":"localhost" , "user":_id ,"passwd":pwd, "database":db}

    def connect(self):
        self.conn = mysql.connector.connect( **self.const )
        self.cursor = self.conn.cursor()
    def close(self):
        self.cursor.close()
        self.conn.close()

    def sql_create(self,table_name="NoName",fields=["sno integer(10)"]):
        stat = "CREATE TABLE if not exists "+table_name+" ("
        for i in fields:
            if i == fields[-1]:stat+= i+")"
            else:stat += i +","
        self.connect()
        self.cursor.execute(stat)
        self.conn.commit()
        self.close()

    def sql_showall(self,table_name="NoName"):
        self.connect()
        self.cursor.execute("select * from "+table_name)
        data = self.cursor.fetchall()
        self.close()
        return data


    def sql_saver(self,table_name="NoName",values=[245]):
        self.connect()
        stat = "INSERT INTO "+table_name+" values("+ "%s,"*(len(values)-1) +"%s)"
        self.cursor.execute(stat,values)
        self.conn.commit()
        self.close()
    def sql_saver_fields(self,table_name="NoName",fields=["sno"],values=[245]):
        self.connect()
        stat = "INSERT INTO "+table_name+"("
        field = ""
        for no,i in enumerate(fields):
            if i == fields[-1]:field += fields[no].split(" ")[0] +") "
            else:field += fields[no].split(" ")[0] + ","
        stat += field +"values(" + "%s,"*(len(fields)-1)+"%s)"
        self.cursor.execute(stat,values)
        self.conn.commit()
        self.close()

    def sql_search_one(self,table,field,_id,val):
        self.connect()
        self.cursor.execute(f"SELECT {field} from {table} WHERE {_id} = %s LIMIT 10",[val] )
        data = self.cursor.fetchall()
        self.close()
        return data
    def sql_search_few(self,table,field,_id,val):
        f = ",".join(field)
        if not val:return
        elif val.isnumeric():
            stat = f"SELECT {f} from {table} WHERE {_id} = {val} LIMIT 10"
        else:
            stat = f"SELECT {f} from {table} WHERE {_id} like '%{val}%' LIMIT 10"

        self.connect()
        self.cursor.execute( stat )
        data = self.cursor.fetchall()
        self.close()
        return data

    def sql_search_few_with_id_pwd(self,table,field,_id,val,_pwd,pas):
        self.connect()
        f = ",".join(field)
        self.cursor.execute(f"SELECT {f} from {table} WHERE {_id} = %s AND {_pwd} = %s",[val]+[pas] )
        data = self.cursor.fetchall()
        self.close()
        if data in ([],[[]],'',((),)):
            return False
        return {i:j for i,j in zip(field,data[0])}


    def sql_search(self,table_name="NoName",_id="1",val="test field"):
        if val.isnumeric():
            stat = f"Select * from {table_name} WHERE {_id} = '{val}'"
        else:
            stat = f"Select * from {table_name} WHERE {_id} like '%{val}%' LIMIT 25"

        self.connect()
        self.cursor.execute(stat)
        data = self.cursor.fetchall()
        self.close()
        return data

    def sql_update(self,table_name="NoName",val=["None"]):
        self.connect()
        self.cursor.execute("show columns from "+table_name)
        structure = [i[0] for i in self.cursor.fetchall()]
        stat = f"Update {table_name} SET "
        for i,v in enumerate(structure[1:]):
            stat += v + f" = '{val[i+1]}' ,"
        stat = stat[:-1] + f" Where {structure[0]} = {val[0]}"
        self.cursor.execute(stat)
        self.conn.commit()
        self.close()

    def sql_update_quantity(self,_id,_qty,dic):  # For billing reasons.
        self.connect()
        for i in dic:
            for key,v in dic[i].items():
                stat = f"UPDATE {i} SET "
                stat += _qty + f" = {_qty} - {v} WHERE {_id} = '{key}'"
                self.cursor.execute(stat)
        self.conn.commit()
        self.close()

    def sql_update_scores(self,table,_id,user,score):
        self.connect()
        self.cursor.execute(f"UPDATE {table} SET score = score + {score} WHERE {_id} = '{user}'")
        self.conn.commit()
        self.close()


    def sql_employee_data(self,table,dic):  # Specificly for employee
        self.connect()
        try:
            self.cursor.execute(f"INSERT into {table}(user,pwd,type) VALUES(%s,%s,%s)",dic["user"])
        except mysql.connector.errors.IntegrityError:
            self.close()
            if dic["user"][1] != "<Hiden>":return True
            # pwd = self.sql_search_few_with_id_pwd(table,["pwd","type"],"user",dic["user"][0],"pwd",dic["user"][1])
        else:
            self.conn.commit()
            self.close()
        finally:
            self.sql_employee_data_update(table,dic)

    def sql_employee_data_update(self,table,dic): # Specificly for employee
        self.connect()
        self.cursor.execute(f"""UPDATE {table} SET
            Name = %s,Address = %s,City = %s,State = %s,PIN = %s,Phone = %s,Email = %s,DOB = %s,
            authorized = %s,felony = %s,past = %s,
            Position = %s,Start = %s,Pay = %s,shift = %s
            WHERE user = '{dic['user'][0]}' """,dic["personal"]+dic['legal']+dic['position'])

        edu = ';'.join( [ ",".join(i) for i in dic["education"] ] )
        self.cursor.execute(f"""UPDATE {table} SET
            Education = %s
            WHERE user = '{dic['user'][0]}'""",[edu])
        self.conn.commit()
        self.close()
    def sql_employee_image_upload(self,table,user,file):
        self.connect()
        with open(file,"rb") as f:
            self.cursor.execute(f"""UPDATE {table} SET
                image = %s,
                image_type = %s
                WHERE user = '{user}' """,[f.read(), "."+file.split(".")[-1]  ])
        self.conn.commit()
        self.close()
    def sql_employee_image_download(self,table,user):
        self.connect()
        self.cursor.execute(f"""SELECT image,image_type FROM {table} WHERE user = '{user}' """)
        data = self.cursor.fetchone()
        self.close()
        if not data[0]:return None

        import os
        from PIL import Image,ImageTk
        os.remove(self.temp_file)
        self.temp_file = self.temp_file + data[1]
        with open(self.temp_file,"wb") as f:
            f.write(data[0])
        try:
            x = Image.open(self.temp_file);x.thumbnail((255,255))
            return ImageTk.PhotoImage( x )
        except Exception as e:
            raise e

    def sql_employee_data_load(self,table,user):
        data = dict()
        self.connect()
        self.cursor.execute(f"""SELECT type
            FROM {table} WHERE user = '{user}'""")
        data['user'] = (user,"<Hiden>",self.cursor.fetchone()[0])

        self.cursor.execute(f"""SELECT Name,Address,City,State,PIN,Phone,Email,DOB
            FROM {table} WHERE user = '{user}'""")
        data['personal'] = self.cursor.fetchone()
        self.cursor.execute(f"""SELECT authorized,felony,past
            FROM {table} WHERE user = '{user}'""")
        data['legal'] = self.cursor.fetchone()

        self.cursor.execute(f"""SELECT Position,Start,Pay,shift
            FROM {table} WHERE user = '{user}'""")
        data['position'] = self.cursor.fetchone()

        self.cursor.execute(f"""SELECT Education
            FROM {table} WHERE user = '{user}'""")
        data['education'] = [i.split(',') for i in self.cursor.fetchone()[0].split(";")]

        return data
