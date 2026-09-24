from database import engine

try:
    connection = engine.connect()
    print("Verbindung erfolgreich!")
    connection.close()
except Exception as e:
    print("Fehler:", e)