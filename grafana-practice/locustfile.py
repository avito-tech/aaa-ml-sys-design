import time
import math
import random
from locust import HttpUser, task, between


LOGREG_REQUEST_PROBA = 0.4
MALE_PROBA = 0.45
MODEL_PROBA_PERIOD = 60 * 5
ERROR_PROBA_PERIOD = 60 * 15
GENDER_PROBA_PERIOD = 60 * 8


female_names = ["Mary", "Anna", "Ruth", "Margaret", "Elizabeth", "Helen", "Florence", "Ethel", "Emma", "Bertha",
                "Clara", "Minnie", "Alice", "Edna", "Bessie", "Grace", "Annie", "Ida", "Marie", "Lillian", "Mabel",
                "Hazel", "Rose", "Gertrude", "Martha", "Pearl", "Nellie", "Ella", "Myrtle", "Edith", "Laura", "Eva",
                "Sarah", "Frances", "Elsie", "Carrie", "Louise", "Agnes", "Esther", "Julia", "Lillie", "Catherine", "Hattie",
                "Cora", "Jennie", "Lena", "Mattie", "Jessie", "Maude", "Josephine", "Irene", "Blanche", "Mae", "Alma",
                "Ada", "Lucy", "Lula", "Gladys", "Mamie", "Mildred", "Fannie", "Katherine", "Stella", "Maggie", "Dora",
                "Viola", "Nora", "Dorothy", "Ellen", "Rosa", "Ruby", "Sadie", "May", "Effie", "Nettie", "Della",
                "Willie", "Susie", "Marguerite", "Beulah", "Lydia", "Olive", "Lizzie", "Daisy", "Beatrice", "Pauline",
                "Georgia", "Nancy", "Flora", "Kathryn", "Vera", "Lottie", "Marion", "Sallie", "Emily", "Katie",
                "Virginia", "Etta", "Caroline", "Charlotte"]
male_names = ["John", "William", "James", "George", "Charles", "Joseph", "Frank", "Robert", "Edward", "Harry",
              "Henry", "Thomas", "Walter", "Arthur", "Fred", "Albert", "Clarence", "Roy", "Willie", "Samuel", "Earl",
              "Louis", "Ernest", "Carl", "Paul", "Richard", "David", "Joe", "Raymond", "Charlie", "Ralph", "Elmer",
              "Oscar", "Harold", "Howard", "Jesse", "Will", "Alfred", "Daniel", "Andrew", "Herbert", "Benjamin",
              "Sam", "Herman", "Leo", "Lee", "Frederick", "Francis", "Michael", "Jack", "Lawrence", "Claude",
              "Eugene", "Peter", "Clyde", "Ray", "Lewis", "Edwin", "Floyd", "Tom", "Martin", "Ben", "Edgar", "Homer",
              "Jacob", "Chester", "Grover", "Harvey", "Leonard", "Luther", "Clifford", "Guy", "Otto", "Jim",
              "Russell", "Leroy", "Lester", "Hugh", "Patrick", "Ed", "Anthony", "Eddie", "Alexander", "Bernard",
              "Jessie", "Oliver", "Stanley", "Leon", "Lloyd", "Theodore", "Philip", "Julius", "Archie", "Charley",
              "Leslie", "Bert", "Isaac", "Ira", "Allen", "Percy", "Stephen"]


def get_logreg_proba(time_seconds: int):
    t = 2 * math.pi * time_seconds / MODEL_PROBA_PERIOD
    return (math.sin(t) + 2) / 4


def get_error_proba(time_seconds: int):
    t = 2 * math.pi * time_seconds / ERROR_PROBA_PERIOD
    return (math.sin(t + math.pi / 4) + 1) / 20


def get_male_proba(time_seconds: int):
    t = 2 * math.pi * time_seconds / GENDER_PROBA_PERIOD
    return (math.cos(t) + 2) / 4


def generate_name_data():
    t = int(time.time())
    model_type = 'cb'
    if random.random() < get_logreg_proba(t):
        model_type = 'lr'
    if random.random() < get_error_proba(t):
        name = 'error'
    else:
        if random.random() < get_male_proba(t):
            name = random.choice(male_names)
        else:
            name = random.choice(female_names)
    return {
        'name': name,
        'model_type': model_type,
    }


class QuickstartUser(HttpUser):
    wait_time = between(0.5, 1)

    @task
    def predict(self):
        self.client.post('/predict_gender/', json=generate_name_data())
