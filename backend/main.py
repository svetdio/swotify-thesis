import pickle
import pandas as pd
from pandasql import sqldf
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Union
import json

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import OneHotEncoder, StandardScaler, OrdinalEncoder
from sklearn.compose import make_column_selector, make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer

from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

# Instatiate the FastAPI class
app = FastAPI()

# Enable CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set the input structure for the predict method
class PredictionInput(BaseModel):
    responsibility_rating: int
    team_communication_rating: int
    task_delegation_rating: int
    calmness_rating: int
    adaptability_rating: int
    attitude_rating: int
    comm_collab_rating: int
    external_resp_rating: int
    time_management_rating: int
    collab_rating: int
    flexible_rating: int
    accountability_rating: int
    comment_feedback: str
    event_contribution: str

# Fetch and load the models
knn_model = pickle.load(open('models/init_knn_model.pkl', 'rb'))
svc_model = pickle.load(open('models/tuned_svc_model.pkl', 'rb'))
xgb_model = pickle.load(open('models/tuned_xgb_model.pkl', 'rb'))

sia = SentimentIntensityAnalyzer()

# Set pandasql
pysqldf = lambda q: sqldf(q, globals())
swotify = pd.read_csv('data/2023_LocalCAF_Swotify.csv', encoding='utf-8')

@app.post("/predict")
async def predict(ratings: PredictionInput):
    performance_ratings = {
        "responsibility_rating" : ratings.responsibility_rating,
        "team_communication_rating" : ratings.team_communication_rating,
        "task_delegation_rating" : ratings.task_delegation_rating,
        "calmness_rating" : ratings.calmness_rating,
        "adaptability_rating" : ratings.adaptability_rating,
        "attitude_rating" : ratings.attitude_rating,
        "comm_collab_rating" : ratings.comm_collab_rating,
        "external_resp_rating" : ratings.external_resp_rating,
        "time_management_rating" : ratings.time_management_rating,
        "collab_rating" : ratings.collab_rating,
        "flexible_rating" : ratings.flexible_rating,
        "accountability_rating" : ratings.accountability_rating,
    }

    perf_rating_df = pd.DataFrame([performance_ratings])
    
    knn_prediction = knn_model.predict(perf_rating_df)[0]
    svc_prediction = svc_model.predict(perf_rating_df)[0]
    xgb_prediction = xgb_model.predict(perf_rating_df)[0]

    cf_scores = sia.polarity_scores(ratings.comment_feedback)
    ec_scores = sia.polarity_scores(ratings.event_contribution)
    final_score = (cf_scores['compound'] + ec_scores['compound']) / 2

    sentiment_cls = "NEUTRAL"

    if final_score >= 0.05:
        sentiment_cls = "POSITIVE"
    elif final_score <= -0.05:
        sentiment_cls = "NEGATIVE"

    return {
        "knn_prediction": int(knn_prediction),
        "svc_prediction": int(svc_prediction),
        "xgb_prediction": int(xgb_prediction),
        "sentiment_class": sentiment_cls,
        "sentiment_score": final_score,
        "cf_scores": cf_scores,
        "ec_scores": ec_scores,
    }

@app.get('/get_officers_names')
async def get_officers_names(keyword: Union[str, None] = None):

    q = """
        SELECT DISTINCT evaluatee AS officers FROM swotify 
    """

    if keyword is not None:
        q = f"""
            SELECT DISTINCT evaluatee AS officers FROM swotify WHERE evaluatee LIKE '%{keyword}%'
        """
    return pysqldf(q).to_dict()

    
@app.get('/get_sentiment_values/{evaluatee}')
async def get_dashboard_values(evaluatee: Union[str, None] = None):
    if evaluatee is None:
        return {'values' : []}
    else:
        q = f"""
            SELECT 
                COUNT(*) total_eval_received,
                COUNT(IIF(sentiment = 'Positive', 1, NULL)) positive_sentiment,
                COUNT(IIF(sentiment = 'Neutral', 1, NULL)) neutral_sentiment,
                COUNT(IIF(sentiment = 'Negative', 1, NULL)) negative_sentiment
            FROM swotify
            WHERE evaluatee = '{evaluatee}'
        """
        return pysqldf(q).to_dict(orient="records")[0]
    

@app.get('/get_performance_rating/{evaluatee}')
async def get_performance_rating(evaluatee: Union[str, None] = None):
    if evaluatee is None:
        return {'values' : []}
    else:
        q = f"""
            SELECT 
                AVG(responsibility_rating) responsibility_rating,
                AVG(team_communication_rating) team_communication_rating,
                AVG(task_delegation_rating) task_delegation_rating,
                AVG(calmness_rating) calmness_rating,
                AVG(adaptability_rating) adaptability_rating,
                AVG(attitude_rating) attitude_rating,
                AVG(comm_collab_rating) comm_collab_rating,
                AVG(external_resp_rating) external_resp_rating,
                AVG(time_management_rating) time_management_rating,
                AVG(collab_rating) collab_rating,
                AVG(flexible_rating) flexible_rating,
                AVG(accountability_rating) accountability_rating
            FROM swotify
            WHERE evaluatee = '{evaluatee}'
        """
        return pysqldf(q).to_dict(orient="records")[0]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)