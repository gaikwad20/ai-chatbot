import random
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from intents import INTENTS, FALLBACK_RESPONSES

class NLPEngine:
    def __init__(self, confidence_threshold=0.4):
        self.confidence_threshold = confidence_threshold
        self.lemmatizer = WordNetLemmatizer()
        self.vectorizer = TfidfVectorizer()
        self.is_ready = False
        
        self.intent_labels = []    # Keeps track of which intent each pattern belongs to
        self.patterns = []         # Holds the original/processed patterns
        
        # Download NLTK data if needed
        self._ensure_nltk_data()
        self.stop_words = set(stopwords.words('english'))
        
        self._train()

    def _ensure_nltk_data(self):
        """Ensure required NLTK datasets are available."""
        required_packages = ['punkt', 'wordnet', 'stopwords', 'omw-1.4', 'punkt_tab']
        for package in required_packages:
            try:
                nltk.download(package, quiet=True)
            except Exception as e:
                print(f"Failed to download {package}: {e}")

    def _preprocess(self, text):
        """Lowercase, tokenize, remove stopwords, and lemmatize."""
        # 1. Lowercase and tokenize
        tokens = nltk.word_tokenize(text.lower())
        
        # 2. Remove stopwords & 3. Lemmatize
        lemmas = []
        for word in tokens:
            if word not in self.stop_words and word.isalnum():
                lemmas.append(self.lemmatizer.lemmatize(word))
                
        return " ".join(lemmas)

    def _train(self):
        """Prepare data and fit the TF-IDF vectorizer."""
        processed_patterns = []
        
        # Extract and preprocess patterns
        for intent_dict in INTENTS:
            intent_name = intent_dict["intent"]
            for pattern in intent_dict["patterns"]:
                self.intent_labels.append(intent_dict) # Keep reference to the full intent dict
                self.patterns.append(pattern)
                processed_patterns.append(self._preprocess(pattern))
                
        if not processed_patterns:
            print("Warning: No intents found for training.")
            return

        # Fit vectorizer
        self.X_train = self.vectorizer.fit_transform(processed_patterns)
        self.is_ready = True

    def get_response(self, user_message):
        """Calculate similarity and return the best response."""
        if not self.is_ready:
            return "Bot is still initializing, please wait!"

        user_processed = self._preprocess(user_message)
        
        # If the input was entirely stopwords (e.g. "is it"), processed string might be empty.
        # Fallback to the original tokens if empty, or just predict on empty (will yield low confidence).
        if not user_processed:
            user_processed = user_message.lower()

        # Vectorize user input
        user_vector = self.vectorizer.transform([user_processed])

        # Calculate Cosine Similarity
        similarities = cosine_similarity(user_vector, self.X_train)
        
        # Find the best match
        best_match_index = np.argmax(similarities)
        best_confidence = similarities[0][best_match_index]

        # Check threshold
        if best_confidence < self.confidence_threshold:
            return random.choice(FALLBACK_RESPONSES)
            
        # Get matching intent
        matched_intent = self.intent_labels[best_match_index]
        
        # Return a random response from the matched intent
        return random.choice(matched_intent["responses"])

# Create a singleton instance to be imported by app.py
nlp = NLPEngine(confidence_threshold=0.4)
