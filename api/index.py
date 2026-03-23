from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
import os
import sys

# Ensure src modules are locally discoverable
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))

try:
    from live_scores import get_live_matches
except Exception:
    def get_live_matches(): return [{"title": "API Error", "score": "Unavailable", "status": ""}]

app = FastAPI(title="IPL Stats API")

from fastapi.responses import FileResponse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "rf_model.pkl")
COLS_PATH = os.path.join(BASE_DIR, "models", "model_columns.pkl")
LE_PATH = os.path.join(BASE_DIR, "models", "label_encoder.pkl")
DATA_PATH = os.path.join(BASE_DIR, "data", "matches.csv")

@app.get("/")
@app.get("/api")
@app.get("/api/")
def serve_frontend():
    try:
        return FileResponse(os.path.join(BASE_DIR, "index.html"))
    except Exception:
        return {"status": "OK", "message": "IPL Stats API is running gracefully."}

class PredictionRequest(BaseModel):
    team1: str
    team2: str
    toss_winner: str
    toss_decision: str
    venue: str

@app.get("/api/options")
@app.get("/options")
def get_options():
    try:
        df = pd.read_csv(DATA_PATH)
        teams = sorted([str(t).strip() for t in df['team1'].dropna().unique() if str(t).strip() != ''])
        venues = sorted([str(v).strip() for v in df['venue'].dropna().unique() if str(v).strip() != ''])
        return {"teams": teams, "venues": venues}
    except Exception as e:
        return {"teams": ["Chennai Super Kings", "Mumbai Indians", "Royal Challengers Bangalore"], "venues": ["Wankhede Stadium", "Eden Gardens"]}

@app.get("/api/live")
@app.get("/live")
def get_live():
    return get_live_matches()

@app.post("/api/predict")
@app.post("/predict")
def predict(request: PredictionRequest):
    if not os.path.exists(MODEL_PATH):
        return {"error": "Predictive model not trained yet", "winner": "Model Missing", "confidence": 0.0}
        
    model = joblib.load(MODEL_PATH)
    model_columns = joblib.load(COLS_PATH)
    le = joblib.load(LE_PATH)
    
    input_df = pd.DataFrame([{
        'team1': request.team1,
        'team2': request.team2,
        'toss_winner': request.toss_winner,
        'toss_decision': request.toss_decision,
        'venue': request.venue
    }])
    
    input_encoded = pd.get_dummies(input_df)
    input_encoded = input_encoded.reindex(columns=model_columns, fill_value=0)
    
    prediction = model.predict(input_encoded)
    probability = model.predict_proba(input_encoded)[0]
    predicted_winner = le.inverse_transform(prediction)[0]
    
    winner_index = list(le.classes_).index(predicted_winner)
    win_prob = probability[winner_index] * 100
    
    return {
        "winner": predicted_winner,
        "confidence": float(win_prob)
    }
