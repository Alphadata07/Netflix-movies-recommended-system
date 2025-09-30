import streamlit as st
import pickle
import requests

# Load the movie list and similarity matrix
movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values

# OMDb API Key (Replace with your own key)
OMDB_API_KEY = "3030599d"

st.header("Movie Recommendation System")
selectvalue = st.selectbox("Select Movies From Dropdown", movies_list)

# Function to fetch movie posters from OMDb

def fetch_poster_omdb(movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("Poster")
    return None

# Function to recommend movies and fetch posters
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movies = []
    recommend_posters = []
    for i in distances[1:6]:
        movie_title = movies.iloc[i[0]].title
        recommend_movies.append(movie_title)
        recommend_posters.append(fetch_poster_omdb(movie_title))
    return recommend_movies, recommend_posters

if st.button("Show Recommend"):
    recommended_movies, recommended_posters = recommend(selectvalue)
    cols = st.columns(5)
    for col, movie_name, poster_url in zip(cols, recommended_movies, recommended_posters):
        with col:
            if poster_url:
                st.image(poster_url, width=150)
            st.text(movie_name)
