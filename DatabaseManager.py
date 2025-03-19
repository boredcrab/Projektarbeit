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
    def insert(self, house_id, Hausname=None, Bild=None, PreisAn=None, PreisVer=None, Provision=None, Raumanzahl=None,
           Wohnflaeche=None, Grundstuecksflaeche=None):
        data = self.sanitize_input(Hausname=Hausname, Bild=Bild, PreisAn=PreisAn, PreisVer=PreisVer,
                                      Provision=Provision, Raumanzahl=Raumanzahl,
                                      Wohnflaeche=Wohnflaeche, Grundstuecksflaeche=Grundstuecksflaeche)

        if not data:
            raise ValueError("No valid data to update!")

        attributes = []
        for key in data.keys():
            if key == "Hausname" or key == "Bild":                                                    # gibt kein %BLOB
                attributes.append(f"{key} = %s")
            else:
                attributes.append(f"{key} = %f")

        table = "Haus(HausName, HausID, Bild, Ankaufspreis, Verkaufspreis, Marklerprovision, Raumanzahl, Wohnflaeche, Grundstuecksflaeche)"
        command = f"INSERT INTO {table} VALUES {", ".join(attributes)}"
        self.cursor.execute(command, tuple(data.values()))

    # read ALL data from table
    def read_all(self):
        houses = []
        attributes_list = []
        self.cursor.execute("SELECT * FROM Haus")
        data = self.cursor.fetchall()
        for row in data:
            r = str(row)
            attributes_list.append(r)                                          # adds the current row, starting with [0]
            houses.append(r.split(", ")[1])                             # [1] is always the house id
        return houses, attributes_list


    # read SPECIFIC data from table
    def read(self, house_id):
        select = f"SELECT * FROM Haus WHERE HausID=%s"
        self.cursor.execute(select, (house_id,))
        return self.cursor.fetchall()

    # CHANGE data in table
    def change(self, house_id, Hausname=None, Bild=None, PreisAn=None, PreisVer=None, Provision=None, Raumanzahl=None,
           Wohnflaeche=None, Grundstuecksflaeche=None):

        """Ändert angegebene Daten in der Datenbank."""

        updates = self.sanitize_input(Hausname=Hausname, Bild=Bild, PreisAn=PreisAn, PreisVer=PreisVer,
        Provision=Provision, Raumanzahl=Raumanzahl,
        Wohnflaeche=Wohnflaeche, Grundstuecksflaeche=Grundstuecksflaeche)

        if not updates:
            raise ValueError("Invalid input detected!")

        attributes = []
        for key in updates.keys():
            if key == "Hausname" or key == "Bild":                                                    # gibt kein %BLOB
                attributes.append(f"{key} = %s")
            else:
                attributes.append(f"{key} = %f")
        command = f"UPDATE Haus SET {", ".join(attributes)} WHERE HausID = {house_id}"
        self.cursor.execute(command, tuple(updates.values()))




    # sanitize input -> make sure no SQL Injection can occur!
    def sanitize_input(self, **kwargs):
        """Prüft auf SQL-Injection. Wenn beim return ein String rauskommt, wurde eine SQL-Injection erkannt und
        die Funktion darf nicht weiterverwendet werden."""
        clean_data = {}
        illegal_words = ("Select", "Drop", "Insert", "Delete", "Update")
        for key, value in kwargs.items():
            for i in illegal_words:
                if i.lower() in value.lower:
                    string = f"WARNING: Potential SQL injection detected in '{key}': '{value}'!"
                    return string
            clean_data[key] = value
        return clean_data