import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os

from data_loader import load_with_pandas

def train_and_save_model():
    data_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "matches.csv")
    
    print("Loading data...")
    df = load_with_pandas(data_file)
    
    # Feature engineering for Machine Learning
    features = ['team1', 'team2', 'toss_winner', 'toss_decision', 'venue']
    
    # Standardize data format (One-Hot Encoding for categorical variables)
    X = pd.get_dummies(df[features])
    
    # Encode Target Variable (winner)
    le = LabelEncoder()
    y = le.fit_transform(df['winner'])
    
    # Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest Classifier model...")
    rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    rf.fit(X_train, y_train)
    
    # Evaluate
    score = rf.score(X_test, y_test)
    print(f"Model trained successfully! Accuracy: {score:.2f}")
    
    # Save the models and encoders perfectly for the Streamlit App
    models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
    os.makedirs(models_dir, exist_ok=True)
    
    joblib.dump(rf, os.path.join(models_dir, "rf_model.pkl"))
    joblib.dump(X.columns, os.path.join(models_dir, "model_columns.pkl"))
    joblib.dump(le, os.path.join(models_dir, "label_encoder.pkl"))
    print(f"Models saved into {models_dir}")
    
if __name__ == "__main__":
    train_and_save_model()
