import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from surprise import Dataset, Reader

# Load datasets
movies = pd.read_csv(r"D:\Movie recommender\ml-latest\movies.csv")
ratings = pd.read_csv(r"D:\Movie recommender\ml-latest\ratings.csv")

# Use first million ratings for faster processing
ratings = ratings.head(1000000)

# Fill missing genres
movies["genres"] = movies["genres"].fillna("")

# Create TF-IDF matrix
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies["genres"])

# Create Surprise dataset (needed for consistency)
reader = Reader(rating_scale=(0.5, 5))

data = Dataset.load_from_df(
    ratings[['userId', 'movieId', 'rating']],
    reader
)

model = joblib.load(r"D:\Movie recommender\svd_model.pkl")

print("Model loaded successfully!")

# Hybrid Recommendation Function
def hybrid_recommend(movie_name, user_id=1, top_n=10):

    # Find movie
    matches = movies[movies["title"].str.contains(
        movie_name,
        case=False,
        na=False,
        regex=False
    )]

    if matches.empty:
        return []

    idx = matches.index[0]

    # Calculate similarity
    cosine_sim = linear_kernel(
        tfidf_matrix[idx],
        tfidf_matrix
    ).flatten()

    # Get similarity scores
    sim_scores = list(enumerate(cosine_sim))

    sim_scores = sorted(
        sim_scores,
        key=lambda x: x[1],
        reverse=True
    )

    # Top 50 similar movies (excluding itself)
    sim_scores = sim_scores[1:51]

    results = []

    # Combine similarity score and SVD prediction
    for i, similarity_score in sim_scores:

        movie_id = movies.iloc[i]['movieId']

        # Predict rating using SVD
        pred = model.predict(user_id, movie_id)

        predicted_rating = pred.est

        # Normalize rating to 0-1 scale
        normalized_rating = predicted_rating / 5

        # Final hybrid score
        final_score = (
            0.5 * similarity_score
            +
            0.5 * normalized_rating
        )

        results.append(
            (
                movies.iloc[i]['title'],
                final_score
            )
        )

    # Sort by final score
    results = sorted(
        results,
        key=lambda x: x[1],
        reverse=True
    )

    # Return top recommendations
    return results[:top_n]
