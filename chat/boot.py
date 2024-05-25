from flask import Flask, request, jsonify, render_template, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Remplacez par une clé secrète sécurisée

# Configuration de la base de données
db_config = {
    'user': 'root',  # Utilisateur par défaut
    'password': '',  # Mot de passe de MySQL
    'host': '127.0.0.1',  # Hôte local
    'database': 'chat'  # Nom de la base de données
}

# Connexion à la base de données
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

# Fonction pour obtenir la liste des villes
def get_cities():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT CITY, IATA_CODE FROM airports")
    cities = {}
    for row in cursor.fetchall():
        city, iata_code = row
        cities[city] = iata_code
    cursor.close()
    conn.close()
    return cities

# Fonction pour obtenir les vols disponibles
def get_available_flights(departure_city, destination_city, DAY,MONTH,YEAR):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT flight_number, airline, departure_time, arrival_time 
        FROM vols 
        WHERE ORIGIN_AIRPORT = %s AND DESTINATION_AIRPORT = %s AND DAY = %s AND MONTH =%s AND YEAR =%s
    """
    cursor.execute(query, (departure_city, destination_city, DAY,MONTH,YEAR))
    flights = cursor.fetchall()
    cursor.close()
    conn.close()
    return flights


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['GET'])
def start():
    session.clear()  # Réinitialiser la session
    cities = get_cities()
    response = f"Bonjour, quelle est votre ville de départ pour ce nouveau vol ?."
    return jsonify({'response': response})

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    cities = get_cities()
    
    if 'departure_city' not in session:
        if user_message in cities:
            session['departure_city'] = user_message
            response = f"Quelle est la ville de destination souhaitez-vous pour votre vol depuis {user_message} ({cities[user_message]}) ?"
        else:
            response = "Désolé, je ne connais pas cette ville. Veuillez en choisir une autre."
    elif 'destination_city' not in session:
        if user_message in cities:
            session['destination_city'] = user_message
            response = f"Quelle date souhaitez-vous pour votre vol de {session['departure_city']} ({cities[session['departure_city']]}) à {user_message}, ({cities[user_message]}) ? Veuillez entrer la date au format AAAA-MM-JJ."
        else:
            response = "Désolé, je ne connais pas cette ville. Veuillez en choisir une autre."
    elif 'departure_date' not in session:
        try:
            # Vérification de la date
            from datetime import datetime
            departure_date = datetime.strptime(user_message, '%Y-%m-%d')
            session['departure_date'] = user_message
            day = departure_date.day
            month = departure_date.month
            year = departure_date.year
            response = f"Recherche des vols disponibles de {session['departure_city']} à {session['destination_city']} pour le {user_message}..."
        
            flights = get_available_flights(cities[session['departure_city']], cities[session['destination_city']], day,month,year)
            if flights:
                flight_list = '<br>'.join([f"Vol {flight[0]} avec {flight[1]}, départ à {flight[2]}, arrivée à {flight[3]}"+"<br>" for flight in flights])
                response += f"<br> Voici les vols disponibles :<br> {flight_list}"
            else:
                response += "<br> Aucun vol disponible à cette date."
        except ValueError:
            response = "Date invalide. Veuillez entrer la date au format AAAA-MM-JJ."
    else:
        response = "Merci de fournir une compagnie aérienne pour votre vol de {session['departure_city']} à {session['destination_city']}."

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)