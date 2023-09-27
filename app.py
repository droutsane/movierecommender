import streamlit as st
import pickle
import pandas as pd
import requests

movies_list = pd.read_pickle("movie_list.pkl")
movies = pd.DataFrame(movies_list)
movies_list = movies_list['title'].values

similarity = pd.read_pickle("similarity.pkl")


def fetch_poster(movie_id):
   url = "https://api.themoviedb.org/3/movie/{}?api_key=4291f577f758cefc8371138b1df9dc1b&language=en-US".format(
      movie_id)
   data = requests.get(url)
   data = data.json()
   poster_path = data['poster_path']
   full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
   return full_path


def recommend(movie):
   index = movies[movies['title'] == movie].index[0]
   distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
   recommended_movie_name = []
   recommended_movie_poster = []
   for i in distances[1:6]:
      movie_id = movies.iloc[i[0]].movie_id
      recommended_movie_name.append(movies.iloc[i[0]].title)
      recommended_movie_poster.append(fetch_poster(movie_id))
   return recommended_movie_name, recommended_movie_poster


st.title('Movie Recommender System')

selected_movie = st.selectbox(
   "Select Movie to find Similar movies",
   movies_list,
   index=None,
   placeholder="Select a movie...",
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])