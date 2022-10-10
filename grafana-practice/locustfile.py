import time
import random
from locust import HttpUser, task, between


ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

LOGREG_REQUEST_PROBA = 0.4
SWAP_MODEL_PROBA_TIME = 60 * 2


def get_logreg_proba():
    t = int(time.time()) // SWAP_MODEL_PROBA_TIME
    return abs(t % 2 - LOGREG_REQUEST_PROBA)


def generate_name_data():
    model_type = 'cb'
    if random.random() < get_logreg_proba():
        model_type = 'lr'
    n = random.randint(3, 10)
    name = ''.join([random.choice(ALPHABET) for _ in range(n)])
    return {
        'name': name,
        'model_type': model_type,
    }


class QuickstartUser(HttpUser):
    wait_time = between(0.5, 1)

    @task
    def predict(self):
        self.client.post('/predict_gender/', json=generate_name_data())
