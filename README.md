# 🏏 IPL Stats Analyser & Predictor

An advanced, serverless-ready data analytics and machine learning application designed to predict Indian Premier League (IPL) match outcomes and provide real-time updates.

## 🚀 Overview
The **IPL Stats Analyser** bridges Big Data Analytics and Machine Learning to give cricket franchises a competitive edge during matches and tactical selection. This project has been entirely built to operate natively on **Vercel** via a fast, decoupled architecture.

### Key Features
- **Predictive Analytics Engine**: Uses a highly trained **Scikit-Learn Random Forest Classifier** to accurately determine a match winner based on historical matchup data, toss decisions, and venues.
- **Vercel Serverless Backend**: Powered by **FastAPI** (`api/index.py`), which seamlessly turns the robust predictive Python engine into a lightweight serverless API.
- **Real-Time Live Hub**: A dedicated dashboard tab scraped in real-time utilizing **BeautifulSoup4** to fetch live scores directly from international broadcasts without requiring costly API keys.
- **Dataset Synchronization**: The `src/data_updater.py` utility elegantly downloads the authoritative historical Kaggle dataset straight from verified GitHub mirror repositories, enabling the ML models to continuously learn from the most verified data.
- **Blazing Fast Frontend**: A completely custom HTML/JS interface (`index.html`) that eliminates the need for heavy WebSockets in favor of fast asynchronous REST API queries.

## 🛠️ Tech Stack
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend API framework**: FastAPI, Uvicorn, Pydantic 
- **Machine Learning Core**: Scikit-Learn (Random Forest classification), Pandas, Joblib
- **Big Data Handling**: PySpark & Pandas data pipeline operations
- **Web Scraping**: BeautifulSoup4, Requests, lxml

## 💻 Local Development Setup
To boot up the project on your own machine and test the Machine Learning models:

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd ipl-stats-analyser
   ```

2. **Install all dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the local backend API server:**
   ```bash
   python -m uvicorn api.index:app --port 8000
   ```
   
4. **Open the Dashboard:** 
   Double-click `index.html` from your file explorer to open it in any web browser. The frontend will dynamically connect to the local API to execute real-time queries.

## ☁️ Deploying to Vercel
Because the project was custom-built with `vercel.json` config settings, deployment is trivial:
1. Push this repository to your **GitHub** account.
2. Visit **Vercel.com** -> Add New Project -> Import your newly pushed Repository.
3. Vercel automatically detects the API functions and deploys the framework in under 3 minutes. 

*(Optional Note: The `models/` directory handles the persistent serialized intelligence for the Random Forest engine. Run `python src/model.py` to retrain the model locally if you ever inject larger datasets or adjust configuration parameters.)*
