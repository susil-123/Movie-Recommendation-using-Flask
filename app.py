from flask import Flask,request,url_for,render_template
from src.pipeline.predict import get_top_6
import json
import urllib.parse

app = Flask(__name__)

@app.route('/',methods=['GET'])
def index_page():
    return render_template('index.html')

@app.route('/recommend_page/')
def recommend_page():
    movie_name = request.args.get('movie_name')
    movie_name = urllib.parse.unquote(movie_name)
    obj = get_top_6()
    result = obj.output_movie(movie_name)
    return render_template('main.html',result = result)

if __name__ ==  '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
