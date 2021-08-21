from tkinter import Frame

class Heading(Frame):
    def __init__(self,master=None,heading="Company",sub_heading="Application Form",**kw):
        super().__init__(master,**kw)
        from tkinter import Label
        from tkinter.ttk import Separator

        bg = self.config("bg")[-1]
        Label(self,text=heading,font=("helvetica",20,"bold"),anchor="w",bg=bg).grid(sticky="w")
        Label(self,text=sub_heading,font=("helvetica",24),anchor="w",bg=bg).grid(sticky="w")

        Separator(self,orient="vertical").grid(row=0,column=1,rowspan=2,sticky="news")
        Label(self,text="Note:All fields with (*) are mendatory.",bg=bg).grid(sticky="s",row=1,column=2)
        Separator(self).grid(sticky="news",row=2,columnspan=5)
    
    def clear(self):
        pass
    def get(self):
        return None
    def get_raw(self):
        return self
    def name(self):
        return "heading"

class Personal_info(Frame):
    var = ["Name","Address","City","State","ZIP/PIN","Phone","Email","DOB"]
    def __init__(self,master=None,fields=var,fg=None,**kw):
        super().__init__(master,**kw)
        from tkinter import Label
        from tkinter.ttk import Separator
        try:
            from Utility import ttkEntry as Entry
        except:
            from source.Utility import ttkEntry as Entry

        self.info = []
        fields = Entry.limit_sep(fields)
        bg = self.config("bg")[-1]

        Separator(self).pack(fill="x")
        Label(self,text="Personal Information*",font=("heavy",18,"bold"),bg=bg).pack(anchor="w")
        Separator(self).pack(fill="x",pady=4)

        fr = Frame(self,bg=bg); fr.pack(fill="both",expand=1)

        fr_n = Frame(fr,bg=bg); fr_n.pack(fill="both",expand=1)
        Label(fr_n,fg=fg,text=fields[0][0],bg=bg).pack(side="left",padx=10)
        a = Entry(fr_n,bind=fields[2][0],limit=fields[1][0]);a .pack(fill="x",anchor="center",padx=5)
        Separator(fr).pack(anchor="s",fill="x",padx=5,pady=4)
        self.info.append(a)

        fr1 = Frame(fr,bg=bg); fr1.pack(fill="both",expand=1,padx=10)
        div = int(len(fields[0][1:])/2)
        for i,val in enumerate(fields[0][1:]):
            if i <= div:
                bind,lim = fields[2][i+1],fields[1][i+1]
                Label(fr1,fg=fg,bg=bg,text=val).grid(row=0,column=i)
                a = Entry(fr1,limit=lim,bind=bind); a.grid(row=1,column=i,padx=8)
                self.info.append(a)
            else:
                bind,lim = fields[2][i+1],fields[1][i+1]
                Label(fr1,fg=fg,bg=bg,text=val).grid(row=2,column=i-div)
                a = Entry(fr1,limit=lim,bind=bind); a.grid(row=3,column=i-div,padx=8)
                self.info.append(a)
        Separator(fr).pack(anchor="s",fill="x",pady=4)
    
    def clear(self):
        for i in self.info:
            i.configure(state="active")
            i.delete(0,"end")
    def get(self):
        return [i.get() for i in self.info]
    def get_raw(self):
        return self.info
    def name(self):
        return "personal"

