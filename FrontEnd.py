import customtkinter as ctk
from DatabaseManager import *

class FrontEnd(ctk.CTk):
    def __init__(self, width, height):
        super().__init__()
        self.dbmanager = DatabaseManager()
        self.width = width
        self.height = height
        ctk.set_appearance_mode("light")
        self.title("Inventar-Editor")
        self.geometry(f"{self.width}x{self.height}")
        self.minsize(1200, 700)
        self.maxsize(1200, 700)
        my_button = ctk.CTkButton(self, text="+", fg_color='#d6d6d6', text_color='#000000', width=self.width * 0.06,
                                  height=self.height * 0.07, font=("Cairo", 30))
        my_button.place(x=self.width * 0.91, y=self.height * 0.8929)
        inventory_frame = ctk.CTkScrollableFrame(self, width=self.width * 0.83, height=self.height * 0.68)
        inventory_frame.place(x=self.width * 0.11, y=self.height * 0.14)
        self.house_dict = self.get_data_from_db()
        i = 0
        houses = []
        for key in self.house_dict:
            attr = self.unpack_values(self.house_dict, key)
            houses[i] = ctk.CTkFrame(inventory_frame)
            ctk.CTkLabel(houses[i], text=str(attr[0]))
            ctk.CTkLabel(houses[i], text=str(attr[2]))
            # now work with unpack_values to insert the rest of the data
        self.mainloop()

    def get_data_from_db(self):
        house_dict = dict(self.dbmanager.read_all())
        print(house_dict)
        return house_dict

    def unpack_values(self, dictionary, key):
        """Gibt eine Liste der Attribute für ein Haus aus. Der key ist immer die HausID.
        values[0] i -> Name, values[8] -> HausID. Weiteres in der Doku."""
        values = []
        dic = str(dictionary[key]).split(", ")                      # check if it really is separated by comma
        for i in dic:
            values.append(i)
        return values




FrontEnd(1200, 700)