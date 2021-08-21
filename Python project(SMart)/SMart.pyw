import sys,io,os,tempfile,pickle
from tkinter import Tk,LabelFrame,Canvas
from tkinter import messagebox as mb
from cryptography.fernet import Fernet


# ______ My modules ______
from source import login
from source import menu
from source import stock
from source import customer
from source import employee
from source import bill
from source.config import Configure_db
from source.Utility import Bluebox,BG_change,Logger,key
from source.database import *   # * to get error classes from mysql.connector

Log = Logger("Error_Log.err")
sys.stdout = sys.stderr = Log  # Changing standard output and error

from source.icon import*    # * to run the program


# ________________________ Loading Resources __________________________
with open("resources.pkl","rb") as f:
    pickle.load(f)
    image = pickle.load(f)
with tempfile.NamedTemporaryFile(delete=False) as temp1:
    temp1.write(image["tool"])
with tempfile.NamedTemporaryFile(delete=False) as temp2:
    temp2.write(image["icon"])
with tempfile.NamedTemporaryFile(delete=False) as temp3:
    pass
os.rename(temp1.name, temp1.name+".ico");temp1.name = temp1.name+".ico"
os.rename(temp2.name, temp2.name+".ico");temp2.name = temp2.name+".ico"
image = {i:io.BytesIO(j) for i,j in image.items() }

root = Tk() # Tk initiated
root.iconify()
root.iconbitmap(temp2.name)
root.title("SMart - Work Smart")

# ________________ Exit Function ______________
def quit_func(force=False):    # Prompt for quitting
    root.iconify()
    text = "( If you encountered any problem please\nconsider reporting it to devloper )"
    ch = mb.askyesno("SMart - Work Smart","Are you sure you want to quit?",
        master=root,detail=text) if not force else 1
    #-default, -detail, -icon, -message, -parent, -title, or -type
    if ch in (True,"yes",1):
        try: sql_obj.close();  os.remove(sql_obj.temp_file)
        except (NameError,AttributeError):os.remove(temp3.name)
        root.destroy()
        os.remove(temp1.name);os.remove(temp2.name)
        Log.remove_if_blank()
        sys.exit(0)
    else:
        root.deiconify()

root.protocol("WM_DELETE_WINDOW",quit_func) # when you click "X"


# _______________ CONFIGURE _______________
Config = Configure_db(root,file_name="Configure.cfg",deicon=False)
# try:
Config(ico=temp1.name,img=image['tools'])

root.wait_window(Config.base)   # Waiting for configuration to end

with open(Config.file,"rb") as f:
    data = pickle.load(f)

# except pickle.UnpicklingError:
#     mb.showerror("Initegrity Error","Configuration file Dammaged. Stopping execution",
#         detail="(Delete Configure.cfg file and re-configuring program.)")
#     quit_func(force=True)
# else:


if not data.get('user',False):
    mb.showerror("Error: Closing Program","Program not properly Configured, stopping execution",)
    quit_func(force=True)

fernet = Fernet(key)                               # Fernet for Decryption
data["user"] = str(fernet.decrypt(data["user"]) )[2:-1] # MySql user (Decrypt)
data["pwd"] =  str(fernet.decrypt(data["pwd"])  )[2:-1] # MySql pwd (Decrypt)

# ____________________ Config END _____________________


root.deiconify() # <-- This is undoing iconification created by configuration
root.attributes("-fullscreen",True)
root.minsize(640,360)
root.focus_force()
root.bind("<F11>",lambda e:root.state("icon"))
root.bind("<Escape>",lambda e:root.attributes("-fullscreen",False) if root.attributes("-fullscreen") else root.attributes("-fullscreen",True))

Bluebox(root,default=False)
# "default=False" so that it won't destroy everything, remove default to make it delete



fr_login = LabelFrame(root,border=0,highlightthickness=0)

fr_menu = LabelFrame(root,border=0,highlightthickness=0)

fr_cus = Canvas(root,border=0,highlightthickness=0,bg="white")

fr_bil = Canvas(root,border=0,highlightthickness=0,bg="white")

fr_emp = Canvas(root,border=0,highlightthickness=0,bg="white")

