from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
from src.utils import save_obj,load_object
import pandas as pd
import sys
import os
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()
from sklearn.metrics.pairwise import cosine_similarity

@dataclass
class Model_Training_config:
    model_path = os.path.join('artifacts','model.pkl')

class Model_Training:
    def __init__(self):
        self.model_training_config = Model_Training_config()

    def initiate_model_training(self,data_path):
        try:
            movie_df = load_object(file_path=data_path)
            logging.info('loaded dataset in model training')

            X = vectorizer.fit_transform(movie_df['tags'])
            logging.info('vectorized the dataset')

            cosine_sim_matrix = cosine_similarity(X, X)
            cosine_df = pd.DataFrame(cosine_sim_matrix,index=movie_df['id'],columns=movie_df['id'])
            logging.info('Calculated cosine similarity of data set')

            save_obj(file_path=self.model_training_config.model_path,obj=cosine_df)
            logging.info('saved the model as pickle file')
            return(
                self.model_training_config.model_path
            )
        except Exception as e:
            raise CustomException(e,sys)