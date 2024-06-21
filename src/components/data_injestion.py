from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
from src.components.data_transformation import Data_Transformation
from src.components.model_training import Model_Training
import pandas as pd
import sys
import os

@dataclass
class Data_Injestion_Config:
    data_injestion_config_path = os.path.join('artifacts','movie_df.csv')

class Data_Injestion:
    def __init__(self):
        self.data_path = Data_Injestion_Config()
    
    def initiate_data_injestion(self):
        try:
            movie_df = pd.read_csv('./data/movies.csv')
            logging.info('Read the movie data set')
            movie_df = movie_df.loc[:,['id','title','genre','overview']]
            movie_df['tags'] = (movie_df['genre'] +' '+ movie_df['overview'])
            movie_df.drop(['genre','overview'],axis=1,inplace=True)
            movie_df.dropna(inplace=True)
            os.makedirs(os.path.dirname(self.data_path.data_injestion_config_path),exist_ok=True)
            movie_df.to_csv(self.data_path.data_injestion_config_path,index=False,header=True)
            logging.info('Movie data set created (with selected columns)')
            return(
                self.data_path.data_injestion_config_path
            )
        except Exception as e:
            raise CustomException(e,sys)

if __name__ == '__main__':
    data_injestion_obj = Data_Injestion()
    data_path = data_injestion_obj.initiate_data_injestion()
    data_transformation_obj = Data_Transformation()
    preprocessed_data_path = data_transformation_obj.initiate_data_transformation(data_path)
    model_training_obj = Model_Training()
    model_path = model_training_obj.initiate_model_training(preprocessed_data_path)
    print(model_path)

