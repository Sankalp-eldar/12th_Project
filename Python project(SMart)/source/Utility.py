# Utility module, I mean useful stuff...?
# Entry,ttkEntry,BG_change,Bluebox,(valid_sep,limit_sep)included in Entry

HERE = AVAILABLE = """
key <Fernet Generated key for encryption/decryption>

Logger(file)    <Output in file, use on sys.stdout>

Entry(master=None,bind=None,*args,**kwargs) <tk>,
ttkEntry(master=None,bind=None,*args,**kwargs)  <ttk Entry>,
BG_change(can,default = None,bluebox = False,config=True)  <"can" is Canvas object>,
Bluebox(windo,default=True)  <"default" if True, removes widget>,
valid_sep(fields)  <A function [name],[bind]>
limit_sep(fields)  <A function [name],[limit],[bind]>
"""

key = b"T3Gx4M2bkN0d_eOBwockQ-V40LeDM7FF8C2QbUgsTrY="   # DND

class Logger:

    def __init__(self,file):
        self.f = file
        with open(self.f,'w') as f:
            pass
    def write(self,content):
        with open(self.f,'a') as f:
            f.write(str(content))
    def flush(self,content=None):
        if content is not None:
            with open(self.f,'a') as f:
                f.write(str(content))
    def remove_if_blank(self):
        import os
        f = open(self.f)
        if not f.read():
            f.close();os.remove(self.f)
        f.close()

# Exchange for 'Entry', To make "validate" and "validatecommand" easier for me
### Removed a lot of 'help' text for this Entry,
from tkinter import Entry as ET
from tkinter.ttk import Entry as ttkET

class Entry(ET):

    def __init__(self,master=None,bind=None,limit="None",*args,**kwargs):
        super().__init__(master,*args,**kwargs)
        self._only = bind
        self._limit = int(limit) if limit not in ("None","") else None
        # self.avaliable = " 'int','str', 'special','float','alnum','noint','nostr','custom' "
        self.validatator()

    def validatator(self):
        if self._only not in (None,""," "):
            if self._only == "str":
                vcmd = (self.register(self.str_ch),"%d","%S","%P")
            elif self._only == "int":
                vcmd = (self.register(self.int_ch),"%d","%S","%P")
                self.configure(justify="right")
            elif self._only == "special":
                vcmd = (self.register(self.special_ch),"%d","%S","%P")
            elif self._only == "float":
                vcmd = (self.register(self.float_ch),"%d","%P")
                self.configure(justify="right")
            elif self._only == "alnum":
                vcmd = (self.register(self.alnum_ch),"%d","%S","%P")
            elif self._only == "noint":
                vcmd = (self.register(self.noint_ch),"%d","%S","%P")
            elif self._only == "nostr":
                vcmd = (self.register(self.nostr_ch),"%d","%S","%P")
            elif self._only.startswith("custom"):
                try:
                    x = self._only.split(" ",maxsplit=2)
                    if x[1] == "-a":
                        vcmd = (self.register(self.custom_a_ch),"%d","%P")
                    elif x[1] == "-d":
                        vcmd = (self.register(self.custom_d_ch),"%d","%P")
                    else:
                        raise ValueError("-a or -d")
                    self.custom = x[2]
                except IndexError:
                    raise SyntaxError('''bind = "custom -a 1234" or something''')
            else:
                raise ValueError(" 'bind' values are only 'int','str', 'special','float','alnum','noint','nostr','custom' ")
            self.configure(validate="key", validatecommand=vcmd)

    def str_ch(self,d,s,p):
        '''Allows only A-Z (not case sensitive)'''
        if d == "1":
            if p[:self._limit] == p:
                return s.isalpha()
            else:
                return False

        return True

    def int_ch(self,d,s,p):
        '''Allow only numbers (use bind="float" for float numbers)'''
        if d == "1":
            if p[:self._limit] == p:
                return s.isnumeric()
            else:
                return False
        return True

    def noint_ch(self,d,s,p):
        '''Allow everything except numbers \n(Please tell me why would you use this.)'''
        if d == "1":
            if p[:self._limit] == p:
                return not s.isnumeric()
            else:
                return False
        return True

    def nostr_ch(self,d,s,p):
        '''Allow everything except A-Z (Cases Like: +91999)'''
        if d == "1":
            if p[:self._limit] == p:
                return not s.isalpha()
            else:
                return False
        return True

    def float_ch(self,d,p):
        '''Allow float numbers (Ex:- 19.5)'''
        if d == "1":
            if p[:self._limit] == p:
                try:
                    float(p)
                    return True
                except ValueError:
                    return False
            else:
                return False
        return True

    def alnum_ch(self,d,s,p):
        '''Allow Alpha-numeric (A-Z and 0-9)(no spaces etc.)\n(works with .isalnum() from inbuilt str class)'''
        if d == "1":
            if p[:self._limit] == p:
                return s.isalnum()
            else:
                return False
        return True

    def special_ch(self,d,s,p):
        '''Works same as bind='alnum' except this allow spaces'''
        if d == "1":
            if p[:self._limit] == p:
                if s.isalnum() or s == " " or (s.replace(" ",'').isalnum() and " " in s):
                    return True
                else:return False
            else:
                return False
        return True
    def custom_a_ch(self,d,p):
        if d == "1":
            if p[:self._limit] == p:
                for i in p:
                    if i not in self.custom:
                        return False
                return True
            else:
                return False
        return True
    def custom_d_ch(self,d,p):
        if d == "1":
            if p[:self._limit] == p:
                for i in p:
                    if i in self.custom:
                        return False
                return True
            else:return False
        return True
 # __________ ENTRY class END ___________

    @staticmethod
    def valid_sep(fields):
        local_x = ([],[])
        for i in fields:
            if " " in i:
                a = i.split(" ",maxsplit=1)
                local_x[0].append(a[0]);local_x[1].append(a[1])
            else:
                local_x[0].append(i);local_x[1].append(None)
        return local_x

    @staticmethod
    def limit_sep(fields):
        local_x = ([],[],[])
        for i in fields:
            if " " in i:
                a = i.split(" ",maxsplit=2)
                local_x[0].append(a[0]); local_x[1].append(a[1]); local_x[2].append(a[2])
            else:
                local_x[0].append(i); local_x[1].append(None); local_x[2].append(None)
        return local_x

