import tkinter as tk               
from tkinter import font  as tkfont 
from tkinter import ttk
import Backend2 as bck
from PIL import Image, ImageTk

class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        #global Variable
        #Background Colour
        self.configure(background='White')
        
        #Create Frame
        frame1 = tk.Frame(self, highlightbackground="black", highlightcolor="black", highlightthickness=1, width=100, bd= 0, bg='black')
        frame1.place(x=240,y=90, width=870,height=420)
        
        #Label Heading 
        lh=tk.Label(self, text="Raco for Warehouses",width=180)
        lh.config(font=("Helvetica", 25),bg='White',anchor='center',fg='black')
        lh.place(x = 250, y = 100, width=850, height=40)

        #Image Logo
        load = Image.open("LOGO.png")
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self, image=render)
        img.image = render
        img.place(x=550, y=150)

        #LABEL 1
        lba = tk.Label(self, text="Enter CSV:",width=90)
        lba.config(font=("Courier", 20),bg='White',anchor='center',fg='black')
        lba.grid(column=0,row=0)
        lba.place(x = 250, y = 370, width=400, height=40)
        
        #Entry of PAT4
        self.e1= tk.Entry(self,width="50")
        self.e1.grid(column=1,row=0)
        self.e1.place(x = 700, y = 370, width=400, height=40)

        #LABEL 2
        lbb = tk.Label(self, text="Enter Date:",width=90)
        lbb.config(font=("Courier", 20),bg='white',anchor='center',fg='black')
        lbb.grid(column=0,row=0)
        lbb.place(x = 250, y = 450, width=400, height=40)
        
        #Entry of PAT4
        self.e2= tk.Entry(self,width="50")
        self.e2.grid(column=1,row=0)
        self.e2.place(x = 700, y = 450, width=400, height=40)
        
        #Button to Submit
        button = tk.Button(self, text="View Map", bg='black',fg="white",command=lambda: bck.Mapping(self.e1.get(),self.e2.get()))
        button.place(x = 500, y =530, width=100, height=50)
        button1 = tk.Button(self, text="Routing Details",bg='black',fg='white',command=lambda: controller.show_frame("PageOne"))
        button1.place(x = 650, y =530, width=100, height=50)
        button2 = tk.Button(self, text="Delivery Details",bg='black',fg='white',command=lambda: controller.show_frame("PageTwo"))
        button2.place(x = 800, y =530, width=100, height=50)
        
        #Clear Input Button
        clear_button = tk.Button(self, text=" Clear Text ", command=self.clear_text,bg='black',fg='white')
        clear_button.place(x = 1050, y = 35, width = 60, height = 40)

    def clear_text(self):
        self.e1.delete(0, 'end')
        self.lbl.place_forget()
        self.lb1.place_forget()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        #global Variable
        #Background Colour
        self.configure(background='White')
        
        #Create Frame
        frame1 = tk.Frame(self, highlightbackground="black", highlightcolor="black", highlightthickness=1, width=100, bd= 0, bg='black')
        frame1.place(x=240,y=80, width=870,height=200)
        
        #Label Heading 
        lh=tk.Label(self, text="Routing Details",width=180)
        lh.config(font=("Helvetica", 25),bg='black',anchor='center',fg='white')
        lh.place(x = 250, y = 90, width=850, height=40)

        #LABEL 1
        lba = tk.Label(self, text="Enter Sales File",width=90)
        lba.config(font=("Courier", 20),bg='black',anchor='center',fg='white')
        lba.grid(column=0,row=0)
        lba.place(x = 250, y = 160, width=400, height=40)
        
        #Entry of PAT4
        self.e1= tk.Entry(self,width="50")
        self.e1.grid(column=1,row=0)
        self.e1.place(x = 700, y = 160, width=400, height=40)
        
        #LABEL 2
        lbb = tk.Label(self, text="Enter Date:",width=90)
        lbb.config(font=("Courier", 20),bg='black',anchor='center',fg='white')
        lbb.grid(column=0,row=0)
        lbb.place(x = 250, y = 220, width=400, height=40)
        
        #Entry of PAT4
        self.e2= tk.Entry(self,width="50")
        self.e2.grid(column=1,row=0)
        self.e2.place(x = 700, y = 220, width=400, height=40)

        '''#declare label
        self.lbn=tk.Label(self,wraplength=700,anchor='w')
        self.lbp=tk.Label(self,wraplength=700,anchor='w')
        #self.lb1=tk.Label(self) '''

        
        self.textn = tk.Text(self)
        
        self.textp = tk.Text(self)
        self.sbn = ttk.Scrollbar(self.textn, orient='vertical')
        self.sbp = ttk.Scrollbar(self.textp, orient='vertical')         
        
        #Button to Submit
        button = tk.Button(self, text="ENTER", fg="white",bg='black',command=lambda: bck.DeliveryDetails(self.e1.get(),self.e2.get(),self.textn,self.textp,self.sbn,self.sbp))
        button.place(x = 550, y =290, width=100, height=50)
        button1 = tk.Button(self, text="START PAGE",fg='white',bg='black',command=lambda: controller.show_frame("StartPage"))
        button1.place(x = 700, y =290, width=100, height=50)
        
        #Clear Input Button
        clear_button = tk.Button(self, text=" Clear Text ", command=self.clear_text,bg='black',fg='white')
        clear_button.place(x = 1050, y = 35, width = 60, height = 40)

    def clear_text(self):
        self.e1.delete(0, 'end')
        self.lbl.place_forget()
        self.lb1.place_forget()
        
