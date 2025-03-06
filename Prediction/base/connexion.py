import pyodbc
from base.config import DB_CONFIG

# Connexion à la base de données
def get_connection():
    """ Établit la connexion avec SQL Server. """
    conn_str = (
        f"DRIVER={{{DB_CONFIG['driver']}}};"
        f"SERVER={DB_CONFIG['server']};"
        f"DATABASE={DB_CONFIG['database']};"
        f"Trusted_Connection={'yes' if DB_CONFIG['trusted_connection'] else 'no'};"
    )

    # On essaie de se connecter et on renvoie la connexion
    try:
        conn = pyodbc.connect(conn_str)
        print("Connexion réussie !")
        return conn
    except Exception as e:
        print("Erreur de connexion :", e)
        return None
