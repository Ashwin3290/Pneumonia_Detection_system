from datetime import datetime
from tkinter import *
from PIL import ImageTk,Image
from backend import *
import customtkinter as ck
from tkinter import filedialog as fd        

ck.set_appearance_mode("dark") 
ck.set_default_color_theme("blue")
loc=""
bg_img="images/bg-dark.ppm"
options="Light"
light=Image.open("images/light slide.png")
dark=Image.open("images/dark slide.png")
def pdfsave(frame,loc,name,date,token,pred):
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 20,style="B")
    pdf.set_text_color(255,0,0)
    pdf.cell(200, 10, txt = "Pneumonia Detection System",ln = 1, align = 'C')
    pdf.cell(200, 10, txt = "Report",ln = 2, align = 'C')

    pdf.set_text_color(0,0,0)
    pdf.set_font("Times", size = 20,style="B")
    pdf.cell(200,10,txt="Name of patient: "+name,ln=2,align="L")
    pdf.cell(200,10,txt="Date of Diagnosis: "+date,ln=2,align="L")
    pdf.cell(200,10,txt="Token Number: "+str(token),ln=2,align="L")
    pdf.cell(200,10,txt="Prediction: "+pred,ln=2,align="L")
    pdf.image(loc, x = 0, y = 100, w = 150, h = 150)
    dest=fd.askdirectory(title = "Select Folder to open")
    dest+="/"+name+"_"+str(token)+".pdf"
    pdf.output(dest,"f") 
    



def output(frame,img,name,date,token,pred,backloc):

    frame.destroy()
    frame=ck.CTkFrame(master=root,height=533,width=800)
    frame.pack()
    bg=PhotoImage(file=bg_img)
    background=ck.CTkLabel(master=frame,image=bg)
    background.pack()
    
    x_ray=ImageTk.PhotoImage(img.resize((300,300)))
    picture=ck.CTkLabel(master=frame,image=x_ray)
    picture.place(relx=.5,rely=.5,x=-300,y=-100,anchor=CENTER)
    x=-50
    y=-80

    #Widgets
    name_Label=ck.CTkLabel(master=frame,text="Name of patient")
    name_Label.place(relx=.5,rely=.5,anchor=CENTER,x=x,y=y)
    date_Label=ck.CTkLabel(master=frame,text="Date of diagnosis")
    date_Label.place(relx=.5,rely=.5,anchor=CENTER,x=x,y=y+50)
    token_Label=ck.CTkLabel(master=frame,text="Token Number")
    token_Label.place(relx=.5,rely=.5,anchor=CENTER,x=x,y=y+100)
    pred_Label=ck.CTkLabel(master=frame,text="Prediction")
    pred_Label.place(relx=.5,rely=.5,anchor=CENTER,x=x,y=y+150)

    name_info=ck.CTkLabel(master=frame,text=name)
    name_info.place(relx=.5,rely=.5,anchor=CENTER,x=x+150,y=y)
    date_info=ck.CTkLabel(master=frame,text=date)
    date_info.place(relx=.5,rely=.5,anchor=CENTER,x=x+150,y=y+50)
    token_info=ck.CTkLabel(master=frame,text=token)
    token_info.place(relx=.5,rely=.5,anchor=CENTER,x=x+150,y=y+100)
    pred_info=ck.CTkLabel(master=frame,text=pred)
    pred_info.place(relx=.5,rely=.5,anchor=CENTER,x=x+150,y=y+150)

    save=ck.CTkButton(master=frame,text="Save report",command=lambda:pdfsave(frame,loc,name,date,token,pred))
    save.place(relx=.5,rely=.5,anchor=CENTER,x=0,y=150)
    back_button=ck.CTkButton(master=frame,text="Back",command=lambda:back(frame,backloc))
    back_button.place(relx=.5,rely=.5,anchor=CENTER,x=300,y=200)
    root.mainloop()

def back(frame,backloc):
    frame.destroy()
    if backloc=="welcome":
        next=welcome()
        next.screen()
    elif backloc=="check":
        next=check()
        next.screen()


