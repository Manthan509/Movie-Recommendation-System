import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
# Load datasets
movies = pd.read_csv(r"D:\Movie recommender\ml-latest\movies.csv")
ratings = pd.read_csv(r"D:\Movie recommender\ml-latest\ratings.csv")
tags = pd.read_csv(r"D:\Movie recommender\ml-latest\tags.csv")

# Display first 5 rows
print("Movies:")
print(movies.head())

print("\nRatings:")
print(ratings.head())

print("\nTags:")
print(tags.head())

# Display shape of datasets
print("\nMovies shape:", movies.shape)
print("Ratings shape:", ratings.shape)
print("Tags shape:", tags.shape)

# Display column names
print("\nMovies columns:")
print(movies.columns)

print("\nRatings columns:")
print(ratings.columns)

print("\nTags columns:")
print(tags.columns)

# Replace missing genres with empty string
movies["genres"] = movies["genres"].fillna("")

# Display first 5 genre entries
print("\nGenres:")
print(movies["genres"].head())
# Create TF-IDF object
tfidf = TfidfVectorizer(stop_words='english')

# Convert genres into numerical vectors
tfidf_matrix = tfidf.fit_transform(movies["genres"])

# Display shape of TF-IDF matrix
print("\nTF-IDF Matrix Shape:")
print(tfidf_matrix.shape)

def recommend(movie_name, top_n=10):

    matches = movies[movies["title"].str.contains(movie_name,
                                                  case=False,
                                                  na=False,
                                                  regex=False)]

    if matches.empty:
        print("Movie not found!")
        return

    idx = matches.index[0]

    cosine_sim = linear_kernel(tfidf_matrix[idx], tfidf_matrix).flatten()

    sim_scores = list(enumerate(cosine_sim))
    sim_scores = sorted(sim_scores,
                        key=lambda x: x[1],
                        reverse=True)

    sim_scores = sim_scores[1:top_n+1]

    print("\nRecommendations for:", movies.iloc[idx]["title"])
    print("-"*50)

    for i, score in sim_scores:
        print(movies.iloc[i]["title"])

while True:

    movie_name = input("\nEnter movie name (or type exit): ")

    if movie_name.lower() == "exit":
        break

    recommend(movie_name)
