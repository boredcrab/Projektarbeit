# Makler-Inventar

Ein Programm von Nuran

## Nutzung der Funktionen

Fast jede Funktion ist kurz erklärt. Weitere Informationen können hier gefunden werden.

### FrontEnd.unpack_values(dict, key)

> Gibt eine Liste der Attribute für ein Haus aus. Der key ist immer die HausID.

Die Zahl **i** in value[ i ] gibt an, welche der folgenden Attribute genommen wird:

0 - Name der Immobilie\
1 - HausID\
2 - Bild (im BLOB-Format)\
3 - Ankaufspreis in **€**\
4 - Verkaufspreis in **€**\
5 - Maklerprovision in **%**\
6 - Raumanzahl\
7 - Wohnfläche in **m²**\
8 - Grundstücksfläche in **m²**