class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        
        #Background Colour
        self.configure(background='White')
        
        #Create Frame
        frame1 = tk.Frame(self, highlightbackground="black", highlightcolor="black", highlightthickness=1, width=100, bd= 0, bg='black')
        frame1.place(x=140,y=90, width=520,height=440)
        #Create Frame
        frame2 = tk.Frame(self, highlightbackground="black", highlightcolor="black", highlightthickness=1, width=100, bd= 0, bg='black')
        frame2.place(x=740,y=90, width=520,height=440)
        
        #Label Heading 
        lh=tk.Label(self, text="Send SMS",width=180)
        lh.config(font=("Helvetica", 25),bg='black',anchor='center',fg='white')
        lh.place(x = 150, y = 100, width=500, height=40)
        
        #LABEL 1
        lba = tk.Label(self, text="Enter Mobile Number",width=20)
        lba.config(font=("Courier", 10),bg='black',anchor='center',fg='white')
        lba.grid(column=0,row=0)
        lba.place(x = 150, y = 150, width=200, height=40)
        #Entry of PAT4
        self.e1= tk.Entry(self,width="50")
        self.e1.grid(column=1,row=0)
        self.e1.place(x = 375, y = 150, width=275, height=40)
        #LABEL 2
        lbb = tk.Label(self, text="Enter Message:",width=20)
        lbb.config(font=("Courier", 10),bg='black',anchor='center',fg='white')
        lbb.grid(column=0,row=0)
        lbb.place(x = 150, y = 200, width=200, height=40)
        #Entry of PAT4
        self.e2= tk.Entry(self,width="50")
        self.e2.grid(column=1,row=0)
        self.e2.place(x = 375, y = 200, width=275, height=150)
        send = tk.Button(self, text="Send",bg='White', fg="Black",command=lambda: bck.sendSMS(self.e1.get(),self.e2.get()))
        send.place(x = 300, y = 370, width=100, height=50)
        
        #Label Heading 
        lh=tk.Label(self, text="Live Order Updates",width=180)
        lh.config(font=("Helvetica", 25),bg='black',anchor='center',fg='white')
        lh.place(x = 750, y = 100, width=500, height=40)
        #declare label
        self.lbl=tk.Label(self,wraplength=700)
        self.lb1=tk.Label(self)
        self.lbl.place(x = 750, y = 150, width=500, height=370)
        
   
        #Button to Submit
        button = tk.Button(self, text="Refresh Server",bg='black', fg="white",command=lambda: bck.OpenServer(self.lbl))
        button.place(x = 750, y = 35, width=100, height=50)
        button1 = tk.Button(self, text="Home Page",fg='white', bg='black', command=lambda: controller.show_frame("StartPage"))
        button1.place(x = 550, y = 35, width=100, height=50)
    
        #Clear Input Button
        #clear_button = tk.Button(self, text=" Clear Text ", command=self.clear_text,bg='black',fg='white')
        #clear_button.place(x = 1050, y = 35, width = 60, height = 50)

    def clear_text(self):
        self.e1.delete(0, 'end')
        self.lbl.config(text='')
        self.lbl.place_forget()
        self.lb1.place_forget()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()