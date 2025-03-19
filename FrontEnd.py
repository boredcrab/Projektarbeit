import customtkinter as ctk
import DatabaseManager as dm

class FrontEnd(ctk.CTk):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        ctk.set_appearance_mode("light")
        self.title("Inventar-Editor")
        self.geometry(f"{self.width}x{self.height}")
        self.minsize(600, 400)
        self.my_button = ctk.CTkButton(self, text ="+", fg_color='#d6d6d6', text_color='#000000', width=self.width*0.06, height=self.height*0.07, font=("Cairo", 30))

        self.frame = ctk.CTkScrollableFrame(self, width=self.width*0.83, height=self.height*0.68)

        self.mainloop()

    def update_layout(self):
        self.my_button.place(width = self.width * 0.06, height= self.height * 0.07)
        self.my_button.place(x=self.width * 0.91, y=self.height * 0.8929)

        self.frame.configure(width = self.width * 0.83, height = self.height * 0.68)
        self.frame.place(x=self.width*0.11, y=self.height * 0.14)


FrontEnd(1200, 700)