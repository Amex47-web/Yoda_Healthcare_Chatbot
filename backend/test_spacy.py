import spacy
try:
    nlp = spacy.blank("en")
    print("spaCy imported and initialized successfully")
except Exception as e:
    print(f"Failed: {e}")
