from flask import Flask, jsonify
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import pymongo

app = Flask(__name__)

# Categories (facility-related and other)
categories = [
    "facility_related",
    "other",
]

# Create a classifier model using Multinomial Naive Bayes
model = make_pipeline(CountVectorizer(), MultinomialNB())

# Training complaints
training_complaints = [
    "The stairs are too steep and dangerous.",
    "The restroom is not clean and needs maintenance.",
    "The elevator is out of order.",
    "The parking lot is always full.",
    "The chairs in the waiting area are uncomfortable.",
    "The lighting in the hallways is too dim.",
    # Add more training complaints here...
    "Some other complaint not related to specific facilities.",
    "Another generic complaint.",
]

# Corresponding categories for the training complaints
training_categories = [
    "facility_related",
    "facility_related",
    "facility_related",
    "facility_related",
    "facility_related",
    "facility_related",
    # Add corresponding categories for the remaining complaints...
    "other",
    "other",
]

# Train the model with the training complaints and their respective categories
model.fit(training_complaints, training_categories)

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection string
db = client["projectdb"]  # Replace with your database name
collection = db["complaints"]  # Replace with your collection name

# Function to predict complaint category
def predict_category(complaint):
    predicted_category = model.predict([complaint])
    return predicted_category[0]

# Function to store complaint and category in MongoDB
def store_in_mongodb(complaint, category):
    complaint_data = {
        "complaint": complaint,
        "category": category
    }
    collection.insert_one(complaint_data)


@app.route('/complaints', methods=['GET'])
def get_complaints():
    complaints_data = list(collection.find({}, {'_id': 0}))  # Retrieve all complaints data
    return jsonify(complaints_data), 200


# Process and store complaints only if this script is the main module
if __name__ == "__main__":
    with open('test_complaints.txt', 'r') as file:
        # Use splitlines() to handle different newline characters
        test_complaints = file.read().splitlines()

    # Loop through test complaints and predict category
    for idx, complaint in enumerate(test_complaints, 1):
        category = predict_category(complaint)

        # Store complaint and category in MongoDB
        store_in_mongodb(complaint, category)

    # Start the Flask application
    app.run()

client.close()  # Close the MongoDB connection when finished

