import streamlit as st
import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt
import sys

# Ensure src modules are discoverable
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
try:
    from live_scores import get_live_matches
except ImportError:
    get_live_matches = lambda: [{"title": "Live Scores Unavailable", "score": "Missing Module", "status": ""}]

# Configuration
st.set_page_config(page_title="IPL Stats Analyser", page_icon="🏏", layout="wide")

# Setup paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "matches.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "rf_model.pkl")
COLS_PATH = os.path.join(BASE_DIR, "models", "model_columns.pkl")
LE_PATH = os.path.join(BASE_DIR, "models", "label_encoder.pkl")

# --- Authentication Module ---
def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (st.session_state["username"] == "admin" and 
            st.session_state["password"] == "password123"):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.title("🔒 Login to IPL Stats Analyser")
        st.markdown("Please enter your franchise credentials to access the analytics dashboard.")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("Login Form"):
                st.text_input("Username", key="username")
                st.text_input("Password", type="password", key="password")
                submit_button = st.form_submit_button("Login", on_click=password_entered)
        return False
        
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.title("🔒 Login to IPL Stats Analyser")
        st.markdown("Please enter your franchise credentials to access the analytics dashboard.")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("Login Form"):
                st.text_input("Username", key="username")
                st.text_input("Password", type="password", key="password")
                submit_button = st.form_submit_button("Login", on_click=password_entered)
            st.error("😕 User not known or password incorrect")
        return False
        
    else:
        # Password correct.
        return True

# --- Main Application ---
if check_password():
    st.sidebar.success("Logged in as Admin")
    if st.sidebar.button("Logout"):
        del st.session_state["password_correct"]
        st.rerun()
        
    st.title("🏏 IPL Stats Analyser & Outcome Predictor")
    st.markdown("""
    Welcome to the **IPL Stats Analyser**, an intelligent platform bridging **Big Data Analytics** 
    and **Machine Learning** to give franchises a competitive edge during matches and tactical selection.
    """)

@st.cache_data
def load_data():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    return None

    df = load_data()

    if df is not None:
        st.divider()
        
        # Layout with tabs
        tab1, tab2, tab3 = st.tabs(["📊 Data & Insights", "🎯 Match Predictor ML", "🔴 Live Matches"])
        
        with tab1:
            st.header("Historical IPL Data Directory")
            st.dataframe(df, use_container_width=True)
            
            st.subheader("Win Distribution by Teams")
            win_counts = df['winner'].value_counts()
            st.bar_chart(win_counts)

        with tab2:
            st.header("Predictive Analytics Engine")
            st.markdown("Use our trained Machine Learning classification model to predict the winner of upcoming matches.")
            
            if os.path.exists(MODEL_PATH):
                model = joblib.load(MODEL_PATH)
                model_columns = joblib.load(COLS_PATH)
                le = joblib.load(LE_PATH)
                
                # Filter out nulls stringently to avoid UI errors
                valid_teams = [t for t in df['team1'].dropna().unique() if str(t).strip() != '']
                teams = sorted(valid_teams)
                
                valid_venues = [v for v in df['venue'].dropna().unique() if str(v).strip() != '']
                venues = sorted(valid_venues)
                
                with st.container():
                    col1, col2 = st.columns(2)
                    with col1:
                        team1 = st.selectbox("Team 1 (Batting First)", teams)
                        toss_decision = st.selectbox("Toss Decision", ["bat", "field"])
                    with col2:
                        team2 = st.selectbox("Team 2 (Bowling First)", teams, index=min(1, len(teams)-1) if len(teams)>1 else 0)
                        toss_winner = st.selectbox("Toss Winner", [team1, "Team 2"])
                    
                    venue = st.selectbox("Match Venue", venues)
                    
                predict_btn = st.button("Predict Match Outcome", type="primary")
                if predict_btn:
                    if team1 == team2:
                        st.error("Team 1 and Team 2 must be different entities.")
                    else:
                        actual_toss = team1 if toss_winner != "Team 2" else team2
                        input_data = {
                            'team1': team1, 'team2': team2,
                            'toss_winner': actual_toss, 'toss_decision': toss_decision,
                            'venue': venue
                        }
                        
                        # Preprocess for the model
                        input_df = pd.DataFrame([input_data])
                        input_encoded = pd.get_dummies(input_df)
                        input_encoded = input_encoded.reindex(columns=model_columns, fill_value=0)
                        
                        # Predict Output
                        prediction = model.predict(input_encoded)
                        probability = model.predict_proba(input_encoded)[0]
                        predicted_winner = le.inverse_transform(prediction)[0]
                        
                        winner_index = list(le.classes_).index(predicted_winner)
                        win_prob = probability[winner_index] * 100
                        
                        st.success(f"### 🏆 Predicted Winner: **{predicted_winner}**")
                        st.info(f"Model Confidence: **{win_prob:.1f}%**")
                        st.balloons()
            else:
                st.warning("⚠️ Predictive Model is missing. Please run `python src/model.py` to train the engine.")
                
        with tab3:
            st.header("🔴 Real-Time Match Hub")
            st.markdown("Fetching live cricket scores globally in real-time.")
            
            with st.spinner("Scraping live match data..."):
                matches = get_live_matches()
                
            if not matches:
                st.info("No live matches are currently available or being broadcasted.")
            else:
                for match in matches:
                    with st.expander(match.get('title', 'Live Match'), expanded=True):
                        st.markdown(f"**Score:** {match.get('score', 'Details unavailable')}")
                        st.caption(f"Status: {match.get('status', 'In Progress')}")
                
            st.button("Refresh Scores", type="secondary")
            
    else:
        st.error("No historical IPL data found. Please run `python src/data_updater.py` to fetch the real dataset.")