class welcome():

    def screen(self):
        super()
        global bg_img,options
        self.frame=ck.CTkFrame(master=root,height=533,width=800)
        self.frame.pack()
        bg=PhotoImage(file=bg_img)
        self.background=ck.CTkLabel(master=self.frame,image=bg)
        self.background.pack()
        
        
        #Widgets
        check = ck.CTkButton(master=self.frame, text="Check patient details",command=lambda:self.call_check())
        check.place(relx=.5,rely=.5,anchor=CENTER,x=-120,y=60)
        pred = ck.CTkButton(master=self.frame, text="Get prediction",command=lambda:self.call_Prediction())
        pred.place(relx=.5,rely=.5,anchor=CENTER,x=120,y=60)
        quit = ck.CTkButton(master=self.frame, text="Quit",command=lambda:exit())
        quit.place(relx=.5,rely=.5,anchor=CENTER,x=0,y=120)
        optionmenu_1 = ck.CTkButton(master=self.frame,text=options+" Mode",command=self.change_appearance_mode)
        optionmenu_1.place(x=10, y=450)
        root.mainloop()

    def change_appearance_mode(self):
        global bg_img,options,button_ico,button_color
        if options=="Light":
            bg_img="images/bg-light.ppm"
            ck.set_appearance_mode(options)
            options="Dark"
            
            ck.set_default_color_theme("green")
        elif options=="Dark":
            bg_img="images/bg-dark.ppm"
            ck.set_appearance_mode(options)
            options="Light"
            button_ico=dark
            button_color="black"
            ck.set_default_color_theme("blue")
        
        self.frame.destroy()
        load=welcome()
        load.screen()

    def call_Prediction(self):
        self.frame.destroy()
        next=prediction()
        next.screen()

    def call_check(self):
        self.frame.destroy()
        next=check()
        next.screen() 
    

class prediction():
    
    def screen(self):
        global bg_img
        self.frame=ck.CTkFrame(master=root,height=533,width=800)
        self.frame.pack()
        bg=PhotoImage(file=bg_img)
        background=ck.CTkLabel(master=self.frame,image=bg)
        background.pack()
        

        #Widgets
        name_var=StringVar()
        entry_1 = ck.CTkEntry(master=self.frame,textvariable=name_var)
        entry_1.place(relx=.5,rely=.5,anchor=CENTER,x=60,y=0)
        name_label=ck.CTkLabel(master=self.frame,text="Name of patient")
        name_label.place(relx=.5,rely=.5,anchor=CENTER,x=-90,y=0)
        open = ck.CTkButton(master=self.frame, text="Upload x-ray",command=self.getfile)
        open.place(relx=.5,rely=.5,anchor=CENTER,x=0,y=60)
        self.process=ck.CTkButton(master=self.frame,text="Proceed",command=lambda:self.proceed(name_var))
        self.process.place(relx=.5,rely=.5,anchor=CENTER,x=0,y=100)
        self.process.configure(state=DISABLED)
        back_button=ck.CTkButton(master=self.frame,text="Back",command=self.back)
        back_button.place(relx=.5,rely=.5,anchor=CENTER,x=300,y=200)
        optionmenu_1 = ck.CTkButton(master=self.frame,text=options+" Mode",command=self.change_appearance_mode)
        optionmenu_1.place(x=10, y=450)
        root.mainloop()

    def proceed(self,name_var):
        import random
        username=name_var.get()
        token=random.randint(0,99999)
        if not verify(token):
            token=random.randint(0,99999)
        date=datetime.now().strftime("%Y-%m-%d")
        img=Image.open(loc)
        pred=predict(loc)
        add(username,token,date,loc,pred)
        output(self.frame,img,username,date,token,pred,"welcome")
        
    def back(self):
        self.frame.destroy()
        next=welcome()
        next.screen()
        
    def getfile(self):                   
        the_file = fd.askopenfilename(  
        title = "Select a file of any type",  
        filetypes = [("jpg file", "*.jpeg*"),("png file", "*.png*"),("All file", "*.*")]  
        )  
        global loc
        loc=the_file
        img=Image.open(loc)
        x_ray=ImageTk.PhotoImage(img.resize((200,200)))
        picture=ck.CTkLabel(master=self.frame,image=x_ray)
        picture.place(relx=0,rely=0,anchor=NW)
        self.process.configure(state=NORMAL)
        root.mainloop()
    

    def change_appearance_mode(self):
        global bg_img,options,button_ico,button_color
        if options=="Light":
            bg_img="images/bg-light.ppm"
            ck.set_appearance_mode(options)
            options="Dark"
            
            ck.set_default_color_theme("green")
        elif options=="Dark":
            bg_img="images/bg-dark.ppm"
            ck.set_appearance_mode(options)
            options="Light"
            button_ico=dark
            button_color="black"
            ck.set_default_color_theme("blue")
        self.frame.destroy()
        load=prediction()
        load.screen()

