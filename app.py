from flask import Flask, render_template, request, jsonify
from nlp_engine import nlp

app = Flask(__name__)

@app.route('/')
def home():
    """Serve the main UI html page"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint for handling chat messages"""
    data = request.get_json()
    
    if not data or "message" not in data:
        return jsonify({"response": "No message provided. Please say something!"}), 400
        
    user_message = data["message"]
    
    # Process the message and generate a bot response using the NLPEngine
    bot_response = nlp.get_response(user_message)
    
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    # Run the web server
    app.run(debug=True, port=5000)
