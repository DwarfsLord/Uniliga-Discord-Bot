# Verwende ein offizielles Python-Image als Basis
FROM python:3.12.0 

# Setze das Arbeitsverzeichnis innerhalb des Containers
WORKDIR /app

# Kopiere die Anwendungsabhängigkeiten in das Arbeitsverzeichnis
COPY requirements.txt .

# Installiere die Python-Abhängigkeiten
RUN pip install -r requirements.txt

# Kopiere den restlichen Anwendungscode in das Arbeitsverzeichnis
COPY . .


# Definiere den Befehl, um Ihre Anwendung auszuführen
CMD ["python", "bot.py"]
