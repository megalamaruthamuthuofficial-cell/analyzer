from flask import Flask, request, jsonify
from flask_cors import CORS
from sentiment import analyze_sentiment
from db import reviews_collection
from scraper import scrape_reviews

app = Flask(__name__)

CORS(app)

# 🏠 Home
@app.route("/")
def home():
    return "Backend Running"

# 🧪 Test API
@app.route("/test")
def test():
    sentiment = analyze_sentiment("This phone is amazing")
    return jsonify({"sentiment": sentiment})

# 🔥 SCRAPE + ANALYZE (FIXED ONLY HERE)
@app.route("/scrape", methods=["POST"])
def scrape():

    try:
        data = request.json
        url = data["url"]

        # FIX 1: pass url correctly
        reviews = scrape_reviews(url)

        for review in reviews:

            sentiment = analyze_sentiment(review)

            reviews_collection.insert_one({
                "product": url,
                "review": review,
                "sentiment": sentiment
            })

        return jsonify({
            "message": "Reviews Scraped and Stored",
            "count": len(reviews)
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


# 📊 DASHBOARD
@app.route("/dashboard")
def dashboard():

    positive = reviews_collection.count_documents(
        {"sentiment": "Positive"}
    )

    negative = reviews_collection.count_documents(
        {"sentiment": "Negative"}
    )

    neutral = reviews_collection.count_documents(
        {"sentiment": "Neutral"}
    )

    return jsonify({
        "positive": positive,
        "negative": negative,
        "neutral": neutral
    })


# 📝 GET ALL REVIEWS
@app.route("/reviews")
def reviews():

    data = list(
        reviews_collection.find(
            {},
            {"_id": 0}
        )
    )

    return jsonify(data)


# 🔍 GET BY PRODUCT
@app.route("/reviews/<product>")
def get_reviews(product):

    data = list(
        reviews_collection.find(
            {"product": product},
            {"_id": 0}
        )
    )

    return jsonify(data)


# 🤖 ANALYZE TEXT
@app.route("/analyze", methods=["POST"])
def analyze():

    try:
        data = request.json
        review = data["review"]

        sentiment = analyze_sentiment(review)

        return jsonify({
            "sentiment": sentiment
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)