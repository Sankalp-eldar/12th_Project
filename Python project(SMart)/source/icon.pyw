from tkinter import Tk,Canvas,Label
from PIL import ImageTk,Image
import pickle,io
with open("resources.pkl","rb") as f:
    op = pickle.load(f)


root= Tk()
w,h = root.winfo_screenwidth(),root.winfo_screenheight()

root.wm_attributes("-topmost",True)
root.wm_attributes("-transparent","green")
root.config(bg="green")
root.geometry("+{}+{}".format((w-300)//2,(h-310)//2))
root.overrideredirect(True)

x = ImageTk.PhotoImage(Image.open(io.BytesIO(op)).resize((300,310)))
can = Canvas(root,width=300,height=310,bg="green",highlightthickness=0)
can.create_image(0,0,anchor='nw',image=x)
can.pack()
Label(root,text="Loading...",bg="Black",fg="Red",font="None 14",width=0,pady=0).pack()
root.after(2000,root.destroy)
root.mainloop()
