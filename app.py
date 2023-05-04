# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 20:03:29 2023

@author: User
"""

from flask import Flask,render_template,request
import pickle
import numpy as np
import pandas as pd

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

app = Flask(__name__)

@app.route('/')

def index():
    return render_template('index.html', book_name = list(popular_df['Book-Title'].values), author=list(popular_df['Book-Author'].values), image=list(popular_df['Image-URL-M'].values), votes=list(popular_df['num_ratings'].values), rating=[ '%.2f' % elem for elem in list(popular_df['avg_rating'].values)])

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/search')
def search_ui():
    return render_template('search.html')


@app.route('/recommend_books', methods=['POST'])
def recommend():
    try:
        user_input = request.form.get('user_input')
        
        index = np.where(pt.index==user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:5]
        
        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
            
            data.append(item)
        
        #print(data)
        
        return render_template('recommend.html',data=data)
    except:
        return render_template('nobook.html')

@app.route('/search_books', methods=['POST'])
def search_book():
    try:
        user_input = request.form.get('user_input')
        index = np.where(pt.index==user_input)[0][0]
        print(index)
        similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[0:1]
        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
            
            data.append(item)
        
        
        return render_template('search.html',data=data)
    except:
        return render_template('no_book.html')

if __name__ == '__main__':
    app.run(debug=False)