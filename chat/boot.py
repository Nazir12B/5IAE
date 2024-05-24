from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    
    # Logique simple pour le chatbot
    if user_message.lower() == 'coucou':
        response = 'oui'
    else:
        response = 'Désolé, je ne comprends pas. Pouvez-vous reformuler?'
    
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