class Legal_info(Frame):
    ques = ["Are you legally authorized to work in this country?",
    "Have you been convicted of a felony?", "Have you been employed by this organisation in past?"]
    def __init__(self,master=None,ques=ques,fg=None,**kw):
        super().__init__(master,**kw)
        from tkinter import Label,Radiobutton,IntVar
        from tkinter.ttk import Separator

        bg = self.config("bg")[-1]
        self.info = []

        Separator(self).pack(fill="x")
        Label(self,text="Additional Information*",font=("heavy",18,"bold"),bg=bg).pack(anchor="w")
        Separator(self).pack(fill="x",pady=4)

        for i in ques:
            fr = Frame(self,bg=bg); fr.pack(fill="both",padx=10)
            self.info.append(IntVar()); self.info[-1].set(2)
            Label(fr,text=i,bg=bg,fg=fg).pack(side="left")
            Radiobutton(fr,bg=bg,fg=fg,variable=self.info[-1],value=0,text="No").pack(side="right")
            Radiobutton(fr,bg=bg,fg=fg,variable=self.info[-1],value=1,text="Yes").pack(side="right")

            Separator(fr).pack(fill="x",padx=10,side="bottom",pady=4)
        Separator(self).pack(fill="x",pady=4)
    
    def clear(self):
        [i.set(None) for i in self.info]
    def get(self):
        return [i.get() for i in self.info]
    def get_raw(self):
        return self.info
    def name(self):
        return "legal"

class Position_info(Frame):
    var = ["Position Assinged:","Start Date:","Pay:"]
    typ = ["Full-Time","Part-Time","Temporary","Internship"]
    def __init__(self,master=None,fields=var,types=typ,fg=None,**kw):
        super().__init__(master,**kw)
        from tkinter import Label,Radiobutton,StringVar
        from tkinter.ttk import Separator,Entry
        # from Utility import ttkEntry as 

        self.info = []
        bg = self.config("bg")[-1]

        Separator(self).pack(fill="x")
        Label(self,text="Position Details",font=("heavy",18,"bold"),bg=bg).pack(anchor="w")
        Separator(self).pack(fill="x",pady=4)

        fr = Frame(self,bg=bg); fr.pack(fill="both",expand=1,padx=10)
        for i,val in enumerate(fields):
            Label(fr,text=val,bg=bg,fg=fg).grid(row=0,column=i)
            a = Entry(fr); a.grid(row=1,column=i,padx=4)
            self.info.append(a)
        Separator(self).pack(fill="x",pady=4,padx=10)

        Separator(self).pack(fill="x",side="bottom",pady=4)
        Label(self,text="Employment Type:",bg=bg,fg=fg).pack(padx=10,anchor="w",side="left")
        self.var = StringVar(); self.var.set("N")
        for i,val in enumerate(types[::-1]):
            Radiobutton(self,text=val,variable=self.var,value=val[0],bg=bg,fg=fg).pack(side="right",padx=10)
    
    def clear(self):
        for i in self.info:
            i.configure(state="active")
            i.delete(0,"end")
        self.var.set(None)
    def get(self):
        return [i.get() for i in self.info] + [self.var.get()]
    def get_raw(self):
        return self.info + [self.var]
    def name(self):
        return "position"

class Education_info(Frame):
    var = ["School/College", "Year", "Degree", "Result"]
    def __init__(self,master=None,titles=var,func=None,fg=None,**kw):
        super().__init__(master,**kw)
        from tkinter import Label
        from tkinter.ttk import Separator,Entry,Button

        bg = self.config("bg")[-1]
        self.info = []
        self.button = []

        Separator(self).pack(fill="x")
        Label(self,text="Education*",font=("heavy",18,"bold"),bg=bg).pack(anchor="w")
        Separator(self).pack(fill="x",pady=4)

        Separator(self).pack(fill="x",side="bottom",pady=4)
        fr = Frame(self,bg=bg); fr.pack(fill="both",expand=1,padx=5)
        self.fr = fr

        fr_temp = Frame(fr,bg=bg); fr_temp.pack(fill="x",padx=20)
        from tkinter import Entry as ET
        for i,val in enumerate(titles):
            a = Entry(fr_temp,text=val,justify="center"); a.grid(row=0,column=i,padx=2)#.pack(padx=20,side="left")
            a.insert(0,val);a.configure(state="readonly")
        del ET

        self.add()
        Button(fr,text="ADD",command=self.add).pack(side="bottom",anchor="center")
        self.bind("<MouseWheel>",func) if func else None

    def add(self):
        from tkinter.ttk import Separator,Entry,Button
        bg = self.config("bg")[-1]
        fr_temp = Frame(self.fr,bg=bg); fr_temp.pack(fill="x")
        Separator(fr_temp).pack(side="bottom",fill="x",pady=2)
        a = Button(fr_temp,text="x",width=1,command=fr_temp.destroy);a.pack(padx=2,side="left")
        self.button.append(a)

        coll = []
        for i in self.var:
            a = Entry(fr_temp);a.pack(padx=2,side="left")
            coll.append(a)
        self.info.append(coll)

    def clear(self):
        for i in self.info:
            for j in i:
                j.configure(state="active")
                j.delete(0,"end")
    def get(self):
        res = []
        for x in self.info:
            try:
                res.append( [i.get() for i in x] )
            except:pass
        return res #[ [ i.get() for i in x] for x in self.info]
    def get_raw(self):
        return self.info
    def get_pointers(self):
        return self.button
    def name(self):
        return "education"

