from http import client
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/movie", methods=["POST"])
def movie_post():
    url_recieve = request.form['url_give']
    star_recieve = request.form['star_give']
    comment_recieve = request.form['comment_give']
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_recieve, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    og_description = soup.select_one('meta[property="og:description"]')

    image = og_image['content']
    title = og_title['content']
    desc = og_description['content']
    doc = {
        'image' : image,
        'title' : title,
        'description' : desc,
        'star' : star_recieve,
        'comment' : comment_recieve,
    }
    db.movie.insert_one(doc)
    return jsonify({'msg':'POST request!'})

@app.route("/movie", methods=["GET"])
def movie_get():
    movie_lisr = list(db.movies.find({}, {'_id': False}))
    return jsonify({'movies':'movie list'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True) 