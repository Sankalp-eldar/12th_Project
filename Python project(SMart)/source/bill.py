class Project_bill:

    def __init__(self,master=None,notebook=None):
        self.root = master
        self.note = notebook
    t = ["Groceries","Utilities","Electronic"]
    def draw(self,functions=None,types=t,**kw):
        from tkinter import Button as TkButton,Label,Frame,LabelFrame,Text
        from tkinter.ttk import Button,Entry,Combobox,Scrollbar,Style
        from PIL import ImageTk,Image
        bg = self.note.configure('background')[-1]
        sty = Style()
        sty.configure("emp.TButton",font=("arial",20))
        self.functions = functions
        self.total = 0
        self.items = {i:dict() for i in types}
        self.score = 0
        self.name = None

        '''functions ---->
        ['cust'] recives id,pwd should Name or False in return
        ['search'] sql_search_one(self,table,field,_id,val)
        ['items'] recives items name and qty like {name:qty}
        ['score'] recives Customer id and score.'''

        # TkButton(self.note,text="Quit",fg="orange",bg="black",font="N 8",
        #     command=self.root.destroy).pack(fill="x",side="bottom")

        Label(self.note,text="Welcome to Smart Billing",fg="orange",bg="black",font=("arial",40,"bold")
            ).pack(side="top",fill="x",padx=10)


        fr = Frame(self.note,border=1,relief="solid",bg=bg); fr.pack(padx=10,pady=10,expand=1)

        fr_cust = LabelFrame(fr,text="REGISTERED CUSTOMER?",font=("arial",20),bg=bg,border=1,relief="solid"); fr_cust.pack(padx=10,pady=5,side="bottom",fill="x")
        fr_add = Frame(fr,bg=bg); fr_add.pack(padx=10,pady=10,side="left",anchor="n")
        fr_text = Frame(fr,bg=bg); fr_text.pack(padx=10,pady=10,side="right",fill="both")

        # ________ Customer id,pwd ________
        def cust():
            from tkinter.messagebox import askokcancel
            ch = askokcancel("Clear Cart?","This will Clear anything in Cart,Continue?",icon="warning")
            if ch not in (1,True,"ok"):
                return
            ch = functions['cust'](cust_id.get(),cust_pwd.get())
            if ch == False:
                return askokcancel("Error Missmatch","ID and Password do not match! Please try again.",
                    type="ok",icon="error")
            # askokcancel("Welcome back!",f"Welcome {ch}")
            cust_pwd.delete(0,"end")
            cust_id.configure(state="readonly");cust_pwd.configure(state='disabled')
            self.name = ch['name']
            self.total = 0
            self.items = {i:dict() for i in types}
            self.add_invoice()
        Label(fr_cust,text="ID:",bg=bg,font=("arial",20)).pack(side='left',padx=10,pady=10)
        cust_id = Entry(fr_cust,font=("arial",20) ); cust_id.pack(side="left",padx=10,pady=10)
        Label(fr_cust,text="Passwd:",bg=bg,font=("arial",20)).pack(side='left',padx=10,pady=10)
        cust_pwd = Entry(fr_cust,show='*',font=("arial",20) ); cust_pwd.pack(side="left",padx=10,pady=10)
        Button(fr_cust,style="emp.TButton",text="Submit",command=cust).pack(side="left",padx=10,pady=10)
        self.score = cust_id
        # ________ ADD Item ________
        def search(_id):
            table = sea_type.get().replace('Search Department: ','')
            value = sea_id.get() if _id == 'P_ID' else sea_name.get()
            data = functions['search'](table,('Item_Name','price'),_id, value)#[["San","32"],['a23','456'],["as qeq 2",'231']]
            try:
                if _id == 'P_ID':return change_val(data[0][0],data[0][1])
                sea_name.configure(value=data)
                def up(e):
                    d = sea_name.get().rsplit(" ",maxsplit=1)
                    change_val(d[0],d[1])
                sea_name.bind("<<ComboboxSelected>>",up)
            except IndexError:
                from tkinter.messagebox import showinfo
                showinfo("Not Found! Try again.",f"{value} was not found in {sea_type.get().replace('Search ','') } " )
            except TypeError:pass
        # self.drop = Combobox(fr_add,font=("arial",20)); self.drop.grid(row=0,column=0,padx=10,pady=10)
        def cart():
            data = (var_a.get(),var_b.get(),var_c.get())
            if '' not in data:
                self.add_item(data[0],data[1],data[2],
                    sea_type.get().replace('Search Department: ','')    )

        Button(fr_add,style="emp.TButton",text="Add To Cart",command=cart
            ).grid(row=7,column=1,sticky="news",padx=10,pady=10)
        Button(fr_add,style="emp.TButton",text="Search with ID:",command=lambda:search("P_ID")
            ).grid(row=1,column=0,sticky="news",padx=10,pady=10)
        Button(fr_add,style="emp.TButton",text="Search with Name:",command=lambda:search("Item_Name")
            ).grid(row=2,column=0,sticky="news",padx=10,pady=10)
        sea_id = Entry(fr_add,font=("arial",16)); sea_id.grid(row=1,column=1,pady=10)
        sea_name = Combobox(fr_add,font=("arial",16) ); sea_name.grid(row=2,column=1,pady=10)
        sea_type = Combobox(fr_add,value=["Search Department: " + i for i in types],state="readonly",
            font=("arial",16)); sea_type.grid(row=0,column=0,columnspan=2,sticky="news",padx=10,pady=10)
        sea_type.current(0)


        def change_val(a,c):
            var_a.configure(state="normal");var_a.delete(0,"end");var_a.insert(0,a);var_a.configure(state="readonly")

            # var_b.configure(state="normal");var_b.delete(0,"end");var_b.insert(0,a);var_b.configure(state="readonly")

            var_c.configure(state="normal");var_c.delete(0,"end");var_c.insert(0,c);var_c.configure(state="readonly")

        Label(fr_add,text="Item: ",bg=bg,font=("arial",20)).grid(row=4,column=0)
        Label(fr_add,text="Quantity: ",bg=bg,font=("arial",20)).grid(row=5,column=0)
        Label(fr_add,text="Price/Unit: ",bg=bg,font=("arial",20)).grid(row=6,column=0)
        var_a = Entry(fr_add,font=("arial",16),state="readonly"
            ); var_a.grid(row=4,column=1,sticky="news",padx=10,pady=10)
        var_b = Combobox(fr_add,font=("arial",16),value=[str(i) for i in range(1,11)],state="readonly"
            );var_b.grid(row=5,column=1,sticky="news",padx=10,pady=10)
        var_c = Entry(fr_add,font=("arial",16),state="readonly"
            );var_c.grid(row=6,column=1,sticky="news",padx=10,pady=10)
        var_b.current(0)
        def purchase():
            self.add_end()
            functions['items'](self.items)
            ok.pack(side="bottom",anchor='e')
        Button(fr_add,style="emp.TButton",text="Purchase",command=purchase
            ).grid(row=7,column=0,sticky="news",padx=10,pady=10)



        # ________ Text box ________
        scr = Scrollbar(fr_text); scr.pack(side="right",fill="y",pady=10)
        self.txt = Text(fr_text,state="disabled",width=50,relief="solid",yscrollcommand=scr.set,font=("MS PGothic",11,"bold")
            ); self.txt.pack(pady=10,side="right")
        scr.config(command=self.txt.yview)
        self.add_invoice()
        def reset():
            change_val('','')
            sea_id.delete(0,"end") ;sea_name.delete(0,"end")
            self.txt.delete(1.0,"end")
            cust_id.configure(state="normal");cust_id.delete(0,"end")
            cust_pwd.configure(state="normal");cust_pwd.delete(0,"end")
            self.items = {i:dict() for i in types}
            self.name = None
            self.total = 0
            self.add_invoice(); ok.forget()

        ok = Button(fr,text="Ok/Reset",command=reset);ok.pack(side="bottom",anchor='e');ok.forget()
        # ________ BASIC MENU ________
        fr_men = Frame(self.note,bg=bg); fr_men.pack(pady=1)
        for g in kw:
            r = kw[g]
            kw[g] = [ImageTk.PhotoImage(Image.open(r[0]) if not isinstance(r[1] if len(r) >= 2 else None,tuple) else Image.open(r[0]).resize(r[1]))]#r[0] if "." not in r[0] else 
            kw[g].insert(0,TkButton(fr_men,image=kw[g],border=0,highlightthickness=0,
              command=r[2] if len(r) == 3 else r[1] if len(r) == 2 else None))
            kw[g][0].pack(side="left")
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

    def add_invoice(self):
        from datetime import datetime
        from random import randint,choice
        self.txt.configure(state="normal")
        self.txt.delete(1.0,"end")
        invoice_id = [str(randint(10,99)),choice([chr(i) for i in range(65,91)]),#["A", "B", "C", "D"]),
                      str(randint(10,99)),choice([chr(i) for i in range(97,123)])]#["a", "b", "c", "d", "e"])]
        text = f"""**************************************************
                             CASH RECEIPT
==================================================
                 SMart - One shop to rule 'em all  

==================================================

         Date               - {datetime.today().date()}
         Invoice ID        - {''.join(invoice_id)}
         Customer Name  - {self.name}

--------------------------------------------------
==================================================


         ITEM                               Qty               Price  
"""
        self.txt.insert(1.0,text)
        self.txt.configure(state="disabled")
    def add_end(self):
        self.txt.configure(state="normal")
        text = f'''
--------------------------------------------------
     SubTotal                                               {self.total}
                                       CGST(6%)        +{self.total*0.06}
                                       SGST(6%)        +{self.total*0.06}
--------------------------------------------------
                GRAND TOTAL   ::         {self.total+(self.total*0.12)} Rs.
--------------------------------------------------


                               (QR Code Here)



                          Thanks For Shopping
**************************************************'''
        self.txt.insert("end",text)
        self.txt.configure(state="disabled")
        if self.total>1000 and self.score.get() != "":
            self.functions['score'](self.score.get(),round(self.total/100,1))


    def add_item(self,name,qty,price,dept):
        self.txt.configure(state="normal")
        self.total += int(qty)*int(price)
        if "{" in name:name = name[1:-1]
        nam = "\n   " + name + " "*(37-len(name))  #44,62
        qt = qty + ' '*(18-len(qty))
        item = ''.join([nam,qt,price])
        self.txt.insert("end",item)
        self.txt.configure(state="disabled")
        try:
            self.items[dept][name] += int(qty)
        except KeyError:
            self.items[dept].update({name:int(qty)})


if __name__ == '__main__':
    from tkinter import Tk

    root = Tk()
    root.configure(bg="white")
    root.attributes("-fullscreen",True)
    a = Project_bill(root,root)
    a.draw(
        menu=("bill420x210.png",(120,60)),
        cust=('CustomerRect.png',(120,60)),
        log=("LogoutRect.png",(120,60)),
        quit=("quit420x210.png",(120,60),root.destroy) )

    root.mainloop()