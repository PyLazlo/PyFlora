import customtkinter as ctk
import tkinter as tk
from .database import Database_repo, connect_repo_to_db, User, Plant, Pot
from .sensors import RaspberryPiSim
from tkinter import filedialog
import os
from .image_control import copy_image, open_image
from .pot_control import pot_status
from .graph import make_data_frame, plot_graph


class PyFlora(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PyFlora App")
        self.geometry('1200x980')
        self.minsize(800,600)

        #Initialize Log in Menu
        self.menu = LoginMenuFrame(self)
        self.menu.pack(expand=True, fill='both')
       
        #Make a connection to the Database       
        self.repo = connect_repo_to_db()

                
        self.mainloop()

    def clear_frame(self):
        """
        Class method used for deleting widgets before placing new ones
        """
        for widget in self.winfo_children():
            widget.destroy()

    def draw_signup_menu(self):
        """
        Class method used to draw the Sign Up menu
        """
        self.clear_frame()
        SignUpFrame(self)

    def draw_login_menu(self):
        """
        Class method used to draw the Log In menu
        """
        self.clear_frame()
        LoginMenuFrame(self)

    def draw_main_menu(self):
        """
        Class method used for drawing the Main menu after a successful log in.
        Also draws the welcome message
        """
        self.clear_frame()
        MenuFrame(self)
        
        # Welcome message part
        user_name = self.repo.get_user_by_userid(self.user_id)

        self.txt = f"Welcome to PyFlora {user_name.name} {user_name.surname}!!!"
        # Create label
        self.lbl = tk.Label(self, font='Bell 36 bold', width=len(self.txt))
        self.lbl.pack(pady=5, anchor=tk.CENTER)
        # Function that runs after every 50ms
        self.after(50, self.animate_label, self.txt)

    def animate_label(self, text, n=0):
        """
        Method for animating the label
        """
        if n < len(text)-1:
            # not complete yet, schedule next run one second later
            self.lbl.after(50, self.animate_label, text, n+1)
        # update the text of the label
        self.lbl['text'] = text[:n+1]

    
    def main_log_in(self, user, pword):
        """
        Main log in logic.
        """
        
        username = self.repo.get_user_by_username(user)

        if username is None:
            print("Username does not exist")
        elif username.password != pword:
            print("Wrong password")
        elif username.username == user and username.password == pword:
            self.user_id = username.id
            #print(self.repo.get_all_pots(self.user_id))

            #if user has no pots, create one
            if self.repo.get_a_pot(self.user_id) is None:
                
                pot = Pot()
                pot.name = "Name"
                pot.location = "Location"
                pot.plant_id = None
                pot.user_id = self.user_id
                self.repo.create_pot(pot=pot, user_id=self.user_id)
            
            self.draw_main_menu()
    
    def update_profile(self, user):
        self.repo.update_user(user= user)

    def main_sign_up(self, user, password, name, surname):

        #check if username already exists in database, if not, create it.
        username = self.repo.get_user_by_username(user)
        if username is None:
            new_user = User(username=user, password= password, name = name, surname= surname)
            self.repo.create_user(new_user)
            
        else:
            print("Username already exists.")
        self.clear_frame()
        LoginMenuFrame(self)

    def draw_plants_frame(self):
        print("Ok")
        self.clear_frame()
        MenuFrame(self)
        PlantsFrame(self)

    def add_a_plant(self):
        PlantCreateFrame(self).attributes('-topmost', 'true')

    def plant_to_database(self, plant:Plant):
        self.repo.create_plant(plant)

    def delete_plant(self, plant):
        self.repo.delete_plant(plant)

    def draw_my_profile(self):
        self.clear_frame()
        MenuFrame(self)
        My_Profile(self)
        

    def draw_pots_frame(self):
        self.clear_frame()
        MenuFrame(self)
        PotsFrame(self)

    def delete_pot(self, pot):
        self.repo.delete_pot(pot)
    
    def add_data(self, data):
        self.repo.create_data(data=data)

    def get_data(self, pot, plant):
        data= self.repo.get_all_data(pot=pot, plant=plant)
        return data

        
        

class LoginMenuFrame(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)
        
        
        self.username = ctk.CTkEntry(master= self,
                               placeholder_text="Username",
                               width=120,
                               height=25,
                               border_width=2,
                               corner_radius=10)
        self.username.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.password = ctk.CTkEntry(master= self,
                               placeholder_text="Password",
                               show="*",
                               width=120,
                               height=25,
                               border_width=2,
                               corner_radius=10)
        self.password.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        login_button = ctk.CTkButton(master= self,
                                 width=120,
                                 height=32,
                                 border_width=0,
                                 corner_radius=8,
                                 text="Log In",
                                 command= lambda: parent.main_log_in(user=self.username.get(), pword=self.password.get()))                  #### self.log_in(parent) - for passing parent class method in to child class method
        login_button.place(relx=0.4, rely=0.7, anchor=tk.CENTER)

        signup_button = ctk.CTkButton(master= self,
                                 width=120,
                                 height=32,
                                 border_width=0,
                                 corner_radius=8,
                                 text="Sign Up",
                                 command= parent.draw_signup_menu)
        signup_button.place(relx=0.6, rely=0.7, anchor=tk.CENTER)
        
        self.pack(expand=True, fill='both')
    



class SignUpFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        
        self.username = ctk.CTkEntry(master= self,
                               placeholder_text="Username",
                               width=120,
                               height=25,
                               border_width=2,
                               corner_radius=10)
        self.username.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        self.password = ctk.CTkEntry(master= self,
                               placeholder_text="Password",
                               show="*",
                               width=120,
                               height=25,
                               border_width=2,
                               corner_radius=10)
        self.password.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        self.fname = ctk.CTkEntry(master= self,
                               placeholder_text="First Name",
                               width=120,
                               height=25,
                               border_width=2,
                               corner_radius=10)
        self.fname.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        self.surname = ctk.CTkEntry(master= self,
                               placeholder_text="Surname",
                               width=120,
                               height=25,
                               border_width=2,
                               corner_radius=10)
        self.surname.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.signup_button = ctk.CTkButton(master= self,
                                 width=120,
                                 height=32,
                                 border_width=0,
                                 corner_radius=8,
                                 text="Sign Up",
                                 command= lambda: parent.main_sign_up(user=self.username.get(), 
                                                                        password=self.password.get(), 
                                                                        name=self.fname.get(), 
                                                                        surname=self.surname.get()))
        self.signup_button.place(relx=0.6, rely=0.6, anchor=tk.CENTER)

        self.back_button = ctk.CTkButton(master= self, 
                                width=120,
                                height=32,
                                border_width=0,
                                corner_radius=8,
                                text="Back",
                                command= parent.draw_login_menu)
        self.back_button.place(relx=0.4, rely=0.6, anchor=tk.CENTER)
        
        self.pack(expand=True, fill = 'both')
        



class MenuFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        profile_button = ctk.CTkButton(master= self,
                                    width=120,
                                    height=32,
                                    border_width=0,
                                    corner_radius=8,
                                    text="My Profile",
                                    command= parent.draw_my_profile)          #complete
        profile_button.place(relx=0, rely=0.1, anchor=tk.W)

        pots_button = ctk.CTkButton(master= self,
                                    width=120,
                                    height=32,
                                    border_width=0,
                                    corner_radius=8,
                                    text="My Pots",
                                    command= parent.draw_pots_frame)        #complete
        pots_button.place(relx=0, rely=0.2, anchor=tk.W)

        plants_button = ctk.CTkButton(master= self,
                                    width=120,
                                    height=32,
                                    border_width=0,
                                    corner_radius=8,
                                    text="My Plants",
                                    command= parent.draw_plants_frame)
        
        plants_button.place(relx=0, rely=0.3, anchor=tk.W)

        self.pack(side = tk.LEFT, fill = "y")



class My_Profile(SignUpFrame):                                         
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.user = self.parent.repo.get_user_by_userid(self.parent.user_id)

        self.signup_button.destroy()
        self.back_button.destroy()
        
        self.fname.grid(row=2, column=2)

        self.fname_label= ctk.CTkLabel(self, text="First Name").grid(row=2, column=1)
        
        self.surname.grid(row=3, column=2)
        self.surname_label= ctk.CTkLabel(self, text="Surname").grid(row=3, column=1)
        
        self.username.grid(row=4, column=2)
        self.username_label= ctk.CTkLabel(self, text="Username").grid(row=4, column=1)

        self.password.grid(row=5, column=2)
        self.password_label= ctk.CTkLabel(self, text="Password").grid(row=5, column=1)
        self.new_password = ctk.CTkEntry(master= self,
                               placeholder_text="New Password",
                               show="*",
                               width=120,
                               height=25,
                               border_width=2,
                               corner_radius=10)
        self.new_password.grid(row=6, column=2)
        self.new_passwpord_label= ctk.CTkLabel(self, text="New Password").grid(row=6, column=1)

        self.confirm_password = ctk.CTkEntry(master= self,
                               placeholder_text="Confirm Password",
                               show="*",
                               width=120,
                               height=25,
                               border_width=2,
                               corner_radius=10)
        self.confirm_password.grid(row=7, column=2)
        self.confirm_password_label= ctk.CTkLabel(self, text="Confirm Password").grid(row=7, column=1)

        self.update_button = ctk.CTkButton(master= self,
                                            width= 120,
                                            height= 32,
                                            border_width= 0,
                                            corner_radius= 8,
                                            text= "Update information",
                                            command= self.update_profile)
        
        self.update_button.grid(row=8, column=2)

        ################# INSERT VALUES ###################
        self.username.insert(0, self.user.username)
        self.fname.insert(0, self.user.name)
        self.surname.insert(0, self.user.surname)
        self.place(relx=0.5, rely=0.2)
        #self.pack(expand=True, fill = 'both',)


        ############################################### INSERT VALUES INTO ENTRY FIELDS #####################################################
        
    def update_profile(self):
        pw = self.password.get()
        npw = self.new_password.get()
        cpw = self.confirm_password.get()
        fname = self.fname.get()
        surname = self.surname.get()
        username = self.username.get()
        user = self.parent.repo.get_user_by_userid(self.parent.user_id)
        nusername = self.parent.repo.get_user_by_username(username)
        
        
        
        if nusername is not None and nusername.username != self.user.username:
            return print("Username already exists")
        
        # with new password
        if npw == cpw and user.password == pw and npw !="":
            user.name = fname
            user.surname = surname
            user.password = npw
            user.username = username
            updated_user = user
            self.parent.update_profile(updated_user)
            print("Information updated")

        # without new password
        elif npw == cpw and user.password == pw:
            user.name = fname
            user.surname = surname
            updated_user = user
            self.parent.update_profile(updated_user)
            print("Information updated")


            ######################################################## 

        else:
            return print("Wrong password or bad confirm password.")
        self.parent.draw_my_profile()




class PotsFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.label = ctk.CTkLabel(self, text= "Pots").grid(row=0, column=0)
        self.pots = parent.repo.get_all_pots(user_id = parent.user_id) 
        self.parent = parent
        
        self.repo = parent.repo

        self.list =[]

        ######################################################## MAYBE ADD GRID PLACEMENT
        add_pot_button = ctk.CTkButton(master= self,
                                            width= 120,
                                            height= 32,
                                            border_width= 0,
                                            corner_radius= 8,
                                            text= "Add a Pot",
                                            command= lambda: PotCreate(parent=self).attributes('-topmost', 'true')).grid(row=1, column=1)
        show_empty_pots_button = ctk.CTkButton(master= self,
                                            width= 120,
                                            height= 32,
                                            border_width= 0,
                                            corner_radius= 8,
                                            text= "Show Empty Pots",
                                            command= lambda: PotsEmptyFrame(parent=self).attributes('-topmost', 'true')).grid(row=1, column=2)
        
        sync_data_button = ctk.CTkButton(master= self,
                                            width= 120,
                                            height= 32,
                                            border_width= 0,
                                            corner_radius= 8,
                                            text= "Sync Data",
                                            command= parent.draw_pots_frame).grid(row=1, column=3)
        i=1
        j=0
        for pot in self.pots:
            if pot.plant_id is not None:
                
                if j==0:

                    pot_object = PotInfo(self, pot=pot, plant=parent.repo.get_plant_by_id(pot.plant_id))  #, data=self.sensor.send_data(pot_id=pot.id
                    pot_object.grid(row=2+i, column=j, columnspan=3)
                    self.grid_columnconfigure(j, weight=1)
                    self.list.append(pot_object)
                    j=4
                else:
                    
                    pot_object = PotInfo(self, pot=pot, plant=parent.repo.get_plant_by_id(pot.plant_id))
                    pot_object.grid(row=2+i, column=j, columnspan=3)
                    self.grid_columnconfigure(j, weight=1)
                    self.list.append(pot_object)
                    i+=1
                    j=0
                 ########################## DATA
        
       
        

        self.pack(expand=True, fill= 'both')

        
class PotInfo(ctk.CTkFrame):
    def __init__(self, parent, pot, plant):
        super().__init__(parent, border_color="black", border_width=2)
        self.parent = parent
        self.pot = pot
        self.plant = plant
        self.sensor = RaspberryPiSim()   
        self.data = self.sensor.send_data(self.pot.id, self.plant.id)
        self.status_message = pot_status(plant=self.plant, data=self.data)
        
        #print(self.data)
        #print(self.data.sen_temp, self.data.sen_hydration, self.data.pot_id)

        self.image_button = ctk.CTkButton(master= self,
                                    width= 120,
                                    height= 120,
                                    border_width= 0,
                                    corner_radius= 8,
                                    text="",
                                    image= ctk.CTkImage(open_image(self.plant.photo), size=(120,120)),
                                    command= None).grid(row= 0, column= 1)
            
        
        self.name_label = ctk.CTkLabel(self, text=f"Pot Name: {self.pot.name}\n"
                                        + f"Pot Location: {self.pot.location}\n\n"
                                        + f"Plant ID/Name: {self.pot.plant_id}/{self.plant.name}\n\n"
                                        + f"Temperature from Internet: {self.data.api_temp} \u2103\n\n"
                                        + f"Temperature sensor: {self.data.sen_temp} \u2103\n"
                                        + f"Hydration sensor: {self.data.sen_hydration}%\n"
                                        + f"pH sensor: {self.data.sen_pH}\n"
                                        + f"Light sensor: {self.data.sen_light}\n"
                                        + f"Time: {self.data.sen_date.strftime('%d.%m.%Y. %H:%M:%S')}")
        self.name_label.grid(row=1, column= 1)
        
        
        self.button_pie = ctk.CTkButton(master= self,
                                    width= 60,
                                    height= 32,
                                    border_width= 0,
                                    corner_radius= 8,
                                    text= f"Pie Chart",
                                    command= lambda: plot_graph(df=make_data_frame(self.parent.parent.get_data(self.pot, self.plant)), plot_type="pie")).grid(row= 8, column= 0)
        
        self.button_histo = ctk.CTkButton(master= self,
                                    width= 60,
                                    height= 32,
                                    border_width= 0,
                                    corner_radius= 8,
                                    text= f"Histogram",
                                    command= lambda: plot_graph(df=make_data_frame(self.parent.parent.get_data(self.pot, self.plant)), plot_type="bar")).grid(row= 8, column= 1)
        
        self.button_line = ctk.CTkButton(master= self,
                                    width= 60,
                                    height= 32,
                                    border_width= 0,
                                    corner_radius= 8,
                                    text= f"Line Chart",
                                    command= lambda: plot_graph(df=make_data_frame(self.parent.parent.get_data(self.pot, self.plant)), plot_type="line")).grid(row= 8, column= 2)

        self.status = ctk.CTkTextbox(master= self,
                                    width=420,
                                    height=90,
                                    border_width=2,
                                    corner_radius=10)                                      
        self.status.grid(row=9, column=0, columnspan=3)
        self.status.insert("0.0", self.status_message)
        
        #print(self.status.get("0.0", "end-1c"))

        self.edit_button = ctk.CTkButton(master= self,
                                width= 120,
                                height= 32,
                                border_width= 0,
                                corner_radius= 8,
                                text= "Edit this pot",
                                command= lambda: PotEdit(parent=self.parent, pot=self.pot, plant= self.plant.name).attributes('-topmost', 'true')).grid(row= 10, column= 1)
        
        
    ########################################################################################### 
       

        self.grid(column=0, row=0, sticky=tk.N+tk.S+tk.E+tk.W) ######################################### 
        
        self.data_to_database()

    def data_to_database(self):
        self.parent.parent.add_data(self.data)


class PotsEmptyFrame(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("560x480")
        self.title("PyFlora App - List of Empty Pots")
        self.label = ctk.CTkLabel(self, text= "Empty Pots").grid(row=0, column=0)
        self.pots = parent.parent.repo.get_all_pots(user_id = parent.parent.user_id) 
        self.parent = parent
        self.sensor = RaspberryPiSim()
        self.repo = parent.repo

        ######################################################## 
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.repo = self.repo
        self.scrollable_frame.parent = self.parent.parent
        self.scrollable_frame.pots = self.pots
        self.scrollable_frame.grid(column=0, row=0, sticky="nsew")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        i=1
        j=0
        for pot in self.pots:
            if pot.plant_id is None:
                

                if j==0:

                    PotInfoEmpty(self.scrollable_frame, pot=pot).grid(row=2+i, column=j)
                    j=1
                else:
                    
                    PotInfoEmpty(self.scrollable_frame, pot=pot).grid(row=2+i, column=j) 
                    i+=1
                    j=0
                



class PotInfoEmpty(ctk.CTkFrame):
    def __init__(self, parent, pot):
        super().__init__(parent, border_color="black", border_width=2)
        self.parent = parent
        self.pot = pot
     

        
        self.name = ctk.CTkEntry(master= self,
                            placeholder_text="Pot name",
                            width=120,
                            height=25,
                            border_width=2,
                            corner_radius=10)
        self.name.grid(row=0, column=1)
        self.name_label = ctk.CTkLabel(self, text="Pot name")
        self.name_label.grid(row=0, column=0)
        self.name.insert(0, self.pot.name)
        self.location = ctk.CTkEntry(master= self,
                            placeholder_text="Pot Location",
                            width=120,
                            height=25,
                            border_width=2,
                            corner_radius=10)
        self.location.grid(row=1, column=1)
        self.location_label = ctk.CTkLabel(self, text="Pot Location")
        self.location_label.grid(row=1, column=0)
        self.location.insert(0, self.pot.location)

        self.status = ctk.CTkLabel(master= self,text= "Status: Empty pot")
        self.status.grid(row=2, column=0)

        self.edit_button = ctk.CTkButton(master= self,
                                width= 120,
                                height= 32,
                                border_width= 0,
                                corner_radius= 8,
                                text= "Edit this pot",
                                command= lambda: PotEdit(parent=self.parent, pot=self.pot, plant=None).attributes('-topmost', 'true')).grid(row=3, column=0)
            
        self.grid(column=0, row=0, sticky=tk.N+tk.S+tk.E+tk.W)

            

class PotCreate(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("720x480")
        self.title("PyFlora App - Create a Pot")
        self.parent = parent
        self.plants = parent.repo.get_all_plants()
        plant_list = [plant.name for plant in self.plants]
        plant_list.insert(0, "None")
        self.label = ctk.CTkLabel(self, text="Create a New Pot")
        self.label.grid(row=0, column=0)

        self.name = ctk.CTkEntry(master= self,
                               placeholder_text="Pot name",
                               width=120,
                               height=25,
                               border_width=2,
                               corner_radius=10)
        self.name.grid(row=2, column=0)
        self.name_label = ctk.CTkLabel(self, text="Pot name").grid(row=1, column=0)
        self.location = ctk.CTkEntry(master= self,
                            placeholder_text="Pot Location",
                            width=120,
                            height=25,
                            border_width=2,
                            corner_radius=10)
        self.location.grid(row=4, column=0)
        self.location_label = ctk.CTkLabel(self, text="Pot Location").grid(row=3, column=0)
        self.plant_id = ctk.CTkOptionMenu(master= self,
                                       values=plant_list,
                                       command=None)
        self.plant_id.grid(row=6, column=0)
        self.plant_id_label = ctk.CTkLabel(self, text="Plant in Pot").grid(row=5, column=0)

        self.create_button = ctk.CTkButton(master= self,
                                    width= 120,
                                    height= 32,
                                    border_width= 0,
                                    corner_radius= 8,
                                    text= "Create this pot",
                                    command= lambda: self.create_a_pot(self.parent))
        self.create_button.grid(row=7, column=0)
        self.grid_columnconfigure(0, weight=1)
        #print(plant_list)
        
        

    def create_a_pot(self, parent):
        plant_name = self.plant_id.get()
        plant = parent.repo.get_plant_by_name(plant_name)
        if plant is not None:
            plant_id = plant.id
        else:
            plant_id = None
        pot = Pot(name = self.name.get(), location = self.location.get(), plant_id = plant_id)
        parent.repo.create_pot(pot, parent.parent.user_id)
        parent.parent.draw_pots_frame()



class PotEdit(PotCreate):
    def __init__(self, parent, pot, plant):
        super().__init__(parent)
        self.title("PyFlora App - Edit a Pot")
        self.parent = parent
        self.pot = pot
        self.plant_name = plant
        
        self.label.destroy()
        self.label = ctk.CTkLabel(self, text="Edit this Pot").grid(row=0, column=0)
        self.create_button.destroy()
        self.name.insert(0, self.pot.name)
        self.location.insert(0, self.pot.location)

        self.save_button = ctk.CTkButton(master= self,
                                    width= 120,
                                    height= 32,
                                    border_width= 0,
                                    corner_radius= 8,
                                    text= "Save changes",
                                    command= self.update_pot).grid(row=7, column=0)

        self.delete_button = ctk.CTkButton(master= self,
                                    width= 120,
                                    height= 32,
                                    border_width= 0,
                                    corner_radius= 8,
                                    text= "Delete this pot",
                                    command= self.delete_pot).grid(row=8, column=0)
        

        self.plant_id.set(self.plant_name)


    def delete_pot(self):
        self.parent.parent.delete_pot(self.pot)
        self.parent.parent.draw_pots_frame()

    def update_pot(self):
        
        plant_name = self.plant_id.get()
        plant_id = self.parent.repo.get_plant_by_name(plant_name)

        if plant_id == None:
            self.pot.plant_id = None
        else:
            self.pot.plant_id = plant_id.id

        self.pot.name= self.name.get()
        self.pot.location = self.location.get()
        self.pot.user_id = self.pot.user_id
        self.parent.repo.update_pot(self.pot)
        self.parent.parent.clear_frame()
        self.parent.parent.draw_pots_frame()



class PlantsFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.label = ctk.CTkLabel(self, text= "Label").grid(row=0, column=0)
        self.plants = parent.repo.get_all_plants()
        self.parent = parent

        add_plant_button = ctk.CTkButton(master= self,
                                            width= 120,
                                            height= 32,
                                            border_width= 0,
                                            corner_radius= 8,
                                            text= "Add Plant",
                                            command=  parent.add_a_plant).grid(row=1, column=0)
        i=2
        j=0
        for plant in self.plants:
           if j==0:
                ctk.CTkButton(master= self,
                                width= 300,
                                height= 120,
                                border_width= 0,
                                corner_radius= 8,
                                image= ctk.CTkImage(open_image(plant.photo), size=(120,120)),
                                text= f"{plant.id}: {plant.name}",
                                command= lambda plant=plant: self.create_plant_edit_frame(plant)).grid(row=2+i, column=j)
                j=1
           else:
               ctk.CTkButton(master= self,
                            width= 300,
                            height= 120,
                            border_width= 0,
                            corner_radius= 8,
                            image= ctk.CTkImage(open_image(plant.photo), size=(120,120)),
                            text= f"{plant.id}: {plant.name}",
                            command= lambda plant=plant: self.create_plant_edit_frame(plant)).grid(row=2+i, column=j)
               i+=1
               j=0
       
        
            
        self.pack(expand=True, fill= 'both')
    def create_plant_edit_frame(self, plant):
        PlantEditFrame(self.parent, plant).attributes('-topmost', 'true')

    

class PlantCreateFrame(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("PyFlora App - Add a Plant")
                
        self.name = ctk.CTkEntry(master= self,
                               placeholder_text="Plant name",
                               width=120,
                               height=25,
                               border_width=2,
                               corner_radius=10)
        self.name.grid(row=1, column=1)
        self.name_label = ctk.CTkLabel(self, text="Plant name")
        self.name_label.grid(row=1, column=0)
        self.about = ctk.CTkTextbox(master= self,
                                    width=120,
                                    height=75,
                                    border_width=2,
                                    corner_radius=10)
        self.about.grid(row=2, column=1)
        self.about_label = ctk.CTkLabel(self, text="About")
        self.about_label.grid(row=2, column=0)
        
        self.photo_path = ctk.CTkButton(master= self,
                               width=120,
                               height=25,
                               border_width=2,
                               corner_radius=10,
                               text = "Photo path",
                               command= self.photo_path_fun) #self.photo_path_fun
        self.photo_path.grid(row=3, column=1)
        self.photo_path_label = ctk.CTkLabel(self, text="Photo path")
        self.photo_path_label.grid(row=3, column=0)
        
        self.hydration = ctk.CTkOptionMenu(master= self,
                                       values=["Low", "Mid", "High"],
                                       command=None)
        self.hydration.grid(row=4, column=1)
        self.hydration_label = ctk.CTkLabel(self, text="Hydration")
        self.hydration_label.grid(row=4, column=0)
        self.hydration.set("Low")  # set initial value
        
        self.light = ctk.CTkOptionMenu(master= self,
                                       values=["Low", "Mid", "High"],
                                       command=None)
        self.light.grid(row=5, column=1)
        self.light_label = ctk.CTkLabel(self, text="Light")
        self.light_label.grid(row=5, column=0)
        self.light.set("Low")  # set initial value
        
        self.warmth = ctk.CTkOptionMenu(master= self,
                                       values=["Low", "Mid", "High"],
                                       command=None)
        self.warmth.grid(row=6, column=1)
        self.warmth_label = ctk.CTkLabel(self, text="Warmth")
        self.warmth_label.grid(row=6, column=0)
        self.warmth.set("Low")  # set initial value

        self.pH = ctk.CTkOptionMenu(master= self,
                                       values=["Low", "Mid", "High"],
                                       command=None)
        self.pH.grid(row=7, column=1)
        self.pH_label = ctk.CTkLabel(self, text="pH")
        self.pH_label.grid(row=7, column=0)
        self.pH.set("Low")
        
        self.substrate = ctk.CTkTextbox(master= self,
                                    width=120,
                                    height=75,
                                    border_width=2,
                                    corner_radius=10)
        
        self.substrate.grid(row=8, column=1)
        self.substrate_label = ctk.CTkLabel(self, text="Substrate")
        self.substrate_label.grid(row=8, column=0)
        
        self.add_button = ctk.CTkButton(master= self,
                                 width= 120,
                                 height= 64,
                                 border_width= 0,
                                 corner_radius= 8,
                                 text= "Add to Database",
                                 command= lambda: self.make_a_plant_class(parent))
        self.add_button.grid(row=9, column=0)
        #self.pack(expand = True, fill= 'both')
        
    def make_a_plant_class(self, parent):
       
        if type(self.photo_path) != str:
           self.photo_path = './images/default.jpg'
        if self.photo_path == "./images/":
            self.photo_path = './images/default.jpg'
       
        plant = Plant()
        plant.name = self.name.get()
        plant.about = self.about.get("0.0","end-1c")
        plant.photo = self.photo_path
        plant.hydration = self.hydration.get()
        plant.light = self.light.get()
        plant.warmth = self.warmth.get()
        plant.pH = self.pH.get()
        plant.substrate = self.substrate.get("0.0","end-1c")
        
        parent.plant_to_database(plant)
        self.destroy()
        parent.draw_plants_frame()
        

    
    def photo_path_fun(self):

        self.photo_path = filedialog.askopenfilename(initialdir = "./images/",
                                                    title = "Select a Photo",
                                                    filetypes = (("Image files",
                                                                            "*.jpg  *.jpeg  *.gif  *.png"),
                                                                ("all files",
                                                                            "*.*")))
        check = copy_image(self.photo_path)
        
        if check == "OK":
            self.photo_path = "./images/" + os.path.basename(self.photo_path)
        else:
            self.photo_path = check      #if check is not "OK" then it is the new filename

        print(self.photo_path)

    

class PlantEditFrame(PlantCreateFrame):
    def __init__(self, parent, plant):
        super().__init__(parent)
        self.title("PyFlora App - Edit Plant Information")
        self.parent = parent
        self.plant = plant
        self.image_button = ctk.CTkButton(master= self,
                                 width= 120,
                                 height= 120,
                                 border_width= 0,
                                 corner_radius= 8,
                                 image= ctk.CTkImage(open_image(self.plant.photo), size=(120, 120)),
                                 text= "",
                                 command= None).grid(row=0, column=0, columnspan=2)
        self.name.insert(0, self.plant.name)
        self.about.insert("0.0", self.plant.about)
        self.hydration.set(self.plant.hydration)
        self.light.set(self.plant.light)
        self.warmth.set(self.plant.warmth)
        self.pH.set(self.plant.pH)
        self.substrate.insert("0.0", self.plant.substrate)
        
        self.add_button.destroy()
        self.add_button = ctk.CTkButton(master= self,
                                 width= 120,
                                 height= 32,
                                 border_width= 0,
                                 corner_radius= 8,
                                 text= "Update information",
                                 command= self.update_plant)
        self.add_button.grid(row=9, column=0)

        self.delete_button = ctk.CTkButton(master= self,
                                 width= 120,
                                 height= 32,
                                 border_width= 0,
                                 corner_radius= 8,
                                 text= "Delete from Database",
                                 command= self.delete_plant)
        self.delete_button.grid(row=9, column=1)

    def update_plant(self):
        self.plant.name = self.name.get()
        self.plant.about = self.about.get("0.0","end-1c")
        self.plant.hydration = self. hydration.get()
        
        if type(self.photo_path) == str:
            if self.photo_path == "./images/":
                self.photo_path = "./images/default.jpg"
            self.plant.photo = self.photo_path
        self.plant.light =self.light.get()
        self.plant.warmth = self.warmth.get()
        self.plant.pH = self.pH.get()
        self.plant.substrate = self.substrate.get("0.0","end-1c")
        self.parent.repo.update_plant(self.plant)
        self.destroy()
        self.parent.draw_plants_frame()
        
    
    def delete_plant(self):
        pots_to_update = self.parent.repo.get_all_pots_plant(user_id= self.parent.user_id, plant_id=self.plant.id)
        for pot in pots_to_update:
            pot.plant_id = None
            self.parent.repo.update_pot(pot)
        self.parent.delete_plant(self.plant)
        self.destroy()
        self.parent.draw_plants_frame()

if __name__ == "__main__":
    App = PyFlora()
