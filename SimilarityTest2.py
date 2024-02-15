from flask import Flask, jsonify
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import pymongo

app = Flask(__name__)

# Categories (facility-related, product_related and other)
categories = [
    "facility_related",
    "product_related",
    "other",
]

# Create a classifier model using Multinomial Naive Bayes
model = make_pipeline(CountVectorizer(), MultinomialNB())

# Training complaints
training_complaints = [
    "The air conditioning in the waiting area is consistently too cold, making it uncomfortable for visitors.",
    "The conference rooms lack proper audio-visual equipment, hindering effective presentations.",
    "The carpeting in the hallways is worn out and needs replacement to enhance the overall appearance.",
    "The vending machines in the break room frequently malfunction, causing frustration among employees.",
    "The windows in the facility are not soundproof, resulting in disturbances from outside noise.",
    "The new software update has caused frequent crashes and disruptions in our workflow.",
    "The product assembly instructions are incomplete, causing frustration for customers attempting to set it up.",
    "The customer support for the product is unresponsive, leaving users without timely assistance.",
    "The product design does not consider ergonomic principles, leading to discomfort during use.",
    "The product's battery life is significantly shorter than advertised, affecting its overall usability.",
    "The website's customer service chatbot is not providing helpful responses.",
    "The company's return policy is unclear and needs better communication to customers.",
    "The product delivery times are inconsistent and often delayed.",
    "The company's mobile app has compatibility issues with certain devices.",
    "The website's search functionality is ineffective, making it hard to find specific information.",
]

# Corresponding categories for the training complaints
training_categories = [
    "facility_related",
    "facility_related",
    "facility_related",
    "facility_related",
    "facility_related",
    "product_related",
    "product_related",
    "product_related",
    "product_related",
    "product_related",
    "other",
    "other",
    "other",
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
        
        print(f"Complaint {idx}: {complaint}\nCategory: {category}\n")

        # Store complaint and category in MongoDB
        store_in_mongodb(complaint, category)

    # Start the Flask application
    app.run()

client.close()  # Close the MongoDB connection when finished