fr_sto = LabelFrame(root,border=0,highlightthickness=0)

BG_change(fr_bil,default=image["back"])
BG_change(fr_emp,default=image["back"])
BG_change(fr_cus,default=image["back"])

fr_list = [fr_login, fr_menu,fr_cus, fr_emp, fr_bil,fr_sto]

def fr_forget():
    for i in fr_list:
        i.pack_forget()


# _____________________ Connection and Exit _____________________



def connection():
    try:
        global sql_obj
        sql_obj = my_db(_id=data['user'],pwd=data['pwd'],db = data['database'])
        sql_obj.connect()
    except mysql.connector.errors.ProgrammingError:
        mb.showerror("Connection Failed","Program not properly Configured, Username or database is invalid.",
            detail="Try deleting configuration file and re-configuring the program.")
        quit_func(force=True)
    except mysql.connector.errors.DatabaseError:
        mb.showerror("Unable to Connect to server","Check Internet Connection and try again!")
        quit_func(force=True)
    except mysql.connector.errors.InterfaceError:
        mb.showerror("Server Error","Server problem contact help.")
        quit_func(force=True)
    else:
        sql_obj.close()
        sql_obj.temp_file = temp3.name
connection()

loged_in = False
def login_try():
    global loged_in,res,user_changed

    if a.user == data['user'] and a.pwd == data['pwd']:
        mb.showinfo("Welcome Administrator!","Special Login Successful.\nMysql Server user and password used.")
        res = {"Name":"<MySql Administrator>", "type":"admin"}
        user_changed = True
    else:
        res = sql_obj.sql_search_few_with_id_pwd('employee',
            ['Name','type'],'user',a.user,'pwd',a.pwd)
        if not res:
            return mb.showerror("Login Failed!","Incorrect username or password. Try again.")
        user_changed = True

    if not loged_in:after_login()

    loged_in = True
    fr_forget()
    fr_menu.pack(expand=1,fill="both")







# _____________________ Frame Switch functions _____________________
def login_func():
    fr_forget()
    fr_login.pack(expand=1,fill="both")
def logout_func():
    fr_forget()
    login_func()    #Login
def menu_func():
    fr_forget()
    fr_menu.pack(expand=1,fill="both")
def customer_func():
    fr_forget()
    fr_cus.pack(expand=1,fill="both")
def employee_func():
    fr_forget()
    emp_create()    #Employee tab creater + change employee
    fr_emp.pack(expand=1,fill="both")
def bill_func():
    fr_forget()
    fr_bil.pack(expand=1,fill="both")
def stock_func():
    fr_forget()
    sto_create()    #Stock Tab creator
    fr_sto.pack(expand=1,fill="both")


# ____ Frame Func End _____



# _____________________ (creating instance) _________________

# ___ Connection based creation ___

def after_login():
    men.draw(
        img={
        'cust':image["cust420x210"],
        'emp':image["emp210x210"],
        'bill':image["bill420x210"],
        'log':image["log210x210"],
        'sto':image["stock210x420"],
        'quit':image["quit420x210"]
        })
    # __ Configuring Buttons __
    men.butt_cust.config(command=customer_func)
    men.butt_emp.config(command=employee_func)
    men.butt_bill.config(command=bill_func)
    men.butt_log.config(command = logout_func)
    men.butt_stock.config(command = stock_func)
    men.butt_quit.config(command=quit_func)
    # _ Configure End _

    cust.draw(
        menu=(image["b2mm"],(180,90),menu_func),
        bill=(image["b2bill"],(180,90),bill_func),
        emp=(image["EmpRect"],(180,90),employee_func),
        log=(image["LogoutRect"],(180,90),logout_func),
        quit=(image["quit420x210"],(180,90),quit_func),

        functions= {"search": lambda x:sql_obj.sql_search_one("customer","score",'id',x),
                    "save": lambda x:sql_obj.sql_saver('customer',x+['0'])
        })

    bil.draw(
        menu=(image["b2mm"],(180,90),menu_func),
        cust=(image['CustomerRect'],(180,90),customer_func),
        stock=(image["StocksRect"],(180,90),stock_func),
        log=(image["LogoutRect"],(180,90),logout_func),
        quit=(image["quit420x210"],(180,90),quit_func),

        functions = {"search":sql_obj.sql_search_few,
                    'cust':lambda x,y:sql_obj.sql_search_few_with_id_pwd("customer",['name'],"id",x,'passwd',y),
                    'items':lambda x:sql_obj.sql_update_quantity('Item_Name','Quantity',x),
                    'score':lambda x,y: sql_obj.sql_update_scores('customer','ID',x,y)
                    } )

    BG_change(men.can,default=image["back"])

