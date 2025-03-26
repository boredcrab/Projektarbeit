import mysql.connector

class DatabaseManager:
    def __init__(self):
        self. connection = mysql.connector.connect(
            user='root',
            password='root',
            host='127.0.0.1',
            port = "3306",
            database='MaklerInventar')
        self.cursor = self.connection.cursor()

    def close_connection(self):
        self.connection.close()

    # insert data into table
    def insert(self, Hausname=None, Bild=None, PreisAn=None, PreisVer=None, Provision=None, Raumanzahl=None,
           Wohnflaeche=None, Grundstuecksflaeche=None, Beschreibung=None):
        data = self.sanitize_input(Hausname=Hausname, Bild=Bild, PreisAn=PreisAn, PreisVer=PreisVer,
                                      Provision=Provision, Raumanzahl=Raumanzahl,
                                      Wohnflaeche=Wohnflaeche, Grundstuecksflaeche=Grundstuecksflaeche, Beschreibung=Beschreibung)

        if not data:
            raise ValueError("No valid data to insert!")
        elif not isinstance(data, list):
            raise ValueError("SQL Injection deKtected!")
# hallo
        attributes = []
        for key in data.keys():
            if key == "Hausname" or key == "Bild":                                                    # gibt kein %BLOB
                attributes.append(f"{key} = %s")
            else:
                attributes.append(f"{key} = %f")

        table = "Haus(HausName, HausID, Bild, Ankaufspreis, Verkaufspreis, Marklerprovision, Raumanzahl, Wohnflaeche, Grundstuecksflaeche)"
        command = f"INSERT INTO {table} VALUES {", ".join(attributes)}"
        self.cursor.execute(command, tuple(data.values()))
        self.connection.commit()

    # read SPECIFIC data from table
    def read_all(self):
        select = "SELECT * FROM Haus"
        self.cursor.execute(select)
        data = self.cursor.fetchall()
        return data

    # CHANGE data in table
    def change(self, house_id, Hausname=None, Bild=None, PreisAn=None, PreisVer=None, Provision=None, Raumanzahl=None,
           Wohnflaeche=None, Grundstuecksflaeche=None, Beschreibung=None):

        """Ändert angegebene Daten in der Datenbank."""

        updates = self.sanitize_input(Hausname=Hausname, Bild=Bild, PreisAn=PreisAn, PreisVer=PreisVer,
        Provision=Provision, Raumanzahl=Raumanzahl,
        Wohnflaeche=Wohnflaeche, Grundstuecksflaeche=Grundstuecksflaeche, Beschreibung=Beschreibung)

        if not updates:
            raise ValueError("Invalid input detected!")
        elif not isinstance(updates, list):
            raise ValueError("SQL Injection detected!")

        attributes = []
        for key in updates.keys():
            if key == "Hausname" or key == "Bild":                                  # !! LONG BLOB!!
                attributes.append(f"{key} = %s")
            else:
                attributes.append(f"{key} = %f")
        command = f"UPDATE Haus SET {", ".join(attributes)} WHERE HausID = {house_id}"
        self.cursor.execute(command, tuple(updates.values()))
        self.connection.commit()




    # sanitize input -> make sure no SQL Injection can occur!
    def sanitize_input(self, **kwargs):
        """Prüft auf SQL-Injection. Wenn beim return ein String rauskommt, wurde eine SQL-Injection erkannt und
        die Funktion darf nicht weiterverwendet werden."""
        clean_data = {}
        illegal_words = ("Select", "Drop", "Insert", "Delete", "Update")
        for key, value in kwargs.items():
            if isinstance(value, str):
                for i in illegal_words:
                    print(type(i), type(value))
                    j = str(i.lower())
                    v = str(value.lower)
                    if j in v:
                        string = f"WARNING: Potential SQL injection detected in '{key}': '{value}'!"
                        return string
                clean_data[key] = value
            else:
                continue
        return clean_data