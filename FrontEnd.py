import io
import base64
from PIL import Image
import customtkinter as ctk
from DatabaseManager import *

class FrontEnd(ctk.CTk):
    def __init__(self, width, height):
        super().__init__()
        self.dbman = DatabaseManager()
        self.width = width
        self.height = height
        ctk.set_appearance_mode("light")
        self.title("Inventar-Editor")
        self.geometry(f"{self.width}x{self.height}")
        self.minsize(1200, 700)
        self.maxsize(1200, 700)
        self.my_button = ctk.CTkButton(self, text="+", fg_color='#d6d6d6', text_color='#000000',
                                       width=self.width * 0.06, height=self.height * 0.07, font=("Cairo", 30))
        self.my_button.place(x=self.width * 0.91, y=self.height * 0.8929)
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=self.width * 0.83, height=self.height * 0.68)
        self.scrollable_frame.place(x=self.width * 0.11, y=self.height * 0.14)
        data = self.dbman.read_all()
        for row in data:
            raw = str(row).split(", ")
            newframe = ctk.CTkFrame(self.scrollable_frame)
            ctk.CTkLabel(newframe, text=raw[0])  # house name
            img_data = row[1]
            img_stream = io.BytesIO(img_data)
            pil_img = Image.open(img_stream)
            img = ctk.CTkImage(pil_img, size=(200, 150))
            ctk.CTkLabel(newframe, image=img, text="").pack()
            ctk.CTkLabel(newframe, text=f"Ankaufspreis: {raw[2]} €").pack()
            ctk.CTkLabel(newframe, text=f"Verkaufspreis: {raw[3]} €").pack()
            ctk.CTkLabel(newframe, text=f"Provision: {raw[4]} %").pack()
            ctk.CTkLabel(newframe, text=f"Räume: {raw[5]}").pack()
            ctk.CTkLabel(newframe, text=f"Wohnfläche: {raw[6]} m²").pack()
            ctk.CTkLabel(newframe, text=f"Grundstücksfläche: {raw[7]} m²").pack()
            newframe.pack(pady=10, padx=100)
        self.mainloop()




FrontEnd(1200, 700)