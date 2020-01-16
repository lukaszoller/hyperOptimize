# hyperOptimize

Installationsanleitung

Mittels VCS und IDE (Windows / Linux):

1.	Voraussetzung: Python 3.5 bis 3.7. Benötigte Module werden je nach Entwicklungsumgebung nach laden des Projekts automatisch bereitgestellt.
2.	Pullen des Git-Repository:  https://github.com/lukaszoller/hyperOptimize.git direkt in die Entwicklungsumgebung.
3.	Benötigte Packages installieren (mit pip, siehe unten) oder je nach Entwicklungsumgebung automatisch installieren lassen.
4.	Starten der Main-Datei (unter /src/hyperOptimizeApp/Main.py).

Windows: (nur möglich unter 64-bit, mit installer executable)
Anmerkung: Eine rein lauffähige Executable mit Python-Code für alle Windows-Versionen hat sich als schwierig herausgestellt. Hier ist die Installationsanleitung mittels eines Windows-Installers. Dabei muss aber trotzdem Python und die benötigten Module im Vorfeld installiert sein.

1.	Python 3.7 Installieren (Die Machine Learning komponenten benötigen 3.5 bis 3.7).
Wichtig: Unbedingt die 64-Bit-Version installieren.
Wichtig: Unbedingt Python zu den umgebungsvariablen hinzufügen.
https://www.python.org/ftp/python/3.7.6/python-3.7.6-amd64.exe
2.	Benötigte Module: (lässt sich mit Powershell mit «pip install [modulname]» installieren
(Diese Module sind der jeweiligen Python-Version angepasst, deshalb müssen sie lokal installiert werden).
-	pandas
-	sklearn
-	urllib
-	keras
-	future
-	jsonpickle
-	cpuinfo
-	numpy
-	matplotlib
-	pytz
-	tensorflow
3.	Die Datei hyperOptimize-1.0.0.win-amd64.exe als Administrator ausführen.
4.	Unter $pythonhome(=Pfad zur Python-Installation)\Lib\site-packages\hyperOptimizeApp kann nun die Datei HyperOptimize geöffnet werden.