class check():

    def screen(self):
        global bg_img,options
        self.frame=ck.CTkFrame(master=root,height=533,width=800)
        self.frame.pack()
        bg=PhotoImage(file=bg_img)
        background=ck.CTkLabel(master=self.frame,image=bg)
        background.pack()
        

        #Widgets
        option=ck.CTkLabel(master=self.frame,text="Enter details in one of the following and search")
        option.place(relx=.5,rely=.5,anchor=CENTER,x=0,y=-50)

        name_var=StringVar()
        entry_1 = ck.CTkEntry(master=self.frame,textvariable=name_var)
        entry_1.place(relx=.5,rely=.5,anchor=CENTER,x=60,y=0)
        name_label=ck.CTkLabel(master=self.frame,text="Name of patient")
        name_label.place(relx=.5,rely=.5,anchor=CENTER,x=-90,y=0)

        token_var=StringVar()
        entry_2 = ck.CTkEntry(master=self.frame,textvariable=token_var)
        entry_2.place(relx=.5,rely=.5,anchor=CENTER,x=60,y=60)
        name_label=ck.CTkLabel(master=self.frame,text="Token number")
        name_label.place(relx=.5,rely=.5,anchor=CENTER,x=-90,y=60)

        search_it=ck.CTkButton(master=self.frame,text="Search",command=lambda:self.search(token_var,name_var))
        search_it.place(relx=.5,rely=.5,anchor=CENTER,x=0,y=120)

        back_button=ck.CTkButton(master=self.frame,text="Back",command=self.back)
        back_button.place(relx=.5,rely=.5,anchor=CENTER,x=300,y=200)
        optionmenu_1 = ck.CTkButton(master=self.frame,text=options+" Mode",command=self.change_appearance_mode)
        optionmenu_1.place(x=10, y=450)
        root.mainloop()

    def back(self):
        self.frame.destroy()
        next=welcome()
        next.screen()
    
    def search(self,token_var,name_var):
        name=name_var.get()
        token=token_var.get()
        data,decide=searchindata(name,token)
        if data:
            if decide=="single":
                image=Image.open(data[3])
                output(self.frame,image,data[0],data[2],data[1],data[4],"check")
            if decide=="multiple":
                self.multiple_options(data)

        else:
            warning=ck.CTkLabel(master=self.frame,text="No Data found",text_color="red",text_font=("",15))
            warning.place(relx=.5,rely=.5,anchor=CENTER,x=-50,y=200)
            root.mainloop()
    
    def send_to_output(self,data):
        image=Image.open(data[3])
        output(self.frame,image,data[0],data[1],data[2],data[4],"check")


    def multiple_options(self,data):
        self.frame.destroy()
        v = StringVar(self.frame,"0")
        global bg_img
        self.frame=ck.CTkFrame(master=root,height=533,width=800)
        self.frame.pack()
        bg=PhotoImage(file=bg_img)
        background=ck.CTkLabel(master=self.frame,image=bg)
        background.pack()

        values = {}
        for i in data:
            key=i[0]+" "+str(i[1])+" "+str(i[2])
            values[key]=data.index(i)
        x=0
        y=-100
        for (text, value) in values.items():
            ck.CTkRadioButton(master=self.frame, text = text, variable = v,
                value = value).place(relx=.5,rely=.5,anchor=CENTER,x=x,y=y)
            y+=30

        proceed=ck.CTkButton(master=self.frame,text="Select",command=lambda:self.proceed(v,data))
        proceed.place(relx=0.5,rely=0.5,anchor=CENTER,x=0,y=230)

        root.mainloop()

    def proceed(self,v,data):
        index=int(v.get())
        send=data[index]
        self.send_to_output(send)


    def change_appearance_mode(self):
        global bg_img,options
        if options=="Light":
            bg_img="images/bg-light.ppm"
            ck.set_appearance_mode(options)
            options="Dark"
            ck.set_default_color_theme("green")
        elif options=="Dark":
            bg_img="images/bg-dark.ppm"
            ck.set_appearance_mode(options)
            options="Light"
            button_ico=dark
            button_color="black"
            ck.set_default_color_theme("blue")
        self.frame.destroy()
        load=check()
        load.screen()

#Main
root=ck.CTk()
root.geometry("800x533+200+40")
root.title(string='Pneuemonia Detection')
root.resizable(FALSE,FALSE)
w=welcome()
w.screen()