from tkinter import Canvas
class Compiled(Canvas):
    def __init__(self,master=None,add=True,scr=False,**kw):
        super().__init__(master,**kw)
        bg = self.config("bg")[-1]

        self.frame = Frame(self,bg=bg,relief="solid",border=1)
        self.create_window(0,0,anchor="nw",window=self.frame,tag="info")

        self.frame.bind("<Configure>",self.scrollings)
        self.bind("<Configure>",self.filling)

        if scr:self.bind_scr()
        if add:self.add_frames()
        if not kw.get("width") and add:
            self.frame.update()
            self.configure(width=self.frame.winfo_reqwidth()+20)

    def add_frames(self):
        bg = self.config("bg")[-1]
        Heading(self.frame,heading="SMart",sub_heading="Employee Form",bg=bg).pack(fill="x",anchor="w")
        Personal_info(self.frame,bg=bg).pack(pady=10,fill="both")
        Legal_info(self.frame,bg=bg).pack(pady=5,fill="both")
        Position_info(self.frame,bg=bg).pack(pady=5,fill="both")
        Education_info(self.frame,bg=bg).pack(pady=5,fill="both")
    def filling(self,e):
        self.itemconfigure("info",width=self.winfo_width() )
    def scrollings(self,e):
        self.configure(scrollregion=self.bbox("info"))
    def dont(self,e):
        self.yview_scroll( int(-1*(e.delta/80)) , "units")

    def unbind_scr(self,e=None):
        self.unbind_all("<MouseWheel>")
    def bind_scr(self,e=None):
        self._scr = self.bind_all("<MouseWheel>",self.dont)
    def clear_all(self):
        [ i.clear() for i in self.frame.winfo_children() ]
    def get_all(self):
        return {i.name():i.get() for i in self.frame.winfo_children()}
    def get_all_raw(self):
        return {i.name():i.get_raw() for i in self.frame.winfo_children()}


