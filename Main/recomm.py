import random
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from Main.models import Favorite,Clicked,WantToRead,ReadBefore

def recom(books_user_likes):
    def get_title_from_index(index):
        try:
            return df[df.index == index]["Title"].values[0]
        except IndexError:
            return None

    def get_index_from_title(Title):
        try:
            return df[df.Title == Title]["index"].values[0]
        except IndexError:
            return None

    books = pd.read_csv("Bookz.csv")
    books = books[:1000]
    df = books.copy()
    img = pd.read_csv("Imagez.csv")

    features = ['Title', 'Author', 'Publisher']
    for feature in features:
        df[feature] = df[feature].fillna('')

    def combine_features(row):
        try:
            return row['Title'] + " " + row['Author'] + " " + row['Publisher']
        except:
            return ''

    df["combined_features"] = df.apply(combine_features, axis=1)

    # Create count matrix from this new combined column
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(df["combined_features"])

    # Compute the Cosine Similarity based on the count_matrix
    cosine_sim = cosine_similarity(count_matrix) 

    # Get index of this book from its title
    books_index = get_index_from_title(books_user_likes)
    if books_index is None:
        return []  # Return an empty list if the book is not found

    similar_books = list(enumerate(cosine_sim[books_index]))

    # Get a list of similar books in descending order of similarity score
    sorted_similar_books = sorted(similar_books, key=lambda x: x[1], reverse=True)

    # Titles of first 10 books
    l = []
    t = []
    i = 0
    for element in sorted_similar_books:
        title = get_title_from_index(element[0])
        if title:
            l.append(title)
            t.append(get_index_from_title(title))
            i += 1
        if i > 9:
            break

    output = l
    index = t

    imgg = []
    year = []
    author = []
    final_list = []

    for i in index:
        if i is not None and i >= 0 and i < len(img):
            imgg.append(img["Image-URL-L"].iloc[i -1] if i < len(img) else '')
            year.append(books["Year"].iloc[i -1] if i < len(books) else '')
            author.append(books["Author"].iloc[i -1] if i < len(books) else '')

    for i in range(len(index)):
        temp = []
        temp.append(output[i])
        temp.append(imgg[i] if i < len(imgg) else '')
        temp.append(year[i] if i < len(year) else '')
        temp.append(author[i] if i < len(author) else '')
        final_list.append(temp)

    return final_list



def bookdisp():
    books = pd.read_csv("Bookz.csv")
    img = pd.read_csv("Imagez.csv")

    title = []
    imgg = []
    year = []
    author = []
    isbn = []
    publisher = []
    finallist = []

    r = np.random.randint(2, 1000, 20)

    for i in r:
        title.append(books["Title"][i-1])
        imgg.append(img["Image-URL-L"][i-1])
        year.append(books["Year"][i-1])
        author.append(books["Author"][i-1])
        isbn.append(books["ISBN"][i-1])
        publisher.append(books["Publisher"][i-1])

    for i in range(20):
        temp = []
        temp.append(title[i])
        temp.append(imgg[i])
        temp.append(year[i])
        temp.append(author[i])
        temp.append(isbn[i])
        temp.append(publisher[i])
        finallist.append(temp)

    return finallist

def recom_by_favorites(user_id):
    user_favorites = Favorite.query.filter_by(user_id=user_id).all()
    if not user_favorites:
        return []

    favorite_titles = [fav.title for fav in user_favorites]
    all_recommendations = []

    for title in favorite_titles:
        recommendations = recom(title)
        for rec in recommendations:
            if rec[0] not in favorite_titles:  # Avoid adding favorite books themselves
                all_recommendations.append(rec)

    # Remove duplicates while maintaining order
    seen = set()
    unique_recommendations = []
    for rec in all_recommendations:
        if rec[0] not in seen:
            unique_recommendations.append(rec)
            seen.add(rec[0])

    # Shuffle the recommendations
    random.shuffle(unique_recommendations)

    return unique_recommendations[:10]


def recommend_books(user_id):
    # Fetch user-related data
    clicked_books = Clicked.query.filter_by(user_id=user_id).all()
    want_to_read_books = WantToRead.query.filter_by(user_id=user_id).all()
    read_before_books = ReadBefore.query.filter_by(user_id=user_id).all()
    favorite_books = Favorite.query.filter_by(user_id=user_id).all()

    # Create a dictionary to store book scores
    book_scores = {}

    # Add scores from Clicked table
    for book in clicked_books:
        book_scores[book.title] = book.count

    # Add scores for WantToRead books
    for book in want_to_read_books:
        if book.title in book_scores:
            book_scores[book.title] += 4
        else:
            book_scores[book.title] = 4

    # Add scores for ReadBefore books
    for book in read_before_books:
        if book.title in book_scores:
            book_scores[book.title] += 5
        else:
            book_scores[book.title] = 5

    # Add scores for Favorite books
    for book in favorite_books:
        if book.title in book_scores:
            book_scores[book.title] += 6
        else:
            book_scores[book.title] = 6

    # Generate recommendations and associate them with their scores
    recommendations_with_scores = []

    for title, score in book_scores.items():
        recommendations = recom(title)
        for rec in recommendations:
            # Store recommendations with the score of the book they were recommended by
            recommendations_with_scores.append((rec, score))

    # Sort recommendations by the score of the book that generated them
    sorted_recommendations = sorted(recommendations_with_scores, key=lambda x: x[1], reverse=True)
    
    # Remove duplicates while maintaining order
    seen = set()
    unique_recommendations = []
    for rec, _ in sorted_recommendations:
        if rec[0] not in seen:
            unique_recommendations.append(rec)
            seen.add(rec[0])

    return unique_recommendations[:10]