emp_created = False
def emp_create(): # Since employee sometimes uses sql as soon as used.
    global emp_created,user_changed
    if emp_created:
        if user_changed:
            emp.change_user(res)
        return

    emp_created = True
    emp.draw(
        who = [res['Name'],res['type']],

        menu=(image["b2mm"],(120,60),menu_func),
        cust=(image['CustomerRect'],(120,60),customer_func),
        bill=(image["b2bill"],(120,60),bill_func),
        log=(image["LogoutRect"],(120,60),logout_func),
        quit=(image["quit420x210"],(120,60),quit_func),

        functions = {
            'save':lambda d:sql_obj.sql_employee_data("employee",d),
            'load': lambda:sql_obj.sql_employee_data_load("employee",a.user),

            "image":[lambda u:sql_obj.sql_employee_image_download("employee",u),
                     lambda u,f:sql_obj.sql_employee_image_upload("employee",u,f) ]     }
            )

sto_created = False
def sto_create():   # Since stocks take more memory.
    # __ STOCKS __
    global sto_created
    if sto_created:
        gross.typ = utns.typ = elect.typ = res['type']
        return
    sto_created = True
    sto.draw(
        menu=(image["b2mm"],(180,90),menu_func),
        cust=(image['CustomerRect'],(180,90),customer_func),
        bill=(image["b2bill"],(180,90),bill_func),
        log=(image["LogoutRect"],(180,90),logout_func),
        quit=(image["quit420x210"],(180,90),quit_func)
        )
    sto.add_tab(gross,(lambda: sql_obj.sql_showall("Groceries"),
                      lambda val: sql_obj.sql_saver("Groceries",val),
                      lambda val: sql_obj.sql_update("Groceries",val),
                      lambda x,y: sql_obj.sql_search("Groceries",x,y)
                      ),
                "Groceries", ["P_ID int","Item_Name ","Quantity int","Price int","Batch_No int"],
                typ = res['type']
               )
    sto.add_tab(utns,(lambda: sql_obj.sql_showall("Utilities"),
                      lambda val: sql_obj.sql_saver("Utilities",val),
                      lambda val: sql_obj.sql_update("Utilities",val),
                      lambda x,y: sql_obj.sql_search("Utilities",x,y)
                      ),
                "Utilities", ["P_ID int","Item_Name ","Quantity int","Price int","Batch_No int"],
                typ = res['type']
               )
    sto.add_tab(elect,(lambda: sql_obj.sql_showall("Electronic"),
                      lambda val: sql_obj.sql_saver("Electronic",val),
                      lambda val: sql_obj.sql_update("Electronic",val),
                      lambda x,y: sql_obj.sql_search("Electronic",x,y)
                      ),
                "Electronic", ["P_ID int","Item_Name ","Quantity int","Price int","Batch_No int"],
                typ = res['type']
               )
    # ___ Background Class create ___

    BG_change(sto.can,default=image["back"])

    # ______ Class End ______

a = login.project_login(master=root,notebook=fr_login)
a.draw(login_try,quit_func,img=[image['33'],image['admin']])

men = menu.project_Menu(master=root,notebook=fr_menu)

sto = stock.project_stock(root,fr_sto)

gross = stock.NoteVar()
utns = stock.NoteVar()
elect = stock.NoteVar()

cust = customer.Project_customer(root,fr_cus)
emp = employee.Project_employee(root,fr_emp)
bil = bill.Project_bill(root,fr_bil)

# ___ start ___
fr_forget()
login_func()


root.mainloop()
