from nlp_engine import nlp

tests = [
    "Hello there",                   # Expected: greeting
    "What is your name?",            # Expected: identity
    "I need some programming help",  # Expected: programming or help
    "Goodbye my friend",             # Expected: farewell
    "skjdfksjfhskjdfh",              # Expected: fallback (low confidence)
]

print("--- Testing Chatbot Responses ---")
for text in tests:
    response = nlp.get_response(text)
    print(f"User: {text}")
    print(f"Bot: {response}\n")
