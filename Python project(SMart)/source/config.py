class Configure_db:
    import pickle
    def __init__(self,master,file_name,deicon=True):
        self.root = master
        self.file = file_name
        self.deicon = deicon

    def __call__(self,ico,img):
        try:
            self.base_config("Configure Database",img=img,ico=ico)
        except FileNotFoundError:
            with open(self.file,"wb") as f:
                self.pickle.dump({1:"Don't open such files"},f)

            self.base_config(img=img,ico=ico)
    def db_config(self,id_,pwd_,**kw):
        try:
            from db_creater import log_Structure
            from Utility import key
        except ModuleNotFoundError:
            from source.db_creater import log_Structure
            from source.Utility import key
        finally:
            from cryptography.fernet import Fernet

        from tkinter.messagebox import showinfo as mb
        try:
            call = log_Structure(id_,pwd_,db=kw.get("db"),data=kw.get("data",False))
            call.CREATE()
            call.close()
            with open(self.file,"rb+") as f:
                data = self.pickle.load(f)
                f.seek(0);f.truncate()
                fernet = Fernet(key)
                data['database'] = kw.get("db",False)
                data['user'] = fernet.encrypt(id_.encode())
                data['pwd'] = fernet.encrypt(pwd_.encode())
                self.pickle.dump(data,f)
            self.base.destroy()
            mb("Success!","Configuration Complete.",detail="Database has been setup Successfully!")
        except Exception as e:
            if "Access denied" in str(e):
                return mb("Access denied","Incorrect username or password. Please try again.",icon="error")
            elif "Can't connect" in str(e):
                return mb("Unable to Connect to server","Check Internet Connection and try again!")
            mb("An Error Occurred","Sorry an error occurred.\nPlease try again or contact help",icon="error")
            self.base.focus_force()

    def base_config(self,where="Configuration file missing",img=None,ico=None):

        run = False
        with open(self.file,"rb") as f:
            try:
                data = self.pickle.load(f)
                if not data.get('configured',False):run = True
            except EOFError:
                raise FileNotFoundError

        if run:
            from tkinter import Toplevel,Checkbutton,IntVar,Label,Message,Frame,Entry
            from tkinter.messagebox import showinfo as mb
            from PIL import ImageTk,Image
            self.base = Toplevel(self.root)
            self.root.withdraw()
            self.base.title("Configure Database")
            self.base.iconbitmap(ico)
            self.base.resizable(0,0)
            self.base.config(bg="white")
            w,h = self.base.winfo_screenwidth(),self.base.winfo_screenheight()
            self.base.geometry(f'444x202+{(w-420)//2}+{(h-354)//2}')
            def quit():
                self.base.destroy()
                self.root.deiconify() if self.deicon else None
                mb("Configuration Stopped",
                    "Configuration Stopped by User,\napplication might not work properly.",
                    master=self.root,icon="warning")
                if data.get('user',True):
                    with open(self.file,"wb") as f:
                        data['configured'] = False
                        self.pickle.dump(data,f)
            self.base.protocol("WM_DELETE_WINDOW",quit)
            #self.base.overrideredirect(True)
            #self.base.pack_propagate(False)

            global x
            x = ImageTk.PhotoImage(Image.open(img).resize((150,146)))
            Label(self.base,image = x,border=0,highlightthickness=0,bg="white").pack(side="left",expand=0)
            fr = Frame(self.base,bg="white",border=0,highlightthickness=0)
            fr.pack(side="right",fill="both",expand=1)

            text= f"{where}.\n\nPerhaps this application has\nnot been configured?"
            Message(fr,text=text,bg="white",font=(None,14),width=300).pack()#fill="both",expand=1)

            def change():
                if data.get('user',True):
                    var1.set(1)
                    return mb('User Missing','You cannot uncheck this field',
                        detail="""'User' information not found, please proceed and provide necessary information.
If you have database for this application, please provide name in next tab.""")
                self.base.focus_set()
                if var1.get() == 0:lab.config(text="(No, I already have database)");db_e.place(x=160,y=126)
                else:lab.config(text="(Yes, setup database)");db_e.place_forget()

            from tkinter.ttk import Button
            var1 = IntVar()
            var2 = IntVar()
            ch1 = Checkbutton(fr,text="Do you want to configure required database?",bg="white",
                variable=var1,command=change)
            ch1.pack()
            ch1.select()
            lab = Label(fr,text="(Yes, setup database)",bg="white")
            lab.pack(anchor="w")

            ch2 = Checkbutton(fr,text="Don't ask me this again",bg="white",
                variable=var2,command=change)
            ch2.select()
            ch2.pack(anchor="w")

            Button(fr,text="Cancel",command=quit).pack(side="right",padx=4,pady=4)# or root.destroy()

            def ask_():
                nonlocal db_e
                db_e = Entry(fr,width=18,fg="gray",relief="solid")
                db_e.insert(0,"Name of database*")
                db_e.bind("<FocusIn>",lambda e:(db_e.config(fg="black"),db_e.delete(0,"end")) if db_e.get() == "Name of database*" else None)
                db_e.bind("<FocusOut>",lambda e:(db_e.config(fg="gray"),db_e.insert(0,"Name of database*")) if db_e.get() == "" else None)
            db_e=None;ask_()

            def done(self=self):
                if var2.get():
                    with open(self.file,"rb+") as f:
                        data = self.pickle.load(f)
                        f.seek(0);f.truncate()
                        data['configured'] = True if var2.get() == 1 else False
                        self.pickle.dump(data, f)
                        # temp = f.readlines();f.seek(0);f.truncate()
                        # f.write("Configured - True\n") if var2.get() == 1 else f.write("Configured - False\n")
                        # f.write(temp[1]) if len(temp) == 2 else None
                        # del temp
                # __ (above) config writen __
                # __ (below) to create database __
                if var1.get() == 0:
                    nonlocal db_e
                    if db_e.get() in ("","Name of database*"):
                        mb("Database required","Enter name of Database connected to this application.",
                            detail="Details:\n(Configuration file is missing name of database.\nYou are seeing this error since you have chosen\nnot to configure required database)")
                        return db_e.focus_set()
                    with open(self.file,"rb+") as f:
                        data = self.pickle.load(f)
                        f.seek(0);f.truncate()
                        data['database'] = db_e.get()
                        self.pickle.dump(data, f)

                    self.root.deiconify() if self.deicon else None
                    self.base.destroy()
                    mb("Configuration Complete","Configuration complete, Thank you for your co-operation",master=self.root)
                    return

                nonlocal fr
                fr.destroy()
                fr = Frame(self.base,bg="white",border=0,highlightthickness=0)
                fr.pack(side="right")


                text = "Provide a user with permission\nto create database"
                Message(fr,text=text,bg="white",font=(None,14),width=300).grid(row=0,column=0,columnspan=4,sticky="w")#.pack()

                from tkinter import Entry
                Label(fr,text="User*:",bg="white").grid(row=1,column=0,sticky="w")#.pack(side="left")
                id_e = Entry(fr,width=18,relief="solid")
                id_e.grid(row=1,column=2,columnspan=3,sticky="w")#.pack(side="left",padx=2)

                Label(fr,text="Password*:",bg="white").grid(row=2,column=0,sticky="w")#.pack(side="left")
                pwd_e = Entry(fr,width=18,relief="solid",show="*")
                pwd_e.grid(row=2,column=2,columnspan=3,sticky="w")#.pack()

                def custom():
                    if var1.get()==1:db_e.config(state="normal");db_e.delete(0,"end");db_e.focus_set()
                    else:db_e.insert(0,"testdb");db_e.config(state="disabled")
                ch1 = Checkbutton(fr,text="Custom database name?",bg="white",variable=var1,command=custom)#(default 'testdb')
                ch1.grid(row=3,column=0,columnspan=4,sticky="w")#.pack(pady=4)

                Label(fr,text="Name Database as*:",bg="white").grid(row=4,column=0,columnspan=2)#.pack(side="left")#,anchor="w")
                db_e = Entry(fr,relief="solid",width=16)
                db_e.grid(row=4,column=2)#.pack(padx=4)
                db_e.insert(0,"testdb");db_e.config(state="disabled");ch1.deselect()

                ch2 = Checkbutton(fr,text="Add test data?",bg="white",variable=var2)
                ch2.grid(row=5,column=0,columnspan=4,sticky="w");ch2.deselect()

                Button(fr,text="Cancel",command=quit).grid(row=6,padx=4,pady=4,column=3,sticky="e")
                Button(fr,text="Next",
                    command=lambda:self.db_config(id_e.get(),pwd_e.get(),db=db_e.get(),data=True if var2.get()==1 else False
                        ) if "" not in (id_e.get(),pwd_e.get(),db_e.get()) else mb("Configure Database","Please provide the required fields.",master=self.base)
                    ).grid(row=6,column=1,padx=4,pady=4,sticky="e",columnspan=2)

            Button(fr,text="Next",command=done).pack(padx=4,pady=4,anchor="e")
            self.base.focus_force()
        else:
            from tkinter import Toplevel
            self.base = Toplevel(self.root)
            self.base.transient(self.root)
            self.base.overrideredirect(True)
            self.base.geometry("0x0")
            self.base.after(1,self.base.destroy)
    # def print(self):
    #     return x

if __name__ == "__main__":
    from tkinter import Tk
    root = Tk()
    #root.iconbitmap("Icon.ico")

    a = Configure_db(root,"Configure.txt")
    a()
    root.wait_window(a.base)
    root.destroy()
    # from _tkinter import TclError
    # try:root.deiconify()
    # except TclError:print("Execution complete")
    root.mainloop()
