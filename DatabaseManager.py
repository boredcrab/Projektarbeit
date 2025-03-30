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

    def delete(self, hausid):
        self.cursor.execute(f"DELETE FROM Haus WHERE Haus_ID {hausid}")
        self.connection.commit()

    # insert data into table
    def insert(self, Hausname=None, Bild=None, PreisAn=None, PreisVer=None, Provision=None, Raumanzahl=None,
           Wohnflaeche=None, Grundstuecksflaeche=None, Beschreibung=None):
        data = self.sanitize_input(Hausname=Hausname, Bild=Bild, PreisAn=PreisAn, PreisVer=PreisVer,
                                      Provision=Provision, Raumanzahl=Raumanzahl,
                                      Wohnflaeche=Wohnflaeche, Grundstuecksflaeche=Grundstuecksflaeche, Beschreibung=Beschreibung)

        print(data)
        if not data:
            raise ValueError("No valid data to insert!")
        elif isinstance(data, str):
            raise ValueError("SQL Injection detected!")
        if data[1] is None:
            data[1] = ""


        attributes = []
        for value in data:
            i = data.index(value)
            if data[i] =='Beschreibung (optional)':
                data[i] = " "
            if value == data[0] or value == data[8]:                                  # !! LONG BLOB and don't forget the desc!!
                attributes.append(str(value))
            else:
                attributes.append(value)
        table = "Haus"
        columns= "(HausName, Bild, Ankaufspreis, Verkaufspreis, Maklerprovision, Raumanzahl, Wohnflaeche, Grundstuecksflaeche, Beschreibung)"
        command = f"INSERT INTO {table} {columns} VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        print(attributes)
        print(columns)
        self.cursor.execute(command, attributes)
        self.connection.commit()

    # read SPECIFIC data from table
    def read_all(self):
        select = "SELECT * FROM Haus"
        self.cursor.execute(select)
        data = self.cursor.fetchall()
        return data

    # CHANGE data in table; NOT FINISHED DUE TO TIME CONSTRAINTS, DO NOT USE!!!
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
        for value in updates:
            i = updates.index(value)
            if updates[i] == 'Beschreibung (optional)':
                updates[i] = " "
            if value == updates[0] or value == updates[8]:  # !! LONG BLOB and don't forget the desc!!
                attributes.append(str(value))
            else:
                attributes.append(value)
        table = "Haus"
        columns = "(HausName, Bild, Ankaufspreis, Verkaufspreis, Maklerprovision, Raumanzahl, Wohnflaeche, Grundstuecksflaeche, Beschreibung)"
        command = f"UPDATE {table} SET HausName=%s, Bild=%s, Ankaufspreis=%s, Verkaufspreis=%s, Maklerprovision=%s, Raumanzahl=%s, Wohnflaeche=%s, Grundstuecksflaeche=%s, Beschreibung=%s) WHERE "
        print(attributes)
        print(columns)
        self.cursor.execute(command, attributes)
        self.connection.commit()




    # sanitize input -> make sure no SQL Injection can occur!
    def sanitize_input(self, **kwargs):
        """Prüft auf SQL-Injection. Wenn beim return ein String rauskommt, wurde eine SQL-Injection erkannt und
        die Funktion darf nicht weiterverwendet werden."""
        clean_data = []
        illegal_words = ("Select", "Drop", "Insert", "Delete", "Update")
        for key, value in kwargs.items():
            if isinstance(value, str):
                for i in illegal_words:
                    j = str(i.lower())
                    v = str(value.lower)
                    if j in v:
                        string = f"WARNING: Potential SQL injection detected in '{key}': '{value}'!"
                        return string
                clean_data.append(value)
            else:
                clean_data.append(value)
                continue
        return clean_data