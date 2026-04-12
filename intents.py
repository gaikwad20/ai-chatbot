# Dictionary of intents and their possible patterns/responses
INTENTS = [
    {
        "intent": "greeting",
        "patterns": ["hello", "hi", "hey", "greetings", "good morning", "good evening", "howdy", "hello there", "what's up", "yo"],
        "responses": ["Hello there! How can I help you today?", "Hi! What's on your mind?", "Greetings! How can I assist?", "Hey! Let me know what you need help with."]
    },
    {
        "intent": "identity",
        "patterns": ["name", "who are you", "what are you", "who am i talking to", "what is your name", "tell me about yourself"],
        "responses": ["I am your friendly NLP-based chatbot.", "You can call me ChatBot. I'm built with Python!", "I am a virtual assistant created to help you."]
    },
    {
        "intent": "help",
        "patterns": ["help", "support", "assist", "i need help", "can you help me", "how does this work", "what can you do"],
        "responses": ["Sure, I can help! What do you need assistance with?", "I'm here to support you. Ask me anything!", "I can answer questions and chat with you. How can I help?"]
    },
    {
        "intent": "programming",
        "patterns": ["python", "code", "programming", "flask", "how to code", "machine learning", "nlp", "scikit-learn"],
        "responses": ["Python is an awesome programming language! This web app is powered by Flask and scikit-learn.", "I love coding! Are you building something cool?", "Programming is great. I was built using Python and Natural Language Processing techniques."]
    },
    {
        "intent": "farewell",
        "patterns": ["bye", "goodbye", "exit", "see ya", "cya", "catch you later", "have a good one", "bye bye"],
        "responses": ["Goodbye! Have a great day!", "See you later!", "Take care!", "Bye! Feel free to chat again later."]
    },
    {
        "intent": "wellbeing",
        "patterns": ["how are you", "how are you doing", "what's up", "how do you do", "are you okay"],
        "responses": ["I'm doing great, thank you for asking!", "I'm just a bundle of code, but I'm feeling fantastic!", "All systems operational! How are you?"]
    }
]

# Fallback responses when confidence is too low
FALLBACK_RESPONSES = [
    "I'm not quite sure I understand. Can you try rephrasing?",
    "Can you give me more details?",
    "I’m still learning, try asking differently.",
    "I didn't catch that. Could you say it in another way?"
]
