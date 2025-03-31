import io
import re
import tkinter as tk
from PIL import Image
from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
from customtkinter import filedialog
from DatabaseManager import *


def format_number(number):
    return re.sub(r'(?<=\d)(?=(\d{3})+(?!\d))', ' ', str(number))


class Programm(ctk.CTk):
    def __init__(self, width, height):
        super().__init__()


        # =============================================================================================================
        # App Parameters
        # =============================================================================================================
        self.dbman = DatabaseManager()
        self.width = width
        self.height = height
        ctk.set_appearance_mode("light")
        self.title("Inventar-Editor")
        self.geometry(f"{self.width}x{self.height}")
        self.minsize(1200, 700)
        self.maxsize(1200, 700)
        self.add_button = ctk.CTkButton(self, text="+", fg_color='#d6d6d6', text_color='#000000',
                                        width=self.width * 0.06, height=self.height * 0.07, font=("Cairo", 30), command=self.on_plusbutton_click)
        self.add_button.place(x=self.width * 0.91, y=self.height * 0.8929)
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=self.width * 0.83, height=self.height * 0.68, fg_color="transparent")
        self.scrollable_frame.place(x=self.width * 0.11, y=self.height * 0.14)



        # =============================================================================================================
        # All entry widgets for the editor frame
        # =============================================================================================================
        self.addframe = ctk.CTkFrame(self, width=self.width * 0.80, height=self.height * 0.7,
                                     fg_color="#ffffff", border_color="#1E90FF", border_width=1, corner_radius=4)
        self.purchase_price = ctk.CTkEntry(self.addframe, width=150, height=30, placeholder_text="Preis", border_width=1, corner_radius=4)
        self.name_entry = ctk.CTkEntry(self.addframe, width=340, height=50, placeholder_text="Immobilienname",
                                       corner_radius=4, border_width=1)
        self.sell_price = ctk.CTkEntry(self.addframe, width=150, height=30, placeholder_text="Preis", border_width=1,
                                       corner_radius=4)
        self.room_count = ctk.CTkEntry(self.addframe, width=100, height=30, placeholder_text="Anzahl", border_width=1,
                                       corner_radius=4)
        self.area = ctk.CTkEntry(self.addframe, width=100, height=30, placeholder_text="Fläche", border_width=1,
                                 corner_radius=4)
        self.total_area = ctk.CTkEntry(self.addframe, width=100, height=30, placeholder_text="Fläche", border_width=1,
                                       corner_radius=4)
        self.commission = ctk.CTkEntry(self.addframe, width=100, height=30, placeholder_text="Prozent", border_width=1,
                                       corner_radius=4)
        self.description = ctk.CTkTextbox(self.addframe, width=500, height=200, corner_radius=4)
        # Values for insertion
        self.name = None
        self.bprice = None
        self.sprice = None
        self.ins_image = None
        self.rooms = None
        self.larea = None
        self.garea = None
        self.provision = None
        self.desc = None

        self.update_inventory()

        self.mainloop()

    def on_right_click(self, event, entry_id):
        menu = tk.Menu(self.scrollable_frame, tearoff=0)
        menu.add_command(label="Löschen", command=lambda: self.confirm_delete(entry_id))
        menu.tk_popup(event.x_root, event.y_root)
        print(event.x_root, event.y_root)

    def confirm_delete(self, entry_id):
        msgbox = CTkMessagebox(title="Bestätigung", message="Möchten Sie diesen Eintrag wirklich löschen?",
                               icon="warning", option_1="Ja", option_2="Nein")
        if msgbox.get() == "Ja":
            self.dbman.delete(entry_id)
            self.update_inventory()

    # =============================================================================================================
    # Open Add Editor
    # =============================================================================================================

    def on_plusbutton_click(self):
        if self.addframe and self.addframe.winfo_exists():
            if not self.addframe.winfo_ismapped():
                self.addframe.place(x=self.width * 0.13, y=self.height * 0.14)

                image_placeholder = ctk.CTkFrame(self.addframe, width=300, height=210, fg_color="#e0e0e0", corner_radius=4)
                image_placeholder.place(x=20, y=20)
                import_button = ctk.CTkButton(self.addframe, text="Importieren (JPG)", width=200, height=30,
                                              fg_color="#d6d6d6", text_color="#000000", corner_radius=4, command=self.on_importbutton_click)
                import_button.place(x=65, y=240)

                # Labels for Pricing
                ctk.CTkLabel(self.addframe, text="Ankaufspreis:", font=("Cairo", 14), corner_radius=4).place(x=350, y=120)
                ctk.CTkLabel(self.addframe, text="€", font=("Cairo", 16), corner_radius=4).place(x=600, y=120)
                ctk.CTkLabel(self.addframe, text="Verkaufspreis:", font=("Cairo", 14), corner_radius=4).place(x=350, y=160)
                ctk.CTkLabel(self.addframe, text="€", font=("Cairo", 16), corner_radius=4).place(x=600, y=160)
                ctk.CTkLabel(self.addframe, text="Anzahl Zimmer:", font=("Cairo", 14, "bold"), corner_radius=4).place(x=20, y=300)
                ctk.CTkLabel(self.addframe, text="Wohnfläche in m²:", font=("Cairo", 14, "bold"), corner_radius=4).place(x=20, y=340)
                ctk.CTkLabel(self.addframe, text="Grundstücksfläche in m²:", font=("Cairo", 14, "bold"), corner_radius=4).place(x=20, y=380)
                ctk.CTkLabel(self.addframe, text="Maklerprovision in %:", font=("Cairo", 14, "bold"),
                             corner_radius=4).place(x=20, y=420)



                self.description.insert("0.0", "Beschreibung (optional)")


                save_button = ctk.CTkButton(self.addframe, text="Speichern", fg_color='#d6d6d6', text_color='#000000',
                                            width=140, height=40, font=("Cairo", 14), corner_radius=4,
                                            border_color="000000", command=self.save_changes)

                cancel_button = ctk.CTkButton(self.addframe, text="Abbrechen", fg_color='#fca1a0', text_color='#000000',
                                              width=140, height=40, font=("Cairo", 14), command=self.vanish_editor,
                                              corner_radius=4, border_color="000000")
                self.name_entry.place(x=350, y=40)
                self.purchase_price.place(x=450, y=120)
                self.sell_price.place(x=450, y=160)
                self.room_count.place(x=220, y=300)
                self.area.place(x=220, y=340)
                self.total_area.place(x=220, y=380)
                self.commission.place(x=220, y=420)
                self.description.place(x=350, y=260)
                save_button.place(x=800, y=20)
                cancel_button.place(x=800, y=70)
        else:
            self.add_button = ctk.CTkButton(self, text="+", fg_color='#d6d6d6', text_color='#000000',
                                            width=self.width * 0.06, height=self.height * 0.07, font=("Cairo", 30),
                                            command=self.on_plusbutton_click)



    def vanish_editor(self):
        if self.addframe and self.addframe.winfo_exists():
            self.addframe.place_forget()



    def save_changes(self):
        """Konvertiert Kommas in Punkte, damit Floats richtig eingetrage werden können,
        überprüft die Einträge auf Sonderzeichen und gibt Daten durch, wenn sie passen."""
        data = {
            "Name": self.name_entry.get(),
            "Beschreibung": self.description.get("1.0", 'end-1c'),
            "Einkaufspreis": self.purchase_price.get(),
            "Verkaufspreis": self.sell_price.get(),
            "Zimmeranzahl": self.room_count.get(),
            "Fläche": self.area.get(),
            "Gesamtfläche": self.total_area.get(),
            "Provision": self.commission.get(),
                        }

        error_messages = []
        string_check = re.compile(r'[@_#$%^&*<>/|}{~="]')
        float_check = re.compile(r'[@_#$€^°!"§%&/()=}{?`´~-]')

        for field, value in data.items():
            if not value.strip():
                error_messages.append(f"Das Feld '{field}' darf nicht leer sein.")
            if field in ["Name", "Beschreibung"] and string_check.search(value):
                error_messages.append(f"Das Feld '{field}' enthält ungültige Zeichen.")

        if not self.ins_image:
            error_messages.append("Es wurde kein Bild hinzugefügt. Bitte wählen Sie ein Bild aus.")

        if error_messages:
            CTkMessagebox(title="Fehler", message="\n".join(error_messages), icon="cancel")
            return

        self.name = data["Name"]
        self.desc = data["Beschreibung"]
        self.bprice = data["Einkaufspreis"].strip(" .").replace(",", ".")
        self.sprice = data["Verkaufspreis"].strip(" .").replace(",", ".")
        self.rooms = data["Zimmeranzahl"].strip(" .").replace(",", ".")
        self.larea = data["Fläche"].strip(" .").replace(",", ".")
        self.garea = data["Gesamtfläche"].strip(" .").replace(",", ".")
        self.provision = data["Provision"].strip(" .").replace(",", ".")

        flts = {
            "Zimmeranzahl": self.rooms,
            "Fläche": self.larea,
            "Gesamtfläche": self.garea,
            "Einkaufspreis": self.bprice,
            "Verkaufspreis": self.sprice,
            "Provision": self.provision,
        }

        for field, value in flts.items():
            if float_check.search(value):
                error_messages.append(f"Das Feld '{field}' enthält ungültige Zeichen. Bitte nur Zahlen eingeben.")

        if error_messages:
            CTkMessagebox(title="Fehler", message="\n".join(error_messages), icon="cancel")
            return

        try:
            flts = {key: float(value) for key, value in flts.items()}
        except ValueError:
            CTkMessagebox(title="Fehler", message="Bitte stellen Sie sicher, dass alle Zahlenfelder korrekt ausgefüllt sind.",
                          icon="cancel")
            return

        self.dbman.insert(self.name, self.ins_image, flts["Einkaufspreis"], flts["Verkaufspreis"], flts["Provision"], flts["Zimmeranzahl"], flts["Fläche"], flts["Gesamtfläche"], self.desc)
        self.addframe.place_forget()
        self.update_inventory()



    def on_importbutton_click(self):
        file = filedialog.askopenfile(initialdir="C:/Users/ndyck/Downloads", title="Bild auswählen", filetypes=(("JPG","*.jpg"),("JPEG", "*.jpeg")))
        if file:
            pil_img = Image.open(file.name)
            pil_img = pil_img.resize((300, 210))
            img = ctk.CTkImage(pil_img, size=(300, 210))

            # display image
            img_label = ctk.CTkLabel(self.addframe, image=img, text="")
            img_label.img = img
            img_label.place(x=20, y=20)

            # store image
            img_bytes = io.BytesIO()
            pil_img.save(img_bytes, format="JPEG")
            self.ins_image = img_bytes.getvalue()





    # =============================================================================================================
    # Update and format card for each entry in table, delete previous entries
    # =============================================================================================================

    def update_inventory(self):
        for widget in self.scrollable_frame.winfo_children():               # clears all widgets inside scrollable frame; no layering
            widget.destroy()

        data = self.dbman.read_all()
        for row in data:
            # For each subframe/card
            card = ctk.CTkFrame(self.scrollable_frame, width=900, height=150, fg_color="#ffffff", corner_radius=5)
            card.pack(pady=10, fill="x")
            card.bind("<ButtonRelease-3>", lambda event, entry_id=row[8]: self.on_right_click(event, entry_id))

            # Left Section
            left_section = ctk.CTkFrame(card, fg_color="transparent")
            left_section.bind("<ButtonRelease-3>", lambda event, entry_id=row[8]: self.on_right_click(event, entry_id))
            left_section.grid(row=0, column=0, sticky="nw", padx=10, pady=10)
            img_data = row[1]
            img_stream = io.BytesIO(img_data)
            pil_img = Image.open(img_stream)
            img = ctk.CTkImage(pil_img, size=(300, 210))  # Bigger image now
            ctk.CTkLabel(left_section, image=img, text="").grid(row=0, column=0, rowspan=2, padx=(0, 15), sticky="n")
            info_block = ctk.CTkFrame(left_section, fg_color="transparent")
            info_block.bind("<ButtonRelease-3>", lambda event, entry_id=row[8]: self.on_right_click(event, entry_id))
            info_block.grid(row=0, column=1, sticky="w")
            ctk.CTkLabel(info_block, text=row[0], font=("Cairo", 20, "bold")).grid(row=0, column=0, sticky="w")
            ctk.CTkLabel(card, text=f"Maklerprovision: {format_number(str(row[4]).replace(".", ","))} %", font=("Cairo", 16, "bold")).grid(row=0, column=0, columnspan=2, sticky="ne", pady=50, padx=20)
            ctk.CTkLabel(info_block, text=f"{row[5]} Zimmer", font=("Cairo", 14)).grid(row=0, column=1, padx=(10, 0))
            ctk.CTkLabel(info_block, text=f"{row[6]} m²", font=("Cairo", 14)).grid(row=0, column=2, padx=(10, 0))
            ctk.CTkLabel(info_block, text=f"{row[7]} m² ges.", font=("Cairo", 14, "bold")).grid(row=1, column=0, sticky="w", pady=(5, 0))

            right_section = ctk.CTkFrame(card, fg_color="transparent")
            right_section.bind("<ButtonRelease-3>", lambda event, entry_id=row[8]: self.on_right_click(event, entry_id))
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


Programm(1200, 700)