class ttkEntry(Entry,ttkET):
    def __init__(self,master=None,bind=None,limit=None,*args,**kw):
        ttkET.__init__(self,master,*args,**kw)
        self._only = bind
        self._limit = limit
        self.validatator()


# __________ Seperator for above Entry field use _________
# well, valid_sep() {below} is made with certain idea in mind.
# idea is: fields = valid_sep(fields)
# Then
# for i,val in fields[0]:
#   Label(root,text= val )
#   Entry(root,bind= fields[1][i] )
# That would set the bind type.
def valid_sep(fields):
    local_x = ([],[])
    for i in fields:
        if " " in i:
            a = i.split(" ",maxsplit=1)
            local_x[0].append(a[0]);local_x[1].append(a[1])
        else:
            local_x[0].append(i);local_x[1].append(None)
    return local_x
def limit_sep(fields):
    local_x = ([],[],[])
    for i in fields:
        if " " in i:
            a = i.split(" ",maxsplit=2)
            local_x[0].append(a[0]); local_x[1].append(a[1]); local_x[2].append(a[2])
        else:
            local_x[0].append(i); local_x[1].append(None); local_x[2].append(None)
    return local_x



# ________________________________ BG_change CLASS START __________________________________

class BG_change:

    def __init__(self,can,default = None,bluebox = False,config=True):
        from tkinter import LabelFrame
        from tkinter.ttk import Combobox,Button
        from tkinter import messagebox as mb
        from tkinter import filedialog as fd
        from PIL import Image,ImageTk
        import os
        can.pack_propagate(0)
        def size():
            can.delete('BG_change')
            # can.update()
            w = can.winfo_width()
            h = can.winfo_height()
            
            self.x = ImageTk.PhotoImage(self.default.resize((w,h)))
            can.create_image(0,0,anchor='nw',image=self.x,tag="BG_change")

        if default != None:
            self.default = Image.open(default)
            size()
        bg_fr = LabelFrame(can,bg="yellow",border=0,highlightthickness=0)

        bg = Button(bg_fr,text="Default BG",command= size if default != None else None)
        bg.pack(side='right')

        close = Button(bg_fr,text="x",width=0,command=lambda:can.focus() or bg_fr.place_forget())
        close.pack(side='left')
        
        bg_loc = Button(bg_fr,text='Image Location')
        bg_loc.pack(side='left')

        bg_set = Button(bg_fr,width=0,text='Set')
        bg_set.pack(side='left')

        bg_image = Combobox(bg_fr,width=15,state='readonly')
        bg_image.pack(side='left')
        a = []
        for i in os.listdir('.'):
                if '.jpg' in i or '.png' in i or '.jpeg' in i:
                        a.append(i)
        bg_image.config(values=a)
        if a != []:
            bg_image.current(0)

        def find():
                global loc
                loc = fd.askdirectory()
                if loc == '':return
                a = []
                for i in os.listdir(loc):
                        if '.jpg' in i or '.png' in i or '.jpeg' in i:
                                a.append(i)
                        if len(a)==100:break
                bg_image.config(values=a)
                if a != []:
                    bg_image.current(0)
                else:
                    mb.showinfo("No Image Found!","Only '.jpg', '.jpeg', '.png' searched")

        bg_loc.config(command= find)

        def set_img():
            can.update()
            w = can.winfo_width()
            h = can.winfo_height()
            op = bg_image.get()
            try:
                    a = loc + '/'+op
            except:a= op
            
            if op == '':return
            can.delete('all')

            self.x = ImageTk.PhotoImage(Image.open(a).resize((w,h)))
            can.create_image(0,0,anchor='nw',image=self.x)

        bg_set.config(command=set_img)
        def clicked(e):
            
            # ___ precaution against my other module __
            bg.pack_forget()
            close.pack_forget()
            bg_loc.pack_forget()
            bg_set.pack_forget()
            bg_image.pack_forget()

            bg.pack(side='right')
            close.pack(side='left')
            bg_loc.pack(side='left')
            bg_set.pack(side='left')
            bg_image.pack(side='left')
            
            bg_fr.place(x=e.x,y=e.y)
            
        if not bluebox:
          can.bind("<Button-3>",lambda e: bg_fr.place(x=e.x,y=e.y))
        else:
          can.bind("<Button-3>",clicked)

        if config:can.bind("<Configure>",lambda e:size())




