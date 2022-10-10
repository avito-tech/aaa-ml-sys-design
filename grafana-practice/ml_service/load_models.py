import pickle
import catboost


def load_feature_extractor(filename: str):
    with open(filename, 'rb') as fin:
        vectorizer = pickle.load(fin)
    return vectorizer


def load_model(filename: str, is_catboost: bool):
    if is_catboost:
        model = catboost.CatBoostClassifier().load_model(filename)
    else:
        with open(filename, 'rb') as fin:
            model = pickle.load(fin)
    return model
