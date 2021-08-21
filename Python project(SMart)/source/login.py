class project_login:
	def __init__(self,master = None,notebook = None):
		self.root = master
		self.note = notebook
		self.user = ""
		self.pwd = ""
	
	def draw(self,func_login,func_quit=None,img=None):
		from tkinter import Canvas,Label,LabelFrame,Entry,Button
		from PIL import ImageTk,Image
		w,h = self.root.winfo_screenwidth(),self.root.winfo_screenheight()

		self.op = img[0]
		self.can = Canvas(self.note,border=0,highlightthickness=0)
		self.can.pack(fill="both",expand=1)

		self.x = ImageTk.PhotoImage(Image.open(self.op).resize((w,h)))
		self.can.create_image(0,0,anchor="nw",image=self.x)
		Label(self.can,text="Login Form",bg="#333",fg="red",
			  font=(None,32)).pack(fill="x")

		#ex = Button(can,text="X",width=0,command=root.destroy,border=0,highlightthickness=0,fg="white",bg="red")
		#ex.place(relx=0.99,y=0)#.pack(side=RIGHT)

		self.can2 = LabelFrame(self.can,border=0,
						  highlightthickness=0,
						  #highlightbackground="black",
						  #highlightcolor="black",
						  relief='raised',
						  bg="black",
						  height=400)

		self.can2.place(relx=0.39,rely=0.3,relwidth=0.2)

		self.box = ImageTk.PhotoImage(Image.open(img[1]))
		Label(self.can,image=self.box,border=0,highlightthickness=0).place(relx=0.468,rely=0.256)



		id_label = Label(self.can2,text="Username :",border=0,highlightthickness=0,fg="white",bg="black")
		id_label.place(relx=0.1,rely=0.25)

		id_entry = Entry(self.can2,fg="gray")
		id_entry.place(relx=0.1,rely=0.35,relwidth=0.8)


		id_entry.insert(0,"Enter Username")
		id_entry.bind("<FocusIn>", lambda e:(id_entry.delete(0,"end") or id_entry.config(fg="black")) if id_entry.get() == "Enter Username" else None)
		id_entry.bind("<FocusOut>", lambda e:(id_entry.insert(0,"Enter Username") or id_entry.config(fg="gray"))if id_entry.get() == "" else None)


		pw_label = Label(self.can2,text="Password :",border=0,highlightthickness=0,fg="white",bg="black")
		pw_label.place(relx=0.1,rely=0.5)

		pw_entry = Entry(self.can2,fg="gray")
		#relif = flat, groove, raised, ridge, solid, or sunken
		pw_entry.place(relx=0.1,rely=0.6,relwidth=0.8)
		pw_entry.insert(0,"Enter Password")
		pw_entry.bind("<FocusIn>", lambda e:(pw_entry.delete(0,"end") or pw_entry.config(show="*",fg="black")) if pw_entry.get() == "Enter Password" else None)
		pw_entry.bind("<FocusOut>", lambda e:(pw_entry.config(show="",fg="gray") or pw_entry.insert(0,"Enter Password")) if pw_entry.get() == "" else None)

		def login():
			
			if id_entry.get() not in ("Enter Username",'') and pw_entry.get() not in ("Enter Password",''):
				self.user = id_entry.get()
				self.pwd = pw_entry.get()
				func_login()
#				self.can.destroy()
			else:
				from tkinter import messagebox as mb
				mb.showinfo("Required","Enter Username and Password")
				return

		self.sub_btn = Button(self.can2,text="Login",border=0,highlightthickness=0,fg="white",bg="red")
		self.sub_btn.place(relx=0.25,rely=0.73,relwidth=0.5)
		self.sub_btn.config(command=login)
		self.sub_btn.bind("<Enter>",lambda e:self.sub_btn.config(fg="black",bg="yellow"))
		self.sub_btn.bind("<Leave>", lambda e:self.sub_btn.config(fg="white",bg="red"))
		self.sub_btn.bind("<Key-Return>",lambda e:login())
		id_entry.bind("<Key-Return>",lambda e:login())
		pw_entry.bind("<Key-Return>",lambda e:login())
		
		exit_btn = Button(self.can2,text="Exit",border=0,highlightthickness=0,
						  relief="flat",fg="red",bg="black",command=self.root.destroy if func_quit == None else func_quit)
		exit_btn.place(relx=0.1,rely=0.9)
		exit_btn.bind("<Enter>",lambda e:exit_btn.config(fg="yellow"))
		exit_btn.bind("<Leave>", lambda e:exit_btn.config(fg="red"))

if __name__ == "__main__":
	from tkinter import Tk
	root = Tk()
	root.attributes("-fullscreen",True)
	a = project_login(root)
	a.draw(lambda:print())
	root.wait_window(a.can)
	try:root.destroy()
	except: pass
	root.mainloop()

