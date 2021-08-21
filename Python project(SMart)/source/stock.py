class project_stock:

    def __init__(self,master =None,notebook =None):
        self.root = master
        self.note = notebook

    def draw(self,**kw):
        self.get = kw#dict()
        from tkinter import Canvas,Label,Frame,Button
        from tkinter.ttk import Notebook
        from PIL import ImageTk,Image

        w,h = self.root.winfo_screenwidth(),self.root.winfo_screenheight()

        # op_menu = "source/back.png"#land19.jpg
        self.can = Canvas(self.note,border=0,highlightthickness=0)
        self.can.pack(fill="both",expand=1)

        # global x
        # x = ImageTk.PhotoImage(Image.open(img).resize((w,h)))
        # self.can.create_image(0,0,anchor="nw",image=x)

        Label(self.can,text="S T O C K S",font='None 32',bg="black",fg="white").pack(padx=40,side="top",fill="x")

        self.note = Notebook(self.can)
        self.note.pack(pady=20,padx=40,fill="both",expand=1)

        fr = Frame(self.can,relief="solid")

        for g in kw:
            r = kw[g]
            kw[g] = [ImageTk.PhotoImage(Image.open(r[0]) if not isinstance(r[1] if len(r) >= 2 else None,tuple) else Image.open(r[0]).resize(r[1]))]#r[0] if "." not in r[0] else 
            kw[g].insert(0,Button(fr,image=kw[g],border=0,highlightthickness=0,
              command=r[2] if len(r) == 3 else r[1] if len(r) == 2 else None))
            kw[g][0].pack()
            def enter(e,g=g):
              kw[g][0].config(border=1,relief="solid")  # BORDER =1 or =2 ???
              #fr.focus_set()                      # which would be better?
            def leave(e,g=g):
              kw[g][0].config(border=0,relief="flat")
            kw[g][0].bind("<Enter>",enter)
            kw[g][0].bind("<Leave>",leave)
            kw[g][0].bind("<FocusIn>",enter)
            kw[g][0].bind("<FocusOut>",leave)
            #self.get[g] = kw[g][0]
        self.root.update()
        fr.place(x = -fr.winfo_reqwidth()+25, y = h//4)
        fr.bind("<Enter>",lambda e:fr.place(x=0) )
        fr.bind("<Leave>",lambda e:fr.place(x=-fr.winfo_reqwidth()+25) )
        fr.bind("<FocusIn>",lambda e:fr.place(x=0) )
        fr.bind("<FocusOut>",lambda e:fr.place(x=-fr.winfo_reqwidth()+25) )


    def add_tab(self,var,functions,title="None",fields=("ID","A","B","C","D"),typ='emp'):
        self.var = var
        from tkinter import Label,Frame#,PhotoImage
        from tkinter.ttk import Notebook,Treeview,Combobox,Button,Scrollbar
        from tkinter import messagebox as mb
        from random import randint as ran
        from PIL import ImageTk,Image
        try:
            from source.Utility import ttkEntry as Entry,valid_sep
        except ModuleNotFoundError:
            from Utility import ttkEntry as Entry,valid_sep
        fields = valid_sep(fields)
        # ______ CONTENT START_______
#self.xy = PhotoImage(file="source/back.png").subsample(25,25)
#,image=self.xy,compound='left')

        # __FRAME__
        self.var.fr_main = Frame(self.note)
        self.var.typ = typ
        self.var.fr_main.pack(fill="both",expand=1)
        self.note.add(self.var.fr_main,text=title)

        fr_opt = Frame(self.var.fr_main)
        fr_opt.pack(side="top",fill="x",pady=5)

        fr_add = Frame(self.var.fr_main)
        #fr_add.pack(side="top",fill="x",pady=5)

        fr_1 = Frame(self.var.fr_main)
        fr_1.pack(fill="both",side="bottom",expand=1)

        # ___ Frame end__


        # __Search and more__
        drop = Combobox(fr_opt,width=15,value=fields[0],state="readonly")#["Search By..."],state="disabled")
        drop.current(0)
        drop.pack(side="right")

        search_text = Entry(fr_opt,width=25)
        search_text.pack(side="right")

        search_butt = Button(fr_opt,text="Search")
        search_butt.pack(side="right")

        load_butt = Button(fr_opt,text="Load")
        load_butt.pack(side="left")

        add_butt = Button(fr_opt,text="Add Item")
        add_butt.pack(side="left")

        edit_butt = Button(fr_opt,text="Enable Edit")
        edit_butt.pack(side="left")
        # __ Search END __


        # _________ ADD ITEM Fields _________
        contain = list()

        for i,val in enumerate(fields[0]):
            lab = Label(fr_add,text=val)
            ent = Entry(fr_add,width=15,bind=fields[1][i])
            lab.grid(row=0,column=i)
            ent.grid(row=1,column=i,padx=10)
            contain.append(ent)
        fields = fields[0]
        def id_config(arg = lambda:ran(10_000_000,99_999_999)):
            contain[0].config(state="active")
            contain[0].delete(0,"end")
            if callable(arg):arg = arg()
            contain[0].insert(0,arg)
            contain[0].config(state="readonly")
        id_config()
        def clear(disable=False):# Clear function
            for j in contain:
                j.delete(0,"end")
                j.config(state="readonly") if disable else None
            id_config()

        # Submit button
        def submit():
            val = [i.get() for i in contain]
            if "" in val:
                mb.showinfo("Field Empty","Fill all Fields/data required")
                return
            try:
                functions[1](val)
                tree.insert('',"0",val[0],text=val[0],values=val[1:])
                clear()
                mb.showinfo("Success","Data Added Successfully")
            except Exception as e:
              mb.showinfo("Failed","Failed to add data.",detail=f"Error code:\n {e}",icon="warning")
              print(e)
              # <>><<><><><><><><><><><><> CHECK ERRORS <><><><><><><><><><><><>
        def add():
            NOEDIT()
            fr_add.pack(side="top",fill="x",pady=5,padx=20)
            for p in contain[1:]:
                def again(p=p):
                    p.config(state="active")
                again()
            clear()
        def search():
            data = functions[3](drop.get(),search_text.get())
            for k in tree.get_children():
                    tree.delete(k)
            for k in data:
                    tree.insert('',"end",k[0],text=k[0],values=k[1:])

        search_butt.config(command=search)
        add_butt.config(command=add)
        sub_butt = Button(fr_add,text="Submit",command=submit)
        sub_butt.grid(row=1,column=i+1,padx=20)

        # _______ SLIDERS and TREE ________
        slid_x = Scrollbar(fr_1, orient= "horizontal")
        slid_y = Scrollbar(fr_1, orient= "vertical")
        slid_x.pack(side = "bottom", fill= "x",padx=20)
        slid_y.pack(side="right", fill= 'y',pady=20)

        tree = Treeview(fr_1,selectmode="browse",yscrollcommand = slid_y.set , xscrollcommand = slid_x.set)
        tree.pack(padx=20,pady=20,fill="both",expand=1)
        tree.column("#0",width=100,minwidth=100,stretch=False)
        tree.heading("#0",text=fields[0])

        slid_x.config(command = tree.xview)
        slid_y.config(command = tree.yview)
        # ______ Tree-Slider configed _____

        tree.config(column=fields[1:])
        for i in fields[1:]:
            tree.column(i,width=250,minwidth=150,stretch=False)
            tree.heading(i,text=i,anchor="w")



        # <>____ Populate DATA ___<>
        def populate():
            #edit_butt.config(text="Enable Edit",command=EDIT)
            NOEDIT()
            for k in tree.get_children():
                tree.delete(k)
            data = (i for i in functions[0]())
            for i in data:
              tree.insert('',"end",i[0],text=i[0],values=i[1:])
        load_butt.config(command=populate)

        # __ TOGGLE EDIT __
        def NOEDIT():
            fr_add.pack_forget()
            clear()
            tree.item(tree.selection(),open=False)
            tree.selection_remove(tree.selection())
            edit_butt.config(text="Enable Edit",command=EDIT)
            sub_butt.config(text="Submit",command=submit)
            for i in tree.get_children():
                for k in tree.get_children(i):
                    tree.delete(k)
            for v in contain:
                v.config(state="active")
                v.unbind("<Key>")
            id_config()
        def update():
            val = [i.get() for i in contain]
            if tree.selection() == ():return
            if "" in val: mb.showinfo("Field Empty","Fill all Fields/data required"); return
            ch = mb.askokcancel("Confirm",f"Change into {val[0]}: {val[1:]}")
            if ch in (False,"cancel",0):return
            try:functions[2](val)
            except:
                raise
                return # <>><<><><><><><><><><<><><> CHECK ERRORS <><><><><><><><><><><><>
            recover = tree.index(val[0])
            tree.delete(val[0])
            tree.insert('',recover,val[0],text=val[0],values=val[1:])
            tree.insert(val[0],'0',text="Edit to:")
            tree.selection_set(val[0])

        def EDIT():
            if self.var.typ != "admin":
              return mb.showerror("Permission Denied","Not authorized to edit.Only admin can enable edit.")
            fr_add.pack(side="top",fill="x",pady=5,padx=20)
            edit_butt.config(text="Disable Edit",command=NOEDIT)
            sub_butt.config(text="Update",command=update)
            tree.bind("<<TreeviewClose>>",lambda e:tree.selection_remove(tree.selection()) or edit_butt.focus_set() or clear(disable=True))
            for v in contain:
                v.config(state="disabled")

            a = tree.get_children()
            def close_(e):
                clear()
                id_config(tree.selection())
                ins = tree.item(tree.selection(),"values")

                for j,v in enumerate(contain[1:]):
                    v.config(state="active")
                    v.insert(0,ins[j])

                    val = [i.get() for i in contain]
                    def bind_in(e,val=val):
                        val = [p.get() for p in contain]
                        tree.item(tree.get_children(tree.selection()),values = val[1:])
                    v.bind("<Key>",bind_in)

                for i in a:
                    tree.item(i,open=False)
                contain[1].focus_set()
                    
            tree.bind("<<TreeviewOpen>>",close_)
            for i in a:
                for k in tree.get_children(i):
                    tree.delete(k)
            for i in a:
                tree.insert(i,'0',text="Edit to:")

        edit_butt.config(command=EDIT)

class NoteVar:
      pass

if __name__ =="__main__":
  from tkinter import Tk
  root = Tk()
  root.attributes("-fullscreen",True)
  a = project_stock(root,root)
  a.draw(menu=("bill420x210.png",(120,60)),
    cust=('CustomerRect.png',(120,60)),
    log=("LogoutRect.png",(120,60)),
    quit=("quit420x210.png",(120,60),root.destroy))
  #print(a.get["menu"])
  """
  self.draw now takes **kwargs.
  This will add buttons on left side,shifting notebook
  
  Fromat:- self.draw(name = ("location" , (width,heigth) , callback) )
  size'(width,height)' and callback are optional,
  you may pass only location followed by callback, i.e. ommiting size of image
  
  To access buttons use 'self.get[name][0]' where 'name' is name created in self.draw()
  Using self.get[name] returns list of 2 objects,
  at 0 is Button, at 1 is image object(useless,only to save from trash collection)
  """
  gross = NoteVar()
  utns = NoteVar()

  def load():
      data = [
          ["141151","THIS","454","98","9%"],
          ["213546","THAT","78","66","18%"],
          ["665354","SOME THING","asd ds","99.9","5%"]
          ]
      return data
  '''
  define a variable to NoteVar() (like in tkinter StringVar()) and
  pass it as first parameter in .add_tab() function

  .add_tab() then requires a list of functions/calllback can be defined as functions=(f1,f2,f3,f4)
  format of functions should be as function to fetch-data, add-data, update-data, search-data # A total of 4 functions
  some functions are given parameters:
   fetch-data (no parameter) (0)
   add-data (A list of entered data (same order as 'fields')) (1)
   update-data (A list of entered data (same order as 'fields')) (1)
   search-data (field name from dropdown, text in search box) (2)

  Since functions are called by the module on respective event,
  don't add '()' in name of functions eg: fetch_data() as fetch_data
  one can pass lambda functions too.
  eg:- lambda val: add_data(table="name",values= val)
   (lambda is given parameter as exactly one is passed by module to 'add-data'(see above))

  .add_tab() then takes heading of the tab as title="",
  .add_tab() then takes 'fields' for creating table as fields= ["","",...]
  
  ## add_tab(self,var,functions,title="None",fields=("ID","A","B","C","D"))
  '''
  fun = lambda val:print(val)
  ser = lambda x,y:print(f"Where {x} = {y}")
  a.add_tab(gross,title="Gross",
            fields=("SNO int","Product str","Quantity int","Price/unit int","GST(%) custom -a %0123456789"),
            functions=(load,fun,fun,ser))

  a.add_tab(utns,title="__TAB__",functions=(lambda:[["876453867","TEST RUN"]],fun,fun,ser),fields=["PID","Name"])
  root.mainloop()
