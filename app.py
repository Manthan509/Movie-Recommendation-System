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

                if movie["poster"] != "N/A":
                 st.image(movie["poster"], width=200)
                else:
                 st.write("🎬 Poster not available")
 
                st.subheader(movie["title"])

                st.write("⭐ IMDb Rating:", movie["rating"])

                st.write("📅 Year:", movie["year"])

                st.write("📝 Plot:")
                st.write(movie["plot"])

               

                st.write("---")