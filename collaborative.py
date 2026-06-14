import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise.accuracy import rmse

# Load ratings dataset
ratings = pd.read_csv(r"D:\Movie recommender\ml-latest\ratings.csv")

# Use first 1 million ratings initially
ratings = ratings.head(1000000)

# Define rating scale
reader = Reader(rating_scale=(0.5, 5))

# Convert pandas dataframe into Surprise dataset
data = Dataset.load_from_df(
    ratings[['userId', 'movieId', 'rating']],
    reader
)

# Split into training and testing sets
trainset, testset = train_test_split(
    data,
    test_size=0.2,
    random_state=42
)

# Create SVD model
model = SVD()

# Train model
model.fit(trainset)

# Test model
predictions = model.test(testset)

# Calculate RMSE
rmse(predictions)
# Predict rating for a user and a movie
prediction = model.predict(1, 296)

print(prediction)
# Load movies dataset
movies = pd.read_csv(r"D:\Movie recommender\ml-latest\movies.csv")

# Movies already rated by User 1
watched = ratings[ratings['userId'] == 1]['movieId'].tolist()

# Movies User 1 has not watched
unwatched = movies[~movies['movieId'].isin(watched)]

# Predict ratings for unwatched movies
predictions = []

for movie_id in unwatched['movieId']:
    pred = model.predict(1, movie_id)
    predictions.append((movie_id, pred.est))

# Sort by predicted rating
predictions.sort(key=lambda x: x[1], reverse=True)

# Top 10 recommendations
top_10 = predictions[:10]

print("\nTop 10 recommendations for User 1:\n")

for movie_id, rating in top_10:
    title = movies[movies['movieId'] == movie_id]['title'].values[0]
    print(f"{title} --> Predicted Rating: {rating:.2f}")