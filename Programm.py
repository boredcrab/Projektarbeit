import io
import re
from PIL import Image
import customtkinter as ctk
from DatabaseManager import *


def format_number(number):
    return re.sub(r'(?<=\d)(?=(\d{3})+(?!\d))', ' ', str(number))


class Programm(ctk.CTk):
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
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=self.width * 0.83, height=self.height * 0.68, fg_color="transparent")
        self.scrollable_frame.place(x=self.width * 0.11, y=self.height * 0.14)
        data = self.dbman.read_all()
        for row in data:
            # For each subframe/card
            card = ctk.CTkFrame(self.scrollable_frame, width=900, height=150, fg_color="#ffffff", corner_radius=5)
            card.pack(pady=10, fill="x")

            # Left Section
            left_section = ctk.CTkFrame(card, fg_color="transparent")
            left_section.grid(row=0, column=0, sticky="nw", padx=10, pady=10)
            img_data = row[1]
            img_stream = io.BytesIO(img_data)
            pil_img = Image.open(img_stream)
            img = ctk.CTkImage(pil_img, size=(300, 210))  # Bigger image now
            ctk.CTkLabel(left_section, image=img, text="").grid(row=0, column=0, rowspan=2, padx=(0, 15), sticky="n")
            info_block = ctk.CTkFrame(left_section, fg_color="transparent")
            info_block.grid(row=0, column=1, sticky="w")
            ctk.CTkLabel(info_block, text=row[0], font=("Cairo", 20, "bold")).grid(row=0, column=0, sticky="w")
            ctk.CTkLabel(card, text=f"Maklerprovision: {format_number(str(row[4]).replace(".", ","))} %", font=("Cairo", 16, "bold")).grid(row=0, column=0, columnspan=2, sticky="ne", pady=50, padx=20)
            ctk.CTkLabel(info_block, text=f"{row[5]} Zimmer", font=("Cairo", 14)).grid(row=0, column=1, padx=(10, 0))
            ctk.CTkLabel(info_block, text=f"{row[6]} m²", font=("Cairo", 14)).grid(row=0, column=2, padx=(10, 0))
            ctk.CTkLabel(info_block, text=f"{row[7]} m² ges.", font=("Cairo", 14, "bold")).grid(row=1, column=0, sticky="w", pady=(5, 0))

            right_section = ctk.CTkFrame(card, fg_color="transparent")
            right_section.grid(row=0, column=1, sticky="se", padx=10, pady=10)
            ctk.CTkLabel(right_section,
                         text=f"Ankaufspreis:\n{format_number(str(row[2]).replace(".", ","))} €",
                         font=("Cairo", 14)
                         ).grid(row=1, column=0, sticky="e", pady=(5, 0))
            ctk.CTkLabel(
                right_section,
                text=f"Verkaufspreis:\n{format_number(str(row[3]).replace(".", ","))} €",
                font=("Cairo", 14)
            ).grid(row=1, column=1, sticky="e", pady=(5, 0), padx=(15, 0))

            card.grid_columnconfigure(0, weight=1)
            card.grid_columnconfigure(1, weight=0)

        self.mainloop()


Programm(1200, 700)