# ________________________________________ Bluebox CLASS START ________________________________

class Bluebox:
    
    def __init__(self,windo,default=True):
        from tkinter import Toplevel
        roo = Toplevel()
        roo.attributes("-topmost",True)
        roo.overrideredirect(True)
        roo.geometry("0x0+0+0")
        roo.attributes("-alpha",0.3)


        roo.configure(bg="#0080ff") # COLOR of selector


        def bluebox(e):
            x_co = roo.winfo_pointerx()
            y_co = roo.winfo_pointery()
            roo.geometry(f"+{x_co-2}+{y_co-2}")

            def boxsize(ev):
                a = ev.x-e.x if ev.x-e.x >=0 else e.x - ev.x
                b = ev.y-e.y if ev.y-e.y >=0 else e.y - ev.y
                roo.geometry(f"{a}x{b}")
                global coord
                coord = roo.geometry()


            def release():
                def selected():
                    core = coord.split("+")
                    core[0] = core[0].split("x")
                    st_x,st_y = int(core[1]),int(core[2])
                    fin_x,fin_y = int(core[0][0])+int(core[1]), int(core[0][1])+int(core[2])
                    destroy = []
                    def deep(parent):
                        for i in parent.winfo_children():
                            if "canvas" in str(i) or "frame" in str(i) or 'notebook' in str(i):
                                if "frame" in str(i):
                                    if i.winfo_ismapped() == 1:destroy.append(i)
                                for k in i.winfo_children():
                                    if k == []:
                                        break
                                    else:
                                        destroy.append(k)
                                        deep(k)
                            else:
                                destroy.append(i)
                    deep(windo)
                    for abc in destroy:
                        a,b = abc.winfo_rootx(),abc.winfo_rooty()
                        if (a >=st_x and a <=fin_x) and (b >= st_y and b <= fin_y) and "toplevel" not in str(abc):
                            # if 'notebook' not in str(abc) else None
                            # <><><><><><><><><><><><> CHECK <><><><><><><><><><
                            abc.forget()
                            abc.place_forget()
                            abc.grid_forget()
                            abc.pack_forget()
                            #print(str(abc),a,b,end=" ")
                    windo.unbind("<ButtonRelease>")
                windo.bind("<ButtonRelease>",lambda e:roo.geometry("0x0+0+0") or (selected() if default == True else None))
                ##  function release end  ##

            windo.bind("<B1-Motion>",lambda ev:boxsize(ev) or release())

        windo.bind("<Button-1>",bluebox)




if __name__ == "__main__":
    # import sys
    # sys.stdout = Logger('Utility_Loggs.txt')

    from tkinter import Tk,Canvas
    root = Tk()
    can = Canvas(root,border=0,highlightthickness=0)
    can.pack(expand=1,fill='both')

    # Testing all Classes

    BG_change(can,default="back.png")

    Bluebox(can)

    fields = ("ID int","A str","B custom -a 1234","C noint","D")
    print(valid_sep(fields))
    ttkEntry(can,bind="int",width=10).pack()


    root.mainloop()