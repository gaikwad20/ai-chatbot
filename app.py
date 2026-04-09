from flask import Flask, render_template, request, jsonify
import random
import nltk
from nltk.stem import WordNetLemmatizer

app = Flask(__name__)

# Download required NLTK data at startup
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('wordnet', quiet=True)

lemmatizer = WordNetLemmatizer()

# Intent dictionary with keywords and responses
intents = [
    {
        "keywords": ["hello", "hi", "hey", "greetings", "good morning", "good evening"],
        "responses": ["Hello there! How can I help you today?", "Hi! What's on your mind?", "Greetings! How can I assist?"]
    },
    {
        "keywords": ["name", "who are you", "what are you"],
        "responses": ["I am your friendly NLP-based chatbot.", "You can call me ChatBot. I'm built with Python!"]
    },
    {
        "keywords": ["help", "support", "assist"],
        "responses": ["Sure, I can help! What do you need assistance with?", "I'm here to support you. Ask me anything!"]
    },
    {
        "keywords": ["python", "code", "programming", "flask"],
        "responses": ["Python is an awesome programming language! This web app is powered by Flask.", "I love coding! Are you building something cool?"]
    },
    {
        "keywords": ["bye", "goodbye", "exit", "see ya", "cya"],
        "responses": ["Goodbye! Have a great day!", "See you later!", "Take care!"]
    },
    {
        "keywords": ["how are you", "how are you doing", "what's up"],
        "responses": ["I'm doing great, thank you for asking!", "I'm just a bundle of code, but I'm feeling fantastic!", "All systems operational! How are you?"]
    }
]

def preprocess(text):
    """Tokenize and lemmatize text into a set of words."""
    tokens = nltk.word_tokenize(text.lower())
    return set(lemmatizer.lemmatize(word) for word in tokens if word.isalpha())

def word_overlap_score(user_words, keyword_phrase):
    """Score a keyword phrase against user input using word overlap (Jaccard-style)."""
    keyword_words = preprocess(keyword_phrase)
    if not keyword_words:
        return 0.0
    overlap = len(user_words & keyword_words)
    return overlap / len(keyword_words)

def nlp_process(user_message):
    """Find the best matching intent using word overlap scoring."""
    user_words = preprocess(user_message)

    best_score = 0.0
    best_responses = None

    for intent in intents:
        for keyword in intent["keywords"]:
            score = word_overlap_score(user_words, keyword)
            if score > best_score:
                best_score = score
                best_responses = intent["responses"]

    # Confidence threshold
    if best_score < 0.3:
        return "I'm not quite sure I understand. Can you try rephrasing?"

    return random.choice(best_responses)

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
    bot_response = nlp_process(user_message)

    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(debug=False, port=5000)
