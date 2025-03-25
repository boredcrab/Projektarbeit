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
        # Parameters
        self.dbman = DatabaseManager()
        self.width = width
        self.height = height
        ctk.set_appearance_mode("light")
        self.title("Inventar-Editor")
        self.geometry(f"{self.width}x{self.height}")

        # Values for insertion
        self.addframe = None
        self.name = None
        self.bprice = None
        self.sprice = None
        self.ins_image = None
        self.rooms = None
        self.larea = None
        self.garea = None
        self.provision = None
        self.desc = None
        self.floatvalues = [self.bprice, self.sprice, self.provision]
        self.intvalues = [self.rooms, self.larea, self.garea]

        self.minsize(1200, 700)
        self.maxsize(1200, 700)
        self.add_button = ctk.CTkButton(self, text="+", fg_color='#d6d6d6', text_color='#000000',
                                        width=self.width * 0.06, height=self.height * 0.07, font=("Cairo", 30), command=self.on_plusbutton_click)
        self.add_button.place(x=self.width * 0.91, y=self.height * 0.8929)
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

    def on_plusbutton_click(self):
        if self.addframe is None or not self.addframe.winfo_exists():
            self.addframe = ctk.CTkFrame(self, width=self.width * 0.80, height=self.height * 0.7,
                                         fg_color="#ffffff", border_color="#1E90FF", border_width=1, corner_radius=4)
            self.addframe.place(x=self.width * 0.13, y=self.height * 0.14)

            image_placeholder = ctk.CTkFrame(self.addframe, width=300, height=210, fg_color="#e0e0e0", corner_radius=4)
            image_placeholder.place(x=20, y=20)
            import_button = ctk.CTkButton(self.addframe, text="Importieren (JPG)", width=200, height=30,
                                          fg_color="#d6d6d6", text_color="#000000", corner_radius=4)
            import_button.place(x=65, y=240)
            # Property Name Input
            name_entry = ctk.CTkEntry(self.addframe, width=320, height=50, placeholder_text="Immobilienname", corner_radius=4, border_width=1)
            self.name = name_entry.get()
            name_entry.place(x=350, y=30)

            # Price Inputs
            ctk.CTkLabel(self.addframe, text="Ankaufspreis:", font=("Cairo", 14), corner_radius=4).place(x=350, y=120)
            purchase_price = ctk.CTkEntry(self.addframe, width=150, height=30, placeholder_text="Preis", border_width=1, corner_radius=4)
            self.bprice = purchase_price.get()
            purchase_price.place(x=450, y=120)
            ctk.CTkLabel(self.addframe, text="€", font=("Cairo", 16), corner_radius=4).place(x=600, y=120)
            ctk.CTkLabel(self.addframe, text="Verkaufspreis:", font=("Cairo", 14), corner_radius=4).place(x=350, y=160)
            sell_price = ctk.CTkEntry(self.addframe, width=150, height=30, placeholder_text="Preis", border_width=1, corner_radius=4)
            self.sprice = sell_price.get()
            sell_price.place(x=450, y=160)
            ctk.CTkLabel(self.addframe, text="€", font=("Cairo", 16), corner_radius=4).place(x=600, y=160)

            ctk.CTkLabel(self.addframe, text="Anzahl Zimmer:", font=("Cairo", 14, "bold"), corner_radius=4).place(x=20, y=300)
            room_count = ctk.CTkEntry(self.addframe, width=100, height=30, placeholder_text="Anzahl", border_width=1, corner_radius=4)
            self.rooms = room_count.get()
            room_count.place(x=220, y=300)
            ctk.CTkLabel(self.addframe, text="Wohnfläche in m²:", font=("Cairo", 14, "bold"), corner_radius=4).place(x=20, y=340)
            area = ctk.CTkEntry(self.addframe, width=100, height=30, placeholder_text="Fläche", border_width=1, corner_radius=4)
            self.larea = area.get()
            area.place(x=220, y=340)
            ctk.CTkLabel(self.addframe, text="Grundstücksfläche in m²:", font=("Cairo", 14, "bold"), corner_radius=4).place(x=20, y=380)
            total_area = ctk.CTkEntry(self.addframe, width=100, height=30, placeholder_text="Fläche", border_width=1, corner_radius=4)
            self.garea = area.get()
            total_area.place(x=220, y=380)
            ctk.CTkLabel(self.addframe, text="Maklerprovision in %:", font=("Cairo", 14, "bold"), corner_radius=4).place(x=20, y=420)
            commission = ctk.CTkEntry(self.addframe, width=100, height=30, placeholder_text="Prozent", border_width=1, corner_radius=4)
            self.provision = commission.get()
            commission.place(x=220, y=420)

            description = ctk.CTkTextbox(self.addframe, width=500, height=200, corner_radius=4)
            description.insert("0.0", "Beschreibung (optional)")
            description.place(x=350, y=260)

            save_button = ctk.CTkButton(self.addframe, text="Speichern", fg_color='#d6d6d6', text_color='#000000', width=140, height=40, font=("Cairo", 14), corner_radius=4, border_color="000000")
            save_button.place(x=800, y=20)
            cancel_button = ctk.CTkButton(self.addframe, text="Abbrechen", fg_color='#fca1a0', text_color='#000000', width=140, height=40, font=("Cairo", 14), command=self.vanish_editor, corner_radius=4, border_color="000000")
            cancel_button.place(x=800, y=70)


    def vanish_editor(self):
        if self.addframe and self.addframe.winfo_exists():
            self.addframe.destroy()

    def save_changes(self):
        self.prepare_data()
        for i, j in self.intvalues, self.floatvalues:
            if isinstance(i, int) and isinstance(j, float):
                continue
            elif not (isinstance(i, int) and isinstance(j, float)):
                return f"Bitte {i} als Ganzzahl und {j} als Zahl angeben! Sonderzeichen werden nicht angenommen."
            elif not isinstance(i, int):
                return f"Bitte {i} als Ganzzahl angeben! Sonderzeichen werden nicht angenommen."
            elif not isinstance(j, float):
                return f"Bitte {j} als Zahl angeben! Sonderzeichen werden nicht angenommen."
        self.dbman.insert(self.name, self.ins_image, self.bprice, self.sprice, self.provision, self.rooms, self.larea, self.garea)
        self.addframe.pack_forget()

    def prepare_data(self):
        self.bprice = str(self.bprice).strip(" .").replace(",", ".")
        self.sprice = str(self.sprice).strip(" .").replace(",", ".")
        self.provision = str(self.provision).replace(",", ".")

Programm(1200, 700)