import os
import time
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
from logging import getLogger
from statsd import StatsClient

from load_models import load_model, load_feature_extractor

logger = getLogger()

CB_KEY = 'cb'
LR_KEY = 'lr'

MODELS_DIR = 'models'
LR_VECTORIZER_PATH = os.path.join(MODELS_DIR, 'logreg_vectorizer.pkl')
CB_VECTORIZER_PATH = os.path.join(MODELS_DIR, 'catboost_vectorizer.pkl')
LR_MODEL_PATH = os.path.join(MODELS_DIR, 'logreg_model.pkl')
CB_MODEL_PATH = os.path.join(MODELS_DIR, 'catboost_model.cb')

feature_extractors = {
    CB_KEY: load_feature_extractor(CB_VECTORIZER_PATH),
    LR_KEY: load_feature_extractor(LR_VECTORIZER_PATH),
}

models = {
    CB_KEY: load_model(CB_MODEL_PATH, is_catboost=True),
    LR_KEY: load_model(LR_MODEL_PATH, is_catboost=False)
}


GRAPHITE_HOST = os.environ.get('GRAPHITE_HOST', None)
GRAPHITE_PORT = os.environ.get('GRAPHITE_PORT', None)
logger.warning(f'graphite url: {GRAPHITE_HOST}, port: {GRAPHITE_PORT}')
statsd = StatsClient(GRAPHITE_HOST, int(GRAPHITE_PORT), prefix='ml_service')


class ModelType(str, Enum):
    cb = CB_KEY
    lr = LR_KEY


class UserRequestIn(BaseModel):
    name: str
    model_type: ModelType = LR_KEY


class Gender(str, Enum):
    f = "f"
    m = "m"


class Prediction(BaseModel):
    name: str
    gender: Gender
    proba: float


app = FastAPI()


@app.post("/predict_gender", response_model=Prediction)
def predict_gender(user_request: UserRequestIn):
    model_type = user_request.model_type
    name = user_request.name
    statsd.incr(f'predict_gender.{model_type}.count')
    if name == 'error':
        statsd.incr(f'predict_gender.request_status.error.count')
        raise KeyError
    model = models[model_type]
    feature_extractor = feature_extractors[model_type]

    tic = time.perf_counter()
    features = np.asarray(feature_extractor.transform([name]).todense())
    toc = time.perf_counter()
    probas = model.predict_proba(features)[0]
    if probas[0] > probas[1]:
        gender = Gender.f
        proba = probas[0]
    else:
        gender = Gender.m
        proba = probas[1]

    statsd.incr(f'predict_gender.{model_type}.result.{gender}.count')
    statsd.gauge(f'predict_gender.{model_type}.result.{gender}.proba', proba)
    statsd.timing(f'predict_gender.{model_type}.timing.feature_extraction', toc - tic)
    statsd.incr(f'predict_gender.request_status.success.count')
    return Prediction(
        name=user_request.name,
        gender=gender,
        proba=proba,
    )