class Project_employee:

    def __init__(self,master=None,notebook=None):
        self.root = master
        self.note = notebook
    def change_user(self,who):
        self.who_label.configure(text=f"""Welcome {who['Name']}{
            (' ('+who['type'].capitalize()+')') if who['type'] == 'admin' else ''   }""")
        if who['type'] in ('employee','emp'):self.toggel_emp(self.functions['load']())
        else:self.toggel_admin()

    def draw(self,functions={1:None},who=["Administrator","admin"],**kw):
        from tkinter import Button,Label,Frame
        from PIL import ImageTk,Image

        self.menu = kw  # for MENU Buttons
        self.functions = functions  # container of functions (bad)
        bg = self.note.configure("background")[-1]  # background color for all widgets

        """FOR 'functions' ---->
        1) 'image' = [func should give tkinter image object recieves 'user' from 'user' Entry,
                      func should take 'user' and image location]
        2) 'save' = recives Compiled.get_all() 
        3) 'load' = Has to return all data for user type 'emp'               #FUTURE FUNCTION
        """


        self.who_label = Label(self.note,text=f"Welcome {who[0]}",
            font=("helvetica",35),bg="red",relief="solid",border=1)
        self.who_label.pack(side="top",fill="x",padx=10)


        fr = Frame(self.note,bg=bg)
        fr.pack(side="right",fill="both",expand=1,pady=30)

        self.can = Compiled(self.note,bg=bg,highlightthickness=0)
        self.can.pack(fill="both",expand=1,padx=30,pady=30)

        self.note.bind("<Enter>",self.can.bind_scr)
        self.note.bind("<Leave>",self.can.unbind_scr)


        # ____________ MENU BUTTONS (right) ____________
        fr_men = Frame(fr,bg=bg); fr_men.pack(anchor="e",padx=10,side="right")
        for g in kw:
            r = kw[g]
            kw[g] = [ImageTk.PhotoImage(Image.open(r[0]) if not isinstance(r[1] if len(r) >= 2 else None,tuple) else Image.open(r[0]).resize(r[1]))]#r[0] if "." not in r[0] else 
            kw[g].insert(0,Button(fr_men,image=kw[g],border=0,highlightthickness=0,
              command=r[2] if len(r) == 3 else r[1] if len(r) == 2 else None))
            kw[g][0].pack()
            def enter(e,g=g):
              kw[g][0].config(border=1,relief="solid")
              # kw[g][0].focus_set() # better not to use
            def leave(e,g=g):
              kw[g][0].config(border=0,relief="flat")
            kw[g][0].bind("<Enter>",enter)
            kw[g][0].bind("<Leave>",leave)
            kw[g][0].bind("<FocusIn>",enter)
            kw[g][0].bind("<FocusOut>",leave)
        fr_men.update(); fr_men.pack_propagate(0)   # To stop frame from resizing entire window
        fr_men.configure(width= fr_men.winfo_reqwidth(),height= fr_men.winfo_reqheight())
        # General frame (middle)
        fr_oth = Frame(fr,border=1,relief="solid",bg=bg); fr_oth.pack(fill="both",expand=1)
        from tkinter.ttk import Button,Entry

        # ____________ USER Image ________

        self.display_image_bt = Button(fr_oth, command = self.update_image,
            text="Click to change image",compound="top")
        self.display_image_bt.pack(pady=40)

        # ____________ USER CREATION ________
        fr_bar = Frame(fr_oth,bg=bg,relief="solid",border=1); fr_bar.pack(fill="x",padx=10)
        Label(fr_bar,bg=bg,text="User ID:").pack(side="left",padx=10,pady=5)
        user = Entry(fr_bar);user.pack(side="left",pady=5)
        Label(fr_bar,bg=bg,text="Password:").pack(side="left",padx=10,pady=5)
        pwd = Entry(fr_bar,show="*");pwd.pack(side="left",pady=5)
        Button(fr_bar,text="show/hide",
            command= lambda:pwd.configure(show='') if pwd.config("show")[-1] == "*" else pwd.configure(show="*")
            ).pack(side="left",padx=2)
        Label(fr_bar,bg=bg,text="Type(Admin/emp):").pack(side="left",padx=10,pady=5)
        typ = Entry(fr_bar);typ.pack(side="left",padx=10,pady=5)

        # self.user = user;self.pwd = pwd;self.typ = typ # Keeping for Employee.
        self.user = [user,pwd,typ]
        # ____________ USER SAVE ________
        fr_bar = Frame(fr_oth,bg=bg); fr_bar.pack(fill="x",padx=10,pady=10)

        def save():
            from tkinter.messagebox import showerror
            try:
                data = self.can.get_all()
            except:
                return showerror("Incomplete Form","Form not filled properly.\nPlease complete the form.")

            data["user"] = [ user.get(),pwd.get(),typ.get() ]

            try:
                if functions.get("save"):
                    ch = functions.get("save")(data)
                    if ch:
                        return showerror("Username Exists",
                            "This Username is already taken, please choose another.",
                            icon="info")
                    stat.pack(side="left"); stat.config(text="Success",fg="green")
                    stat.after(2000,stat.forget)
                    user.configure(state="readonly"); pwd.configure(state="readonly")
                    typ.configure(state="readonly")
            except Exception as e:
                stat.pack(side="left"); stat.config(text="Failed",fg="red")
                stat.after(2000,stat.forget)
                raise e
        Button(fr_bar,text="Save/Upload Data",command = save
            ).pack(side="left",padx=10)

        def up():
            try:
                functions.get("image")[1](user.get(),self.display_image_upload)
            except AttributeError:pass
        u = Button(fr_bar,text="Upload Image", command = up)
        u.pack(side="left",padx=10)
        stat = Label(fr_bar,bg=bg)

        # Area filling
        Label(fr_oth,text="Work Smart!!",font=("Joker",72),bg="black",fg="yellow"
            ).pack(fill="both",expand=1,padx=20,pady=30)

        if who[1].lower() in ("emp","employee"):self.toggel_emp(data=functions['load']())

    def toggel_emp(self,data=None):
        ent = self.can.get_all_raw()
        # print(ent,data,sep="\n\n")
        for i,j in zip(self.user,data["user"]):
            i.delete(0,"end")
            i.insert(0,j)
            i.configure(state="readonly")
        for i,j in zip(ent["personal"],data['personal']):
            i.delete(0,"end")
            i.insert(0,j)
            i.config(state="readonly")
        for i,j in zip(ent["position"],data['position']):
            if "entry" in str(i):
                i.delete(0,"end")
                i.insert(0,j)
                i.config(state="readonly")
            else:i.set(j)
        for i,j in zip(ent["legal"],data['legal']):
            i.set(j)

        if self.functions.get("image"):
            self.display_image = self.functions["image"][0](self.user[0].get())
            self.display_image_bt.configure(image = self.display_image)

        # ____________ #Education_is_different!
        edu_instance = [x for x in self.can.frame.winfo_children() if x.name() == "education"][0]
        edu_rows = [i.winfo_exists() for i in edu_instance.button]
        while edu_rows.count(1) < len(data['education']):
            edu_instance.add()
            edu_rows = [i.winfo_exists() for i in edu_instance.button]

        edu_fields = [i for i,j in zip(edu_instance.info,edu_rows) if j == 1]
        edu_instance.button = [i for i,j in zip(edu_instance.button,edu_rows) if j == 1]
        edu_instance.info = edu_fields


        for i,j in zip(edu_fields,data['education']):
            for k,val in enumerate(i):
                val.delete(0,"end")
                val.insert(0,j[k])
                val.configure(state="readonly")

    def toggel_admin(self):
        self.can.clear_all()
        [(i.configure(state="active"),i.delete(0,"end")) for i in self.user]
        self.display_image = None
        self.display_image_bt.configure(image = self.display_image)


    def update_image(self):
        from tkinter import filedialog
        from PIL import ImageTk,Image
        loc = filedialog.askopenfilename(initialdir="",
            title="Select Image",filetypes=(("PNG","*.png"),("JPG","*.jpg"),("All types","*.*")))
        if loc == "":return

        loca = Image.open(loc)
        if loca.size > (1080,720):
            from tkinter.messagebox import showerror
            showerror("Bad Size",f"Size {loca.size} is not accepted. Should be 1080x720p or below. ")
            return
        loca.thumbnail((255,255))

        self.display_image = ImageTk.PhotoImage(loca)
        self.display_image_bt.config(image=self.display_image)
        self.display_image_upload = loc
        del loc,loca

if __name__ == '__main__':
    from tkinter import Tk
    # import os
    # os.chdir("waste")
    def img():
        from PIL import ImageTk,Image
        im = Image.open("bill420x210.png")
        im.thumbnail((255,255))
        return ImageTk.PhotoImage(im)

    root = Tk()
    root.attributes("-fullscreen",True)
    root.configure()
    a = Project_employee(root,root)
    a.draw(
        #load=lambda:None,
        menu=("bill420x210.png",(120,60)),
        cust=('CustomerRect.png',(120,60)),
        log=("LogoutRect.png",(120,60)),
        quit=("quit420x210.png",(120,60),root.destroy),
        who=['A','admin'],

        functions={"image":[lambda e:img(),None] }
        )

    root.mainloop()