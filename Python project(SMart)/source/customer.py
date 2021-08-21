class Project_customer:

    def __init__(self,master=None,notebook=None):
        self.root = master
        self.note = notebook

    val = ["ID","Name","Passwd","Phone","Email",'Address']
    def draw(self,functions=None,fields=val,**kw):
        from tkinter import Button as TkButton,Label,Frame
        from tkinter.ttk import Entry,Button,Style
        from PIL import ImageTk,Image
        # from Utility import Bluebox
        # Bluebox(self.root)
        sty = Style()
        sty.configure("cust.TButton",font=("Joker",30,"bold"))
        bg = self.note.configure("background")[-1]
        self.cust_info = []

        Label(self.note,text="Customer Registrations",fg="orange",bg="black",font=("arial",40,"bold")
            ).pack(side="top",fill="x",padx=10)

        fr_ch = Frame(self.note,bg=bg); fr_ch.pack(expand=1,padx=50)
        def fr_change(fr):
            for i in fr_ch.winfo_children():
                i.forget()
            fr.pack(expand=1)


        fr_serch = Frame(fr_ch,bg=bg,relief="solid",border=1)#; fr.pack(expand=1)
        def search():
            try:
                data = functions['search']( sea.get() )
                sea.delete(0,"end")
                if data == []:
                    result.configure(text="Not found!",fg="red"); result.grid()
                    result.after(5000,result.grid_remove)
                else:
                    result.configure(text=data,fg="green"); result.grid()
                    result.after(5000,result.grid_remove)
            except Exception as e:
                result.configure(text="FAIL",fg="red"); result.grid()
                result.after(3000,result.grid_remove)
                raise e
        Label(fr_serch,bg=bg,text="Enter ID:",font=("Joker",30,"bold")).grid(row=0,column=0,pady=10,padx=10)
        sea = Entry(fr_serch,font=("Joker",30,"bold")); sea.grid(row=0,column=1,padx=20,pady=15)
        Button(fr_serch,style="cust.TButton",text="Search",command=search
            ).grid(row=1,column=0,padx=20,pady=10)
        result = Label(fr_serch,bg=bg,font=("Joker",30,"bold"))
        result.grid(row=1,column=1); result.grid_remove()
        Button(fr_serch,style="cust.TButton", text="ADD NEW",command=lambda:fr_change(fr)
            ).grid(row=2,column=1,padx=20,pady=10,sticky="news")
        Button(fr_serch,style="cust.TButton", text="Back",command=lambda:fr_change(fr_opt)
            ).grid(row=2,column=0,padx=20,pady=10)



        fr = Frame(fr_ch,bg=bg,relief="solid",border=1)#; fr.pack(expand=1)
        for i,val in enumerate(fields):
            Label(fr,text=val,bg=bg,font=("Joker",30,"bold")).grid(row=i,column=0,padx=10)
            a = Entry(fr,font=("Joker",30,"bold"));a.grid(row=i,column=1,padx=10,pady=10)
            self.cust_info.append(a)
        def save():
            try:
                functions['save']( [i.get() for i in self.cust_info] )
                stat.configure(text="Success",fg="green"); stat.grid()
                stat.after(2000,stat.grid_remove)
            except Exception as e:
                stat.configure(text="Fail",fg="red"); stat.grid()
                stat.after(2000,stat.grid_remove)
                raise e

        Button(fr,text="Save",style="cust.TButton",command=save
            ).grid(row =i//2-1, column = 2,padx=10,pady=10,sticky="w")
        Button(fr,text="Clear",style="cust.TButton",command=lambda:[i.delete(0,"end") for i in self.cust_info]
            ).grid(row =i//2, column = 2, pady=10)
        Button(fr,text="Back",style="cust.TButton",command=lambda:fr_change(fr_opt)
            ).grid(row =i//2+1, column = 2, pady=10,padx=10,sticky="e")
        stat = Label(fr,text="Success",font=("Joker",30,"bold"),fg="green")
        stat.grid(row=len(fields)-1,column=2); stat.grid_remove()


        fr_opt = Frame(fr_ch,bg=bg); fr_opt.pack(expand=1)
        Button(fr_opt,style="cust.TButton", text="ADD NEW",
            command=lambda:fr_change(fr)).pack(side="left",padx=10,expand=1)
        Button(fr_opt,style="cust.TButton", text="CHECK POINTS",
            command=lambda:fr_change(fr_serch)).pack(side="left",padx=10,expand=1)

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

if __name__ == '__main__':
    from tkinter import Tk

    root = Tk()
    root.attributes("-fullscreen",True)
    a = Project_customer(root,root)
    a.draw(
        menu=("bill420x210.png",(120,60)),
        cust=('CustomerRect.png',(120,60)),
        log=("LogoutRect.png",(120,60)),
        quit=("quit420x210.png",(120,60),root.destroy) )

    root.mainloop()