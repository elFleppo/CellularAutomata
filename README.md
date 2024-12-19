# CellularAutomata
Zellulärer Automat für Personenstromsimulationen

# Test der Komponenten
Um die Funktion unsere Komponenten zu prüfen haben wir tests geschrieben, welche im Ordner testing in der Datei test_components.py aufgeführt sind.
Um die Tests zu überprüfen, ins Verzeichnis Application wechseln und folgenden Befehl ausführen:  

` python -m unittest -v test_components`

# Rimea Test
Um den Rimea Test durchzuführen muss die Datei run.py gestartet werden. Der Algorithmus (Floodfill, Dijkstra) kann in der run.py movement_method angepasst werden.
Visualisierung (in der Timestep loop ausgeklammert) kann auch angepasst werden.