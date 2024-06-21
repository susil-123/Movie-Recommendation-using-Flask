from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
from src.utils import save_obj,load_object
import pandas as pd
import sys
import requests
import os

class get_top_6:
    def __init__(self):
        self.dataset_path = os.path.join('artifacts','preprocessed_df.pkl')
        self.model_path = os.path.join('artifacts','model.pkl')
    def get_movie_url(self,movie_name):
        url = f"http://www.omdbapi.com/?t={movie_name}&apikey=dba30e27"
        try:
            response = requests.get(url)
            data = response.json()
            title = data['Title']
            year = data['Year']
            rated = data['Rated']
            released = data['Released']
            runtime = data['Runtime']
            genre = data['Genre']
            director = data['Director']
            actors = data['Actors']
            plot = data['Plot']
            poster = data['Poster']
            ratings = data['Ratings']
            data_dict = {
                'title': title,
                'year': year,
                'rated': rated,
                'released': released,
                'runtime': runtime,
                'genre': genre,
                'director': director,
                'actors': actors,
                'plot': plot,
                'poster': poster,
                'ratings': ratings
            }
            return data_dict
        except Exception as e:
            raise e
        
    # function to find top 6 based on similarity scores
    def get_top_6_similar_documents(self,doc_id, sim_df):
        sim_scores = sim_df[doc_id]
        top_6_similar = sim_scores.sort_values(ascending=False).iloc[1:7]
        return top_6_similar
    
    # movie to find and recommed movies
    def movie_to_find_api(self,movie_name):
        movie_df = load_object(self.dataset_path)
        cosine_df = load_object(self.model_path)
        movies_api = {}
        movies_api['main_movie'] = self.get_movie_url(movie_name)
        movie_row = movie_df[movie_df['title'].str.contains(movie_name, case=False, regex=True)]
        if not movie_row.empty:
            recommended_movie_list = self.get_top_6_similar_documents(movie_row['id'].iloc[0],cosine_df).index.tolist()
            movies_api['recommendations'] = self.get_movie_list_api(recommended_movie_list,movie_df)
            return movies_api
        else:
            print('results not found')

    def get_movie_list_api(self,recommended_movie_list,movie_df):
        recommended_api_lst = []
        for i in range(len(recommended_movie_list)):
            title = movie_df[movie_df['id'] == recommended_movie_list[i]]['title'].iloc[0]
            data = self.get_movie_url(title)
            recommended_api_lst.append(data)
        return recommended_api_lst
    
    def output_movie(self,movie_name):
        movie_details = self.movie_to_find_api(movie_name)
        main = movie_details['main_movie']
        recommendation = movie_details['recommendations']
        print(f"The movie you asked for: \n\n{main['title']}\nreleased: {main['released']}\ndirected by: {main['director']}",end='\n\n\n')
        print(f"Recommended Movies:\n1 {recommendation[0]['title']} ({recommendation[0]['year']})\n2 {recommendation[1]['title']} ({recommendation[0]['year']})\n3 {recommendation[2]['title']} ({recommendation[0]['year']})\n4 {recommendation[3]['title']} ({recommendation[0]['year']})\n5 {recommendation[4]['title']} ({recommendation[0]['year']})")

    def custom_data(self,movie_name):
        pass