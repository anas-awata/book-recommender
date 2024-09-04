from flask import Flask, abort, render_template, request, url_for, flash, redirect
from flask_login import current_user
from Main import form
from Main.models import Favorite
from form import FavoriteForm, RegistrationForm, LoginForm, BookForm, UploadBook, Contact, DeleteBook
from recomm import recom, recom_by_favorites
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
import os
import pandas as pd
import numpy as np
from flask_table import Table, Col
from flask_migrate import Migrate

class Results(Table):
    id = Col('Id', show=False)
    title = Col('TOP RECOMMENDATIONS')

app=Flask(__name__)

SECRET_KEY = "5791628bb0b13ce0c676dfde280ba245"
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

posts = [
	{
	'author' : 'Eshita Jain',
	'title' : 'International Institute of Information Technology'
	}
]

@app.route("/")
@app.route("/home")
def home():
	return render_template('home.html',posts=posts,title="Home")


@app.route("/about")
def about():
	return render_template('about.html',posts=posts,title="About")


@app.route("/register", methods=['GET','POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(f'Account Created for { form.username.data } !', 'success')
		return redirect(url_for('home'))
	return render_template('register.html',title='Register',form=form)


@app.route("/login", methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if form.email.data == 'admin@blog.com' and form.password.data == 'password':
			flash(f'You have been logged in !', 'success')
			return redirect(url_for('home'))
		else:
			flash(f'Login Unsuccessful. Please check login details again.', 'danger')
	return render_template('login.html',title='Login',form=form)


@app.route("/recommender",methods=['GET','POST'])
def recommender():
	form=BookForm()
	df=pd.read_csv('Book.csv')
	if form.validate_on_submit():
		if form.bookname.data in list(df['Title']):
			flash(f'Here are the following recommendations for you', 'success')
			isbn=[]
			year=[]
			publisher=[]
			final_list=[]
			book=form.bookname.data
			output, index = recom(book)
			for i in index:
				isbn.append(df["ISBN"][i-1])
				year.append(df["Year"][i-1])
				publisher.append(df["Publisher"][i-1])
			for i in range(len(index)):
				temp=[]
				temp.append(output[i])
				temp.append(isbn[i])
				temp.append(year[i])
				temp.append(publisher[i])
				final_list.append(temp)
		
			return render_template('recommender.html',title='Recommender',form=form,final=final_list)
		else:
			flash(f'Name not clearly mentioned or does not exist in the database. Please try again.', 'danger')
			return redirect(url_for('recommender'))
	return render_template('recommender.html',title='Recommender',form=form)

@app.route("/uploadbook",methods=['GET','POST'])
def uploadbook():
	form=UploadBook()
	df=pd.read_csv('Book.csv')
	if form.validate_on_submit():
		flash(f'Book Uploaded Succesfully', 'success')
		return redirect(url_for('home'))
	return render_template('uploadbook.html',title='Upload Book',form=form)


@app.route("/contact",methods=['GET','POST'])
def contact():
	form=Contact()
	if form.validate_on_submit():
		flash(f'Query Submission Succesful', 'success')
		return redirect(url_for('contact'))
	return render_template('contact.html',title='Upload Book',form=form)


@app.route("/deletebook",methods=['GET','POST'])
def deletebook():
	form=DeleteBook()
	if form.validate_on_submit():
		flash(f'Book is Deleted', 'success')
		return redirect(url_for('home'))
	return render_template('deletebook.html',title='Delete Book',form=form)


@app.route("/account")
def account():
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', title='Account',image_file=image_file, form=form)

@app.route("/add_favorite", methods=['POST'])
def add_favorite():
    isbn = request.form.get('isbn')
    title = request.form.get('title')
    author = request.form.get('author')
    publisher = request.form.get('publisher')
    image_url = request.form.get('image_url')
    year = request.form.get('year')  # Get the year from the form
    if isbn and title and author and publisher and image_url and year:
        favorite = Favorite(isbn=isbn, title=title, author=author, publisher=publisher, image_url=image_url, year=year, user_id=current_user.id)
        db.session.add(favorite)
        db.session.commit()
        flash('Book added to your favorites!', 'success')
    else:
        flash('Failed to add the book to favorites. Please try again.', 'danger')
    return redirect(url_for('home'))
@app.route("/favorites")
def favorites():
    user_favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    return render_template('favorites.html', title='Your Favorites', favorites=user_favorites)

@app.route("/delete_favorite/<int:favorite_id>", methods=['POST'])
def delete_favorite(favorite_id):
    favorite = Favorite.query.get_or_404(favorite_id)
    if favorite.user_id != current_user.id:
        abort(403)
    db.session.delete(favorite)
    db.session.commit()
    flash('Book removed from your favorites!', 'success')
    return redirect(url_for('favorites'))

@app.route("/user_recommendation")
def recommend_by_favorites():
    user_id = current_user.id
    recommended_books = recom_by_favorites(user_id)
    if isinstance(recommended_books, str):  # In case of an error message
        flash(recommended_books, 'danger')
        return redirect(url_for('home'))
    return render_template('user_recommendation.html', title='Recommended Books', final=recommended_books)

if __name__ == '__main__':
	app.run(debug=True)