# Makler-Inventar

Ein Programm von Nuran

## Nutzung der Funktionen

Fast jede Funktion ist kurz erklärt. Weitere Informationen können hier gefunden werden.

### FrontEnd.unpack_values(dict, key)

> Gibt eine Liste der Attribute für ein Haus aus. Der key ist immer die HausID.

Die Zahl **i** in value[ i ] gibt an, welche der folgenden Attribute genommen wird:

0 - Name der Immobilie\
1 - Bild (im BLOB-Format)\
2 - Ankaufspreis in **€**\
3 - Verkaufspreis in **€**\
4 - Maklerprovision in **%**\
5 - Raumanzahl\
6 - Wohnfläche in **m²**\
7 - Grundstücksfläche in **m²**\
8 - HausID
