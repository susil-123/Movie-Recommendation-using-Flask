from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
from src.utils import save_obj
import pandas as pd
import sys
import os

@dataclass
class Data_Transformation_Config:
    data_transformation_config_path = os.path.join('artifacts','preprocessed_df.pkl')

class Data_Transformation:
    def __init__(self):
        self.preprocessor_path = Data_Transformation_Config()
    
    def preprocessing(self,text):
        str(text)
        text = text.lower()
        words = word_tokenize(text,language='english')
        words = [lemmatizer.lemmatize(word,pos='v') for word in words if word not in stopwords.words('english')]
        words = [i.replace(',','') for i in words]
        return ' '.join(words)

    def initiate_data_transformation(self,df_path):
        try:
            movie_df = pd.read_csv(df_path)
            logging.info('read movie_df')
            movie_df['tags'] = movie_df['tags'].apply(lambda x:self.preprocessing(x))
            logging.info('preprocessed')
            save_obj(file_path=self.preprocessor_path.data_transformation_config_path,obj=movie_df)
            logging.info('saved the preprocessed data set')
            return (
                self.preprocessor_path.data_transformation_config_path
            )
        except Exception as e:
            raise CustomException(e,sys)

