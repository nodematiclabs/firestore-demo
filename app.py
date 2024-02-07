import json

from flask import Flask, request, render_template
from firebase_admin import credentials, firestore

import firebase_admin

# Initialize Flask app and Firebase admin
app = Flask(__name__)
firebase_admin.initialize_app()

# Initialize the DB
db = firestore.client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-review', methods=['POST'])
def submit_review():
    reviewer_name = request.form['reviewer_name']
    review_text = request.form['review_text']

    # Save the review to Firestore
    db.collection('reviews').add({
        'reviewer_name': reviewer_name,
        'review_text': review_text
    })

    return 'Review submitted successfully!'


@app.route('/reviews')
def show_reviews():
    # Fetch all reviews from Firestore
    reviews = db.collection('reviews').stream()
    reviews_list = [{**review.to_dict(), 'id': review.id} for review in reviews if 'review_text' in review.to_dict().keys()]
    print(json.dumps(reviews_list))

    return render_template('reviews.html', reviews=reviews_list)

if __name__ == '__main__':
    app.run(debug=True)