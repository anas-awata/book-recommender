# Book-Recommendation-System

Book Recommender - A book Recomemder for all the book lovers out their .To save thier time and easily provide them their Favorite books based on the genre they prefer to read, most liked content and the books that are highly rated by the users.

Book Recommender is a simple yet powerfull web app made using flask framework to recommed your favourate book using content based filtering and cosine similarity metrices.

Front-end : Developed using HTML and CSS.

Back-end : Flask Framework.

How to run ?

Steps:

1. Clone the repositary in your local device.
2. Install all the requirements using :

`pip install -r requirements.txt`

4. Now simply run the server in terminal using
  
`python run.py`

# ALGORITHMS USED

* CONTENT BASED FILTERING:
Content based recommender systems take into account the data provided by the user both directly or indirectly. For example, age can be used to determine classes of products or items reviewed or bought by the user. This type of recommender system relies on characteristics of object. New content can be quickly recommended to the user. These type of systems does not take into account behavior/ data about other users in the systems but here things are little changed.

* COSINE SIMILARITY:
Cosine similarity is a metric used to measure how similar the documents are irrespective of their size. Mathematically, it measures the cosine of the angle between two vectors projected in a multi-dimensional space. The cosine similarity is advantageous because even if the two similar documents are far apart by the Euclidean distance (due to the size of the document), chances are they may still be oriented closer together. The smaller the angle, higher the cosine similarity.

Similarity Score :

How does it decide which item is most similar to the item user likes? Here come the similarity scores.

It is a numerical value ranges between zero to one which helps to determine how much two items are similar to each other on a scale of zero to one. This similarity score is obtained measuring the similarity between the text details of both of the items. So, similarity score is the measure of similarity between given text details of two items. This can be done by cosine-similarity.



 
