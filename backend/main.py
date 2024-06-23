import warnings
warnings.filterwarnings('ignore')

import os.path
import time
from fastapi.responses import StreamingResponse

import pickle
import pandas as pd
from pandasql import sqldf
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Union
import json
import csv

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

from train import execute_train

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
    evaluatee: str
    position: str
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

# Fetch and load the base models
knn_model = pickle.load(open('models/base/base_knn_model.pkl', 'rb'))
svc_model = pickle.load(open('models/base/base_svc_model.pkl', 'rb'))
xgb_model = pickle.load(open('models/base/base_xgb_model.pkl', 'rb'))
rfc_model = pickle.load(open('models/base/base_rfc_model.pkl', 'rb'))
lr_model = pickle.load(open('models/base/base_lr_model.pkl', 'rb'))

# Fetch best fit CSG trained models
csg_knn_model = pickle.load(open('models/csg/init_knn_model.pkl', 'rb'))
csg_svc_model = pickle.load(open('models/csg/tuned_svc_model.pkl', 'rb'))
csg_xgb_model = pickle.load(open('models/csg/tuned_xgb_model.pkl', 'rb'))

sia = SentimentIntensityAnalyzer()

# Set pandasql
pysqldf = lambda q: sqldf(q, globals())
swotify = pd.read_csv('data/2023_LocalCAF_Swotify.csv', encoding='utf-8')

@app.post("/predict")
async def predict(ratings: PredictionInput, model: Union[str, None] = None ):
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
    
    self_train_prediction = None
    if model is not None:
        self_train_model = pickle.load(open(f'models/retrain/{model}', 'rb'))
        self_train_prediction = int(self_train_model.predict(perf_rating_df)[0])

    
    knn_prediction = knn_model.predict(perf_rating_df)[0]
    svc_prediction = svc_model.predict(perf_rating_df)[0]
    xgb_prediction = xgb_model.predict(perf_rating_df)[0]
    rfc_prediction = rfc_model.predict(perf_rating_df)[0]
    lr_prediction = lr_model.predict(perf_rating_df)[0]

    csg_knn_prediction = csg_knn_model.predict(perf_rating_df)[0]
    csg_svc_prediction = csg_svc_model.predict(perf_rating_df)[0]
    csg_xgb_prediction = csg_xgb_model.predict(perf_rating_df)[0]

    cf_scores = sia.polarity_scores(ratings.comment_feedback)
    ec_scores = sia.polarity_scores(ratings.event_contribution)
    final_score = (cf_scores['compound'] + ec_scores['compound']) / 2

    sentiment_cls = "NEUTRAL"

    if final_score >= 0:
        sentiment_cls = "POSITIVE"
    elif final_score <= 0:
        sentiment_cls = "NEGATIVE"

    ## Saves the inputted data into a csv file for retraining
    save_response(dict(ratings))

    return {
        "knn_prediction": int(knn_prediction),
        "svc_prediction": int(svc_prediction),
        "xgb_prediction": int(xgb_prediction),
        "rfc_prediction": int(rfc_prediction),
        "lr_prediction": int(lr_prediction),
        
        "csg_knn_prediction": int(csg_knn_prediction),
        "csg_svc_prediction": int(csg_svc_prediction),
        "csg_xgb_prediction": int(csg_xgb_prediction),

        "sentiment_class": sentiment_cls,
        "sentiment_score": final_score,
        "cf_scores": cf_scores,
        "ec_scores": ec_scores,
        
        "self_train_prediction": self_train_prediction,
    }


def save_response(ratings):
    data = [ratings]
    fields = list(data[0].keys())
    path = 'data/feedback.csv'
    
    isWriteHeader = False
    if not os.path.isfile(path):
        isWriteHeader = True 
    
    with open(path, 'a', newline='') as file: 
        if isWriteHeader:
            writer = csv.DictWriter(file, fieldnames = fields)
            writer.writeheader() 
            writer.writerows(data)
        else:
            writer = csv.writer(file)
            writer.writerow(list(ratings.values()))


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

        q2 = f"""
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
        """
        return {
            "self" : pysqldf(q).to_dict(orient="records")[0],
            "global": pysqldf(q2).to_dict(orient="records")[0],
        }


@app.get('/get_comments/{evaluatee}')
async def get_comments(evaluatee: Union[str, None] = None):
    q = f"""
            SELECT 
                evaluator,
                comment_feedback,
                event_contribution,
                cf_compound,
                ec_compound
            FROM swotify
            WHERE evaluatee = '{evaluatee}'
        """
    return pysqldf(q).to_dict(orient="records")

@app.get('/train')
async def train(csv_url: Union[str, None] = None):
    return StreamingResponse(execute_train(csv_url), media_type='text/event-stream')


@app.get('/get_models')
async def get_models():
    model_path = "models/retrain/"
    try:
        models = os.listdir(model_path)
    except:
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        models = os.listdir(model_path)
    return models

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)