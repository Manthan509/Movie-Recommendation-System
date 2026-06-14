import streamlit as st
from hybrid import hybrid_recommend
from tmdb import fetch_movie

st.title("🎬 Movie Recommendation System")

movie_name = st.text_input("Enter movie name")

if st.button("Recommend"):

    recommendations = hybrid_recommend(movie_name)

    if len(recommendations) == 0:
        st.error("Movie not found!")

    else:

        st.subheader("Top Recommendations")

        for title, score in recommendations:

            movie = fetch_movie(title)

           if movie:

    if movie.get("poster") and movie["poster"] != "N/A":
        st.image(movie["poster"])
    else:
        st.write("🖼️ Poster not available")

    st.subheader(movie["title"])

    st.write("⭐ IMDb Rating:", movie.get("rating", "N/A"))
    st.write("📅 Year:", movie.get("year", "N/A"))

    st.write("📝 Plot:")
    st.write(movie.get("plot", "N/A"))

    st.write("---")