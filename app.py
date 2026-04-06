from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Basic NLP intent dictionary
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

def ensure_nltk_data():
    """Ensure NLTK required tokenizers are downloaded"""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
        
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        nltk.download('punkt_tab', quiet=True)

# Try to initialize NLP processing safely
HAS_NLTK = False
try:
    import nltk
    ensure_nltk_data()
    HAS_NLTK = True
except ImportError:
    print("Warning: NLTK module not found. Using basic fallback matching.")
except Exception as e:
    print(f"Warning: NLTK initialization failed. Using basic fallback matching. Error: {e}")

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer

# Download required data
nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

# Prepare training data from intents
all_keywords = []
all_responses = []

for intent in intents:
    for keyword in intent["keywords"]:
        all_keywords.append(keyword)
        all_responses.append(intent["responses"])

def preprocess(text):
    tokens = nltk.word_tokenize(text.lower())
    lemmas = [lemmatizer.lemmatize(word) for word in tokens]
    return " ".join(lemmas)

# Preprocess keywords
processed_keywords = [preprocess(k) for k in all_keywords]

# Train vectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(processed_keywords)

def nlp_process(user_message):
    user_processed = preprocess(user_message)
    user_vector = vectorizer.transform([user_processed])

    # Calculate similarity
    similarities = cosine_similarity(user_vector, X)
    best_match_index = np.argmax(similarities)

    # Confidence check (important!)
    if similarities[0][best_match_index] < 0.3:
        return "I'm not quite sure I understand. Can you try rephrasing?"

    # Return random response from matched intent
    return random.choice(all_responses[best_match_index])

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
    
    # Process the message and generate a bot response
    bot_response = nlp_process(user_message)
    
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    # Run the web server
    app.run(debug=True, port=5000)
