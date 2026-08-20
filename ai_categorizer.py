import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "categorizer_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "vectorizer.pkl")

# Expanded dummy data for better training
dummy_data = [
    ("Walmart groceries", "Food"),
    ("Starbucks coffee", "Food"),
    ("McDonalds", "Food"),
    ("Rent payment", "Housing"),
    ("Electric bill", "Utilities"),
    ("Water bill", "Utilities"),
    ("Internet bill", "Utilities"),
    ("Netflix subscription", "Entertainment"),
    ("Spotify", "Entertainment"),
    ("Movie tickets", "Entertainment"),
    ("Gas station", "Transport"),
    ("Uber ride", "Transport"),
    ("Train ticket", "Transport"),
    ("Pharmacy", "Health"),
    ("Doctor visit", "Health"),
    ("Gym membership", "Health"),
    ("Amazon purchase", "Shopping"),
    ("Target", "Shopping"),
    ("Flight to NYC", "Travel"),
    ("Hotel booking", "Travel")
]

def train_and_save_model():
    """Trains a simple NLP model on dummy data and saves it."""
    df = pd.DataFrame(dummy_data, columns=["description", "category"])
    
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df["description"])
    y = df["category"]
    
    model = LogisticRegression()
    model.fit(X, y)
    
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
        
    with open(VECTORIZER_PATH, "wb") as f:
        pickle.dump(vectorizer, f)
        
    return True

def predict_category(description: str) -> str:
    """Predicts the category of an expense based on its description."""
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        train_and_save_model()
        
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
        
    with open(VECTORIZER_PATH, "rb") as f:
        vectorizer = pickle.load(f)
        
    X_new = vectorizer.transform([description])
    prediction = model.predict(X_new)
    return prediction[0]

if __name__ == "__main__":
    train_and_save_model()
    print("Model trained and saved.")
