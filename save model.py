import pandas as pd
import joblib
from surprise import Dataset, Reader, SVD

# Load ratings
ratings = pd.read_csv(r"D:\Movie recommender\ml-latest\ratings.csv")

# Use first 1 million ratings
ratings = ratings.head(1000000)

# Create reader
reader = Reader(rating_scale=(0.5, 5))

# Convert dataframe to Surprise dataset
data = Dataset.load_from_df(
    ratings[['userId', 'movieId', 'rating']],
    reader
)

# Build trainset
trainset = data.build_full_trainset()

# Create model
model = SVD()

print("Training model...")

# Train model
model.fit(trainset)

# Save model
joblib.dump(model, r"D:\Movie recommender\svd_model.pkl")

print("Model saved successfully!")