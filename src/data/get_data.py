from kaggle.api.kaggle_api_extended import KaggleApi

Q_SCORES_1 = "volpatto/coffee-quality-database-from-cqi"
Q_SCORES_2 = "erwinhmtang/coffee-quality-institute-reviews-may2023"

api = KaggleApi()
api.authenticate()

def get_kaggle_datasets(url: str):

