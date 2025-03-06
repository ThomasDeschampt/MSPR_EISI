from connexion import get_connection

def load_data(query):
    """ Exécute une requête SQL et retourne les résultats sous forme de liste. """
    conn = get_connection()
    if conn is None:
        print("Impossible de récupérer les données.")
        return None

    try:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print("Erreur lors de l'exécution de la requête :", e)
        return None

if __name__ == "__main__":
    query = "SELECT TOP 10 * FROM Candidat;"
    data = load_data(query)

    if data:
        for row in data:
            print(row)
