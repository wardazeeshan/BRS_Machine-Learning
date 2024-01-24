# Importing necessary libraries and modules from Flask
from flask import Flask, render_template, request
import pickle
import pandas as pd
import numpy as np

# Loading preprocessed data files using pickle
new_df = pickle.load(open("new.pkl", 'rb'))

# Creating a dataframe from the loaded dictionary
popular = pd.DataFrame(new_df)

# Loading additional data files using pickle
table = pickle.load(open("table.pkl", "rb"))
pt = pd.DataFrame(table)
books = pickle.load(open("books.pkl", "rb"))
book = pd.DataFrame(books)
score = pickle.load(open("score.pkl", "rb"))

# Creating a Flask web application
app = Flask(__name__)

# Route for the home page
@app.route('/')
def index():
    # Rendering the home page with data from the 'popular' dataframe
    return render_template('index.html',
                           book_name=list(popular['Book-Title'].values),
                           author=list(popular['Book-Author'].values),
                           image=list(popular['Image-URL-M'].values),
                           votes=list(popular['num_ratings'].values),
                           rating=list(popular['avg_ratings'].values)
                           )

# Route for the recommendation page UI
@app.route('/recommend')
def recommend_ui():
    # Rendering the recommendation page
    return render_template('recommend.html')

# Route for handling book recommendations based on user input
@app.route('/recommend_books', methods=["POST"])
def recommend():
    # Getting user input from the form
    user_input = request.form.get('user_input')
    
    # Finding the index of the user input in the 'pt' dataframe
    index = np.where(pt.index == user_input)[0][0]
    
    # Finding similar items based on the user input
    similar_item = sorted(list(enumerate(score[index])), key=lambda x: x[1], reverse=True)[1:6]
    
    # Creating a list to store recommended book information
    data = []
    
    # Looping through similar items and retrieving book details
    for i in similar_item:
        item = []
        temp_df = book[book['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        data.append(item)
        print(data)

    # Rendering the recommendation page with the obtained data
    return render_template('recommend.html', data=data)

# Running the Flask application if this script is the main module
if __name__ == '__main__':
    app.run(debug=True)
