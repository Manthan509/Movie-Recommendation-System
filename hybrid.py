import pandas as pd
import joblib
import os
import gdown
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Load movies dataset
movies = pd.read_csv("ml-latest/movies.csv")

# Fill missing genres
movies["genres"] = movies["genres"].fillna("")

# Create TF-IDF matrix
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies["genres"])

# Download SVD model if it doesn't exist
if not os.path.exists("svd_model.pkl"):

    url = "https://drive.google.com/uc?id=1us1EXNR8_fbzQ-QjhqvUylScX2SWYvpD"

    gdown.download(url, "svd_model.pkl", quiet=False)

# Load trained model
model = joblib.load("svd_model.pkl")

print("Model loaded successfully!")

# Hybrid recommendation function
def hybrid_recommend(movie_name, user_id=1, top_n=10):

    # Find movie
    matches = movies[
        movies["title"].str.contains(
            movie_name,
            case=False,
            na=False,
            regex=False
        )
    ]

    if matches.empty:
        return []

    idx = matches.index[0]

    # Content-based similarity
    cosine_sim = linear_kernel(
        tfidf_matrix[idx],
        tfidf_matrix
    ).flatten()

    # Similarity scores
    sim_scores = list(enumerate(cosine_sim))

    sim_scores = sorted(
        sim_scores,
        key=lambda x: x[1],
        reverse=True
    )

    # Exclude itself and take top 50
    sim_scores = sim_scores[1:51]

    results = []

    # Hybrid scoring
    for i, similarity_score in sim_scores:

        movie_id = movies.iloc[i]["movieId"]

        # Predict rating with SVD
        pred = model.predict(user_id, movie_id)

        predicted_rating = pred.est

        # Normalize to 0-1
        normalized_rating = predicted_rating / 5

        # Final hybrid score
        final_score = (
            0.5 * similarity_score
            +
            0.5 * normalized_rating
        )

        results.append(
            (
                movies.iloc[i]["title"],
                final_score
            )
        )

    # Sort by final score
    results = sorted(
        results,
        key=lambda x: x[1],
        reverse=True
    )

    return results[:top